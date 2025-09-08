import logging
from typing import Dict, List, Tuple


import click
import pandas as pd
from omegaconf import OmegaConf
from tqdm import tqdm
import csv
import os
import re
import wandb
from components.evaluator import GPTEvaluator, NullEvaluator
from components.proposer import (
    LLMProposer,
    LLMProposerDiffusion,
    VLMFeatureProposer,
    VLMProposer,
)
import time
from components.ranker import CLIPRanker, LLMRanker, NullRanker, VLMRanker


def load_config(config: str, prompt:str) -> Dict:
    base_cfg = OmegaConf.load("configs/base.yaml")
    cfg = OmegaConf.load(config)
    final_cfg = OmegaConf.merge(base_cfg, cfg)
    args = OmegaConf.to_container(final_cfg)
    args["config"] = config
    args["proposer"]["prompt"] = prompt
    print("args['proposer']['prompt']: ", args["proposer"]["prompt"])
    if args["wandb"]:
        wandb.init(
            project=args["project"],
            name=args["data"]["name"],
            group=f'{args["data"]["group1"]} - {args["data"]["group2"]} ({args["data"]["purity"]})',
            config=args,
        )
    return args


def load_data(args: Dict) -> Tuple[List[Dict], List[Dict], List[str]]:
    data_args = args["data"]

    df = pd.read_csv(f"{data_args['root']}/{data_args['name']}.csv")

    if data_args["subset"]:
        old_len = len(df)
        df = df[df["subset"] == data_args["subset"]]
        print(
            f"Taking {data_args['subset']} subset (dataset size reduced from {old_len} to {len(df)})"
        )

    dataset1 = df[df["group_name"] == data_args["group1"]].to_dict("records")
    dataset2 = df[df["group_name"] == data_args["group2"]].to_dict("records")
    group_names = [data_args["group1"], data_args["group2"]]

    if data_args["purity"] < 1:
        logging.warning(f"Purity is set to {data_args['purity']}. Swapping groups.")
        assert len(dataset1) == len(dataset2), "Groups must be of equal size"
        n_swap = int((1 - data_args["purity"]) * len(dataset1))
        dataset1 = dataset1[n_swap:] + dataset2[:n_swap]
        dataset2 = dataset2[n_swap:] + dataset1[:n_swap]
    return dataset1, dataset2, group_names


def propose(args: Dict, dataset1: List[Dict], dataset2: List[Dict], image_path: str, output_path: str, modify: bool) -> List[str]:
    proposer_args = args["proposer"]
    proposer_args["seed"] = args["seed"]
    proposer_args["captioner"] = args["captioner"]

    proposer = eval(proposer_args["method"])(proposer_args)
    hypotheses, logs, images = proposer.propose(dataset1, dataset2, image_path, output_path, modify)
    if args["wandb"]:
        wandb.log({"logs": wandb.Table(dataframe=pd.DataFrame(logs))})
        for i in range(len(images)):
            wandb.log(
                {
                    f"group 1 images ({dataset1[0]['group_name']})": images[i][
                        "images_group_1"
                    ],
                    f"group 2 images ({dataset2[0]['group_name']})": images[i][
                        "images_group_2"
                    ],
                }
            )
    return hypotheses

def rank(
    args: Dict,
    hypotheses: List[str],
    dataset1: List[Dict],
    dataset2: List[Dict],
    group_names: List[str],
    metrics_path: str,
    gt_path: str,
) -> List[str]:
    ranker_args = args["ranker"]
    ranker_args["seed"] = args["seed"]

    ranker = eval(ranker_args["method"])(ranker_args)

    scored_hypotheses = ranker.rerank_hypotheses(hypotheses, dataset1, dataset2, metrics_path)
    if args["wandb"]:
        table_hypotheses = wandb.Table(dataframe=pd.DataFrame(scored_hypotheses))
        wandb.log({"scored hypotheses": table_hypotheses})
        for i in range(5):
            wandb.summary[f"top_{i + 1}_difference"] = scored_hypotheses[i][
                "hypothesis"
            ].replace('"', "")
            wandb.summary[f"top_{i + 1}_score"] = scored_hypotheses[i]["auroc"]
    scored_groundtruth = ranker.rerank_hypotheses(
        group_names,
        dataset1,
        dataset2,
        gt_path
    )
    if args["wandb"]:
        table_groundtruth = wandb.Table(dataframe=pd.DataFrame(scored_groundtruth))
        wandb.log({"scored groundtruth": table_groundtruth})

    return [hypothesis["hypothesis"] for hypothesis in scored_hypotheses]


def evaluate(args: Dict, ranked_hypotheses: List[str], group_names: List[str]) -> Dict:
    evaluator_args = args["evaluator"]

    evaluator = eval(evaluator_args["method"])(evaluator_args)

    scores, metrics, evaluated_hypotheses = evaluator.evaluate(
        ranked_hypotheses,
        group_names[0],
        group_names[1],
    )
    return scores, metrics


def main():

    # 規定 cot 只能讀取同樣的圖片
    # BASE_PATH = "/media/yang/473ef2c3-2f01-4bba-83af-723090c8ab20/Project/VisDiff/results/qwen2.5_prompt_imagenetr"
    BASE_PATH = "/media/yang/473ef2c3-2f01-4bba-83af-723090c8ab20/Project/VisDiff/results/final/PIS"
    start_time = time.time()
    # config_dir = "/media/yang/473ef2c3-2f01-4bba-83af-723090c8ab20/Project/VisDiff/configs/sweep_visdiffbench_purity1.0_seed0_evaluate"
    # config_dir = "/media/yang/473ef2c3-2f01-4bba-83af-723090c8ab20/Project/VisDiff/configs/sweep_visdiffbench_purity1.0_seed0_evaluate_30"
    config_dir = "/media/yang/473ef2c3-2f01-4bba-83af-723090c8ab20/Project/VisDiff/configs/sweep_visdiffbench_purity1.0_seed0"
    # config_dir = "/media/yang/473ef2c3-2f01-4bba-83af-723090c8ab20/Project/VisDiff/configs/sweep_imagenetstar"
    model_name = "qwen25cot"
    modify = False  # 是否修改圖片，True 代表修改圖片，False 代表不修改圖片

    # 取得所有 YAML 檔案（包含完整路徑）
    yaml_files = [os.path.join(config_dir, f) for f in os.listdir(config_dir) if f.endswith(".yaml")]

    # 提取數字並排序
    def extract_number(filepath):
        filename = os.path.basename(filepath)  # 取得檔名，不包含路徑
        match = re.search(r'^\d+', filename)   # 尋找開頭的數字
        return int(match.group()) if match else float('inf')  # 若找不到數字，設為無窮大（排最後）
    sorted_configs = sorted(yaml_files)
    # 印出排序結果
    print("sorted_configs", sorted_configs)

    for idx, config in enumerate(sorted_configs):
        print(f"\n正在執行第 {idx + 1}/{len(sorted_configs)} 個 YAML 配置檔案: {config}")
        logging.info("Loading config...")
        args = load_config(config, 'VLM_PROPOSE_AND_RANK_PROMPT_COT_V7')
        logging.info("Loading data...")
        dataset1, dataset2, group_names = load_data(args)

        name = group_names[0] # or idx+1
        
        logging.info("Proposing hypotheses...")
        if modify:
            images_path = os.path.join(BASE_PATH,f'images/modified_picture/image_{name}')
            is_modified = "modified"
        else:
            images_path = os.path.join(BASE_PATH,f'images/normal_picture/image_{name}')
            is_modified = "normal"
        output_dir = os.path.join(BASE_PATH, 'results/qwen25cot')
        os.makedirs(output_dir, exist_ok=True)  # 若資料夾不存在則建立，不會報錯
        output_path = os.path.join(output_dir,f'output_{name}.csv')

        hypotheses = propose(args, dataset1, dataset2, images_path, output_path, modify)
        print("hypotheses: ", hypotheses)

        if modify:
            result_output_path = os.path.join(BASE_PATH,f'hypotheses/{model_name}/modified_picture')
        else:
            result_output_path = os.path.join(BASE_PATH,f'hypotheses/{model_name}/normal_picture')
        os.makedirs(result_output_path, exist_ok=True)
        result_path = os.path.join(result_output_path,f'hypotheses_{name}.csv')
        file_exists = os.path.isfile(result_path)
        with open(result_path, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['hypothesis'])
            for hypothesis in hypotheses:
                writer.writerow([hypothesis])

        logging.info("Evaluating hypotheses...")
        hypotheses = hypotheses[:5]
        scores1, metrics1 = evaluate(args, hypotheses, group_names)
        print("scores: " ,scores1)
        print("metrics: " ,metrics1)
        score_path = os.path.join(BASE_PATH,'scores')
        os.makedirs(score_path, exist_ok=True)
        csv_file = os.path.join(BASE_PATH,f'scores/scores_{model_name}_{is_modified}.csv')
        file_exists = os.path.isfile(csv_file)
        with open(csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['scores', 'metrics'])
            writer.writerow([scores1, metrics1])


    end_time = time.time()
    total_time = end_time - start_time
    
    # 轉換成時分秒格式
    hours = int(total_time // 3600)
    minutes = int((total_time % 3600) // 60)
    seconds = int(total_time % 60)
    
    print(f"\n總執行時間: {hours}小時 {minutes}分鐘 {seconds}秒")
    print(f"總執行時間(秒): {total_time:.2f}秒")





if __name__ == "__main__":
    main()

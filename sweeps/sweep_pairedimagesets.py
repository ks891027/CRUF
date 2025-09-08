import json
import os
import random

import click
import time


@click.command()
@click.option("--seed", default=0, type=int)
@click.option("--purity", default=1.0, type=float)
def main(purity: float, seed: int):
    random.seed(0)
    start_time = time.time()
    # scores_path = '/home/yang/Documents/Project/VisDiff/results/scores.csv'
    # if os.path.isfile(scores_path):
    #     with open(scores_path, 'w', newline='') as f:
    #         print("file cleared!")
    root = "data/VisDiffBench"
    easy = [json.loads(line) for line in open(f"{root}/easy.jsonl")]
    medium = [json.loads(line) for line in open(f"{root}/medium.jsonl")]
    hard = [json.loads(line) for line in open(f"{root}/hard.jsonl")]
    data = easy + medium + hard
    print(f"Total number of items: {len(data)}")
    print(f"Easy: {len(easy)}")
    print(f"Medium: {len(medium)}")
    print(f"Hard: {len(hard)}")
    for idx in range(0, 150):  # 150
        item = data[idx]
        cfg = f"""
project: PairedImageSets
seed: {seed}  # random seed

data:
  name: PairedImageSets
  group1: "{item['set1']}"
  group2: "{item['set2']}"
  purity: {purity}
"""

        difficulty = (
            "easy"
            if idx < len(easy)
            else "medium"
            if idx < len(easy) + len(medium)
            else "hard"
        )
        cfg_dir = f"configs/sweep_visdiffbench_purity{purity}_seed{seed}"
        if not os.path.exists(cfg_dir):
            os.makedirs(cfg_dir)
        cfg_file = f"{cfg_dir}/{idx}_{difficulty}.yaml"
        with open(cfg_file, "w") as f:
            f.write(cfg)
        print(f"python main.py --config {cfg_file}")
        os.system(f"python main.py --config {cfg_file}")

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

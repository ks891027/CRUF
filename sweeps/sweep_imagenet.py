import os
import random
import time
group_names_r = [
    "art",
    "cartoon",
    "deviantart",
    "embroidery",
    "graffiti",
    "graphic",
    "origami",
    "painting",
    "sculpture",
    "sketch",
    "sticker",
    "tattoo",
    "toy",
    "videogame",
]
group_names_star = [
    "in the forest",
    "green",
    "red",
    "pencil sketch",
    "oil painting",
    "orange",
    "on the rocks",
    "in bright sunlight",
    "person and a",
    "in the beach",
    "studio lighting",
    "in the water",
    "at dusk",
    "in the rain",
    "in the grass",
    "yellow",
    "blue",
    "and a flower",
    "on the road",
    "at night",
    "embroidery",
    "in the fog",
    "in the snow",
]


def main_r():
    random.seed(0)
    start_time = time.time()

    for group_name in group_names_r:
        cfg = f"""
project: ImageNetR

data:
  name: ImageNetR
  group1: "{group_name}"
  group2: "imagenet"
"""
        cfg_dir = f"configs/sweep_imagenetr"
        if not os.path.exists(cfg_dir):
            os.makedirs(cfg_dir)
        cfg_file = f"{cfg_dir}/{group_name}-imagenet.yaml"
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


def main_star():
    random.seed(0)
    start_time = time.time()

    for group_name in group_names_star:
        cfg = f"""
project: ImageNetStar

data:
  name: ImageNetStar
  group1: "{group_name}"
  group2: "base"
"""
        cfg_dir = f"configs/sweep_imagenetstar"
        if not os.path.exists(cfg_dir):
            os.makedirs(cfg_dir)
        cfg_file = (
            f"{cfg_dir}/{group_name.replace(' ', '_')}-base.yaml"
        )
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
    # main_r()
    main_star()

import hashlib
from typing import Dict, List, Optional

import lmdb
# from PIL import Image
from PIL import Image, ImageDraw, ImageFont


def resize_image(image: Image.Image, size=(256, 256)) -> Image.Image:
    return image.resize(size)


def merge_images_horizontally(images: List[Image.Image], gap: int = 10) -> Image.Image:
    imgs = [resize_image(image) for image in images]
    total_width = sum(img.width for img in imgs) + gap * (len(imgs) - 1)
    height = imgs[0].height

    merged = Image.new("RGB", (total_width, height))

    x_offset = 0
    for img in imgs:
        merged.paste(img, (x_offset, 0))
        x_offset += img.width + gap

    return merged


def merge_images_vertically(images: List[Image.Image], gap: int = 10) -> Image.Image:
    imgs = images
    total_height = sum(img.height for img in imgs) + gap * (len(imgs) - 1)
    width = max(img.width for img in imgs)

    merged = Image.new("RGB", (width, total_height))

    y_offset = 0
    for img in imgs:
        merged.paste(img, (0, y_offset))
        y_offset += img.height + gap

    return merged

def combine_dataset_image(dataset: List[Dict], save_path: str):
    n_images = len(dataset)
    # Load images into memory as PIL Image objects
    images_dataset = [Image.open(item["path"]) for item in dataset]

    # Merge images from the same dataset horizontally
    merged_images_dataset1_first = merge_images_horizontally(
        images_dataset[: n_images // 2]
    )
    merged_images_dataset1_second = merge_images_horizontally(
        images_dataset[n_images // 2 :]
    )

    # Merge the resulting images from different datasets vertically
    final_merged_image = merge_images_vertically(
        [
            merged_images_dataset1_first,
            merged_images_dataset1_second,
        ]
    )

    # Save the merged image
    final_merged_image.save(save_path)

def draw_border(image: Image.Image, color: str, width: int = 5) -> Image.Image:
    draw = ImageDraw.Draw(image)
    for i in range(width):
        draw.rectangle([i, i, image.width - 1 - i, image.height - 1 - i], outline=color)
    return image

def add_label_above(image: Image.Image, label: str, color: str, font_size: int = 24) -> Image.Image:
    font = ImageFont.load_default()
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        pass  # fallback to default

    # 改用 getbbox 取代 getsize
    bbox = font.getbbox(label)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    padding = 10
    new_height = image.height + text_height + padding
    new_img = Image.new("RGB", (image.width, new_height), (255, 255, 255))
    draw = ImageDraw.Draw(new_img)
    draw.text(
        ((image.width - text_width) // 2, padding // 2),
        label,
        fill=color,
        font=font,
    )
    new_img.paste(image, (0, text_height + padding))
    return new_img

def save_data_diff_image(dataset1: List[Dict], dataset2: List[Dict], save_path: str, modify: bool = False):
    assert len(dataset1) == len(dataset2), "Datasets must be of the same length"
    n_images = len(dataset1)

    # Load images into memory as PIL Image objects, if modify is True, draw borders
    if modify:
        images_dataset1 = [
            draw_border(Image.open(item["path"]).convert("RGB"), color="red") for item in dataset1
        ]
        images_dataset2 = [
            draw_border(Image.open(item["path"]).convert("RGB"), color="green") for item in dataset2
        ]
    else:
        images_dataset1 = [Image.open(item["path"]) for item in dataset1]
        images_dataset2 = [Image.open(item["path"]) for item in dataset2]
    

    # Merge images from the same dataset horizontally
    merged_images_dataset1_first = merge_images_horizontally(
        images_dataset1[: n_images // 2]
    )
    merged_images_dataset1_second = merge_images_horizontally(
        images_dataset1[n_images // 2 :]
    )
    merged_images_dataset2_first = merge_images_horizontally(
        images_dataset2[: n_images // 2]
    )
    merged_images_dataset2_second = merge_images_horizontally(
        images_dataset2[n_images // 2 :]
    )

    # Add labels above the merged images when modify is True
    # if modify:
    #     merged_images_dataset1_first = add_label_above(merged_images_dataset1_first, "Group A", "red")
    #     merged_images_dataset1_second = add_label_above(merged_images_dataset1_second, "Group A", "red")
    #     merged_images_dataset2_first = add_label_above(merged_images_dataset2_first, "Group B", "green")
    #     merged_images_dataset2_second = add_label_above(merged_images_dataset2_second, "Group B", "green")
    
    # Merge the resulting images from different datasets vertically
    final_merged_image = merge_images_vertically(
        [
            merged_images_dataset1_first,
            merged_images_dataset1_second,
            merged_images_dataset2_first,
            merged_images_dataset2_second,
        ]
    )

    # Save the merged image
    final_merged_image.save(save_path)


def hash_key(key) -> str:
    return hashlib.sha256(key.encode()).hexdigest()


def get_from_cache(key: str, env: lmdb.Environment) -> Optional[str]:
    with env.begin(write=False) as txn:
        hashed_key = hash_key(key)
        value = txn.get(hashed_key.encode())
    if value:
        return value.decode()
    return None


def save_to_cache(key: str, value: str, env: lmdb.Environment):
    with env.begin(write=True) as txn:
        hashed_key = hash_key(key)
        txn.put(hashed_key.encode(), value.encode())

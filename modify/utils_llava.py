import json
import logging
import threading
import base64

logging.basicConfig(level=logging.INFO)

import os
from typing import Dict, List

import lmdb
import requests
from tqdm import tqdm, trange

from serve.global_vars import BLIP_FEATURE_URL, BLIP_URL, LLAVA_URL, VLM_CACHE_FILE, LLAVA_NEXT_URL, QWEN2_URL, LLAVA_CODE_PATH
from serve.utils_general import get_from_cache, save_to_cache

if not os.path.exists(VLM_CACHE_FILE):
    os.makedirs(VLM_CACHE_FILE)

vlm_cache = lmdb.open(VLM_CACHE_FILE, map_size=int(1e11))

import sys
from dataclasses import dataclass

import torch
from flask import Flask, jsonify, request

sys.path.append(LLAVA_CODE_PATH)
from llava.constants import (
    DEFAULT_IM_END_TOKEN,
    DEFAULT_IM_START_TOKEN,
    DEFAULT_IMAGE_TOKEN,
    IMAGE_TOKEN_INDEX,
)
from llava.conversation import SeparatorStyle, conv_templates
from llava.mm_utils import (
    KeywordsStoppingCriteria,
    get_model_name_from_path,
    process_images,
    tokenizer_image_token,
)
from llava.model.builder import load_pretrained_model
from llava.utils import disable_torch_init
from PIL import Image
from transformers import BitsAndBytesConfig


@dataclass
class Args:
    model_path: str = "liuhaotian/llava-v1.5-13b"
    device: str = "cuda"
    temperature: float = 0.2
    max_new_tokens: int = 512
    image_aspect_ratio: str = "pad"
    load_in_8bit: bool = True  # Enable 4-bit quantization
    use_double_quant: bool = True  # Use nested quantization
    bnb_8bit_compute_dtype: torch.dtype = torch.float16
    bnb_8bit_quant_type: str = "8"  # Use normal float 4 for better accuracy


args = Args()

# Setup logging
logging.basicConfig(level=logging.INFO)

# Model setup
disable_torch_init()

quantization_config = BitsAndBytesConfig(
    load_in_8bit=args.load_in_8bit,
    bnb_8bit_compute_dtype=args.bnb_8bit_compute_dtype,  # Using 8-bit compute dtype
    llm_int8_enable_fp32_cpu_offload=True,  # Enable FP32 CPU offload for 8-bit
)

model_name = get_model_name_from_path(args.model_path)
tokenizer, model, image_processor, context_len = load_pretrained_model(
    args.model_path, None, model_name, False, False, device=args.device, quantization_config=quantization_config
)


logging.info("Model loaded successfully!")

def interact_with_llava(files, text_data, model_n):
    key = json.dumps([model_n, files, text_data])
    if "llama-2" in model_name.lower():
        conv_mode = "llava_llama_2"
    elif "v1" in model_name.lower():
        conv_mode = "llava_v1"
    elif "mpt" in model_name.lower():
        conv_mode = "mpt"
    else:
        conv_mode = "llava_v0"

    conv = conv_templates[conv_mode].copy()
    if "mpt" in model_name.lower():
        roles = ("user", "assistant")
    else:
        roles = conv.roles
    raw_image = Image.open(files).convert("RGB")
    image_tensor = process_images([raw_image], image_processor, args)

    if type(image_tensor) is list:
        image_tensor = [
            image.to(model.device, dtype=torch.float16) for image in image_tensor
        ]
    else:
        image_tensor = image_tensor.to(model.device, dtype=torch.float16)

    inp = text_data

    if model.config.mm_use_im_start_end:
        inp = (
            DEFAULT_IM_START_TOKEN
            + DEFAULT_IMAGE_TOKEN
            + DEFAULT_IM_END_TOKEN
            + "\n"
            + inp
        )
    else:
        inp = DEFAULT_IMAGE_TOKEN + "\n" + inp

    conv.append_message(conv.roles[0], inp)
    conv.append_message(conv.roles[1], None)
    prompt = conv.get_prompt()

    input_ids = (
        tokenizer_image_token(prompt, tokenizer, IMAGE_TOKEN_INDEX, return_tensors="pt")
        .unsqueeze(0)
        .cuda()
    )
    stop_str = conv.sep if conv.sep_style != SeparatorStyle.TWO else conv.sep2
    keywords = [stop_str]
    stopping_criteria = KeywordsStoppingCriteria(keywords, tokenizer, input_ids)
    with torch.inference_mode():
        output_ids = model.generate(
            input_ids,
            images=image_tensor,
            do_sample=True,
            temperature=args.temperature,
            max_new_tokens=args.max_new_tokens,
            use_cache=False,
            stopping_criteria=[stopping_criteria],
        )
    
    outputs = tokenizer.decode(output_ids[0]).strip()
    # outputs = tokenizer.decode(output_ids[0, input_ids.shape[1] :]).strip()
    print("outputs: ", outputs)
    conv.messages[-1][-1] = outputs
    save_to_cache(key, outputs, vlm_cache)
    # print(image_tensor, conv, inp)
    return outputs




def get_image_base64(image_path):
    with open(image_path, 'rb') as file:
        return base64.b64encode(file.read()).decode('utf-8')

def get_llava_output(hypothesis: str, dataset: List[dict], model_n: str) -> List[float]:
    scores = []
    invalid_scores = []
    for i in trange(0, len(dataset)):
        item = dataset[i]
        image = item["path"]
        prompt = f"Does this image contain {hypothesis.replace('and ', '')}?"  # TODO: why this prompt
        key = json.dumps([model_n, image, prompt])
        if model_n in ["blip", "llava", 'llava_next', "qwen2"]:
            response = interact_with_llava(image, prompt).json()
            output = response["output"]
            save_to_cache(key, output, vlm_cache)
        if "yes" in output.lower():
            scores.append(1)
        elif "no" in output.lower():
            scores.append(0)
        else:
            invalid_scores.append(output)
    print(f"Percent Invalid {len(invalid_scores) / len(dataset)}")
    print(f"scores: {scores}")
    return scores, invalid_scores

    

def captioning(image: str, model_n: str) -> str:
    caption = get_llava_output(image, "Describe this image in detail.", model_n)
    return caption


def vqa(image: str, question: str, model_n: str) -> str:
    answer = get_llava_output(image, question, model_n)
    return answer


def test_get_vlm_output():
    image = "data/teaser.png"
    model_n = "blip"

    caption = captioning(image, model_n)
    print(f"{caption=}")
    question = "Is there a table in the image?"
    answer = vqa(image, question, model_n)
    print(f"{answer=}")

    model_n = "gpt-4-vision-preview"

    caption = captioning(image, model_n)
    print(f"{caption=}")
    question = "Is there a table in the image?"
    answer = vqa(image, question, model_n)
    print(f"{answer=}")

    model_n = "llava"

    caption = captioning(image, model_n)
    print(f"{caption=}")
    question = "Is there a table in the image?"
    answer = vqa(image, question, model_n)
    print(f"{answer=}")


def test_get_vlm_output_parallel():
    threads = []

    for _ in range(3):
        thread = threading.Thread(target=test_get_vlm_output)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    test_get_vlm_output()
    # test_get_vlm_output_parallel()

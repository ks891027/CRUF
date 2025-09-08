# # import logging
# # import sys
# # from dataclasses import dataclass

# # import torch
# # from flask import Flask, jsonify, request
# # from global_vars import LLAVA_CODE_PATH

# # sys.path.append(LLAVA_CODE_PATH)
# # from llava.constants import (
# #     DEFAULT_IM_END_TOKEN,
# #     DEFAULT_IM_START_TOKEN,
# #     DEFAULT_IMAGE_TOKEN,
# #     IMAGE_TOKEN_INDEX,
# # )
# # from llava.conversation import SeparatorStyle, conv_templates
# # from llava.mm_utils import (
# #     KeywordsStoppingCriteria,
# #     get_model_name_from_path,
# #     process_images,
# #     tokenizer_image_token,
# # )
# # from llava.model.builder import load_pretrained_model
# # from llava.utils import disable_torch_init
# # from PIL import Image
# # from transformers import BitsAndBytesConfig


# @dataclass
# class Args:
#     model_path: str = "liuhaotian/llava-v1.5-13b"
#     device: str = "cuda"
#     temperature: float = 0.2
#     max_new_tokens: int = 2048
#     image_aspect_ratio: str = "pad"
#     load_in_8bit: bool = True  # Enable 4-bit quantization
#     use_double_quant: bool = True  # Use nested quantization
#     bnb_8bit_compute_dtype: torch.dtype = torch.float16
#     bnb_8bit_quant_type: str = "8"  # Use normal float 4 for better accuracy


# args = Args()

# app = Flask(__name__)

# # Setup logging
# logging.basicConfig(level=logging.INFO)

# # Model setup
# disable_torch_init()

# quantization_config = BitsAndBytesConfig(
#     load_in_8bit=args.load_in_8bit,
#     bnb_8bit_compute_dtype=args.bnb_8bit_compute_dtype,  # Using 8-bit compute dtype
#     llm_int8_enable_fp32_cpu_offload=True,  # Enable FP32 CPU offload for 8-bit
# )

# model_name = get_model_name_from_path(args.model_path)
# tokenizer, model, image_processor, context_len = load_pretrained_model(
#     args.model_path, None, model_name, False, False, device=args.device, quantization_config=quantization_config
# )


# logging.info("Model loaded successfully!")

# @app.route("/", methods=["POST"])
# def interact_with_llava():
#     if "image" not in request.files:
#         return jsonify({"error": "Image not provided"}), 400

#     if "text" not in request.form:
#         return jsonify({"error": "Text not provided"}), 400

#     if "llama-2" in model_name.lower():
#         conv_mode = "llava_llama_2"
#     elif "v1" in model_name.lower():
#         conv_mode = "llava_v1"
#     elif "mpt" in model_name.lower():
#         conv_mode = "mpt"
#     else:
#         conv_mode = "llava_v0"

#     conv = conv_templates[conv_mode].copy()
#     if "mpt" in model_name.lower():
#         roles = ("user", "assistant")
#     else:
#         roles = conv.roles
#     print("true image:", request.files["image"])
#     raw_image = Image.open(request.files["image"]).convert("RGB")
#     print("raw_image: ", raw_image)
#     image_tensor = process_images([raw_image], image_processor, args)

#     if type(image_tensor) is list:
#         image_tensor = [
#             image.to(model.device, dtype=torch.float16) for image in image_tensor
#         ]
#     else:
#         image_tensor = image_tensor.to(model.device, dtype=torch.float16)

#     inp = request.form["text"]

#     if model.config.mm_use_im_start_end:
#         inp = (
#             DEFAULT_IM_START_TOKEN
#             + DEFAULT_IMAGE_TOKEN
#             + DEFAULT_IM_END_TOKEN
#             + "\n"
#             + inp
#         )
#     else:
#         inp = DEFAULT_IMAGE_TOKEN + "\n" + inp

#     conv.append_message(conv.roles[0], inp)
#     conv.append_message(conv.roles[1], None)
#     prompt = conv.get_prompt()

#     input_ids = (
#         tokenizer_image_token(prompt, tokenizer, IMAGE_TOKEN_INDEX, return_tensors="pt")
#         .unsqueeze(0)
#         .cuda()
#     )
#     stop_str = conv.sep if conv.sep_style != SeparatorStyle.TWO else conv.sep2
#     keywords = [stop_str]
#     stopping_criteria = KeywordsStoppingCriteria(keywords, tokenizer, input_ids)
#     with torch.inference_mode():
#         output_ids = model.generate(
#             input_ids,
#             images=image_tensor,
#             do_sample=True,
#             temperature=args.temperature,
#             max_new_tokens=args.max_new_tokens,
#             use_cache=False,
#             repetition_penalty=1.1
#             # stopping_criteria=[stopping_criteria],
#             # stop_sequences = ["### End", "\n\n\n"],
#         )
#         # print("out_ids: ", output_ids)
    
#     outputs = tokenizer.decode(output_ids[0]).strip()
#     # outputs = tokenizer.decode(output_ids[0, input_ids.shape[1] :]).strip()
#     # print("outputs: ", outputs)
#     conv.messages[-1][-1] = outputs

#     # print(image_tensor, conv, inp)

#     return jsonify({"input": prompt, "output": outputs})


# if __name__ == "__main__":
#     logging.info("Server is running!")
#     app.run(host="0.0.0.0", port=8084, debug=False)


# # fp16

# import logging
# import sys
# from dataclasses import dataclass

# import torch
# from flask import Flask, jsonify, request
# from global_vars import LLAVA_CODE_PATH

# sys.path.append(LLAVA_CODE_PATH)
# from llava.constants import (
#     DEFAULT_IM_END_TOKEN,
#     DEFAULT_IM_START_TOKEN,
#     DEFAULT_IMAGE_TOKEN,
#     IMAGE_TOKEN_INDEX,
# )
# from llava.conversation import SeparatorStyle, conv_templates
# from llava.mm_utils import (
#     KeywordsStoppingCriteria,
#     get_model_name_from_path,
#     process_images,
#     tokenizer_image_token,
# )
# from llava.model.builder import load_pretrained_model
# from llava.utils import disable_torch_init
# from PIL import Image


# @dataclass
# class Args:
#     model_path: str = "liuhaotian/llava-v1.5-13b"
#     device: str = "cuda"
#     temperature: float = 0.2
#     max_new_tokens: int = 512
#     image_aspect_ratio: str = "pad"


# args = Args()

# app = Flask(__name__)

# # Setup logging
# logging.basicConfig(level=logging.INFO)

# # Model setup
# disable_torch_init()

# model_name = get_model_name_from_path(args.model_path)
# tokenizer, model, image_processor, context_len = load_pretrained_model(
#     args.model_path, None, model_name, False, False, device=args.device
# )


# logging.info("Model loaded successfully!")


# @app.route("/", methods=["POST"])
# def interact_with_llava():
#     if "image" not in request.files:
#         return jsonify({"error": "Image not provided"}), 400

#     if "text" not in request.form:
#         return jsonify({"error": "Text not provided"}), 400

#     if "llama-2" in model_name.lower():
#         conv_mode = "llava_llama_2"
#     elif "v1" in model_name.lower():
#         conv_mode = "llava_v1"
#     elif "mpt" in model_name.lower():
#         conv_mode = "mpt"
#     else:
#         conv_mode = "llava_v0"

#     conv = conv_templates[conv_mode].copy()
#     if "mpt" in model_name.lower():
#         roles = ("user", "assistant")
#     else:
#         roles = conv.roles

#     raw_image = Image.open(request.files["image"]).convert("RGB")
#     image_tensor = process_images([raw_image], image_processor, args)
#     if type(image_tensor) is list:
#         image_tensor = [
#             image.to(model.device, dtype=torch.float16) for image in image_tensor
#         ]
#     else:
#         image_tensor = image_tensor.to(model.device, dtype=torch.float16)

#     inp = request.form["text"]

#     if model.config.mm_use_im_start_end:
#         inp = (
#             DEFAULT_IM_START_TOKEN
#             + DEFAULT_IMAGE_TOKEN
#             + DEFAULT_IM_END_TOKEN
#             + "\n"
#             + inp
#         )
#     else:
#         inp = DEFAULT_IMAGE_TOKEN + "\n" + inp

#     conv.append_message(conv.roles[0], inp)
#     conv.append_message(conv.roles[1], None)
#     prompt = conv.get_prompt()

#     input_ids = (
#         tokenizer_image_token(prompt, tokenizer, IMAGE_TOKEN_INDEX, return_tensors="pt")
#         .unsqueeze(0)
#         .cuda()
#     )
#     stop_str = conv.sep if conv.sep_style != SeparatorStyle.TWO else conv.sep2
#     keywords = [stop_str]
#     stopping_criteria = KeywordsStoppingCriteria(keywords, tokenizer, input_ids)

#     with torch.inference_mode():
#         output_ids = model.generate(
#             input_ids,
#             images=image_tensor,
#             do_sample=True,
#             temperature=args.temperature,
#             max_new_tokens=args.max_new_tokens,
#             use_cache=True,
#             stopping_criteria=[stopping_criteria],
#         )

#     outputs = tokenizer.decode(output_ids[0, input_ids.shape[1] :]).strip()
#     conv.messages[-1][-1] = outputs

#     return jsonify({"input": prompt, "output": outputs})


# if __name__ == "__main__":
#     logging.info("Server is running!")
#     app.run(host="0.0.0.0", port=8084, debug=False)

import logging
import sys
from dataclasses import dataclass
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
import torch
from flask import Flask, jsonify, request
from global_vars import LLAVA_CODE_PATH

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


@dataclass
class Args:
    model_path: str = "liuhaotian/llava-v1.5-13b"
    device: str = "cuda"
    temperature: float = 0.2
    max_new_tokens: int = 512
    image_aspect_ratio: str = "pad"


args = Args()

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO)

# Model setup
disable_torch_init()

model_name = get_model_name_from_path(args.model_path)
tokenizer, model, image_processor, context_len = load_pretrained_model(
    args.model_path, None, model_name, False, False, device=args.device
)


logging.info("Model loaded successfully!")


@app.route("/", methods=["POST"])
def interact_with_llava():
    if "image" not in request.files:
        return jsonify({"error": "Image not provided"}), 400

    if "text" not in request.form:
        return jsonify({"error": "Text not provided"}), 400

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

    raw_image = Image.open(request.files["image"]).convert("RGB")
    image_tensor = process_images([raw_image], image_processor, args)
    if type(image_tensor) is list:
        image_tensor = [
            image.to(model.device, dtype=torch.float16) for image in image_tensor
        ]
    else:
        image_tensor = image_tensor.to(model.device, dtype=torch.float16)

    inp = request.form["text"]

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
        .to(args.device)
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
            use_cache=True,
            stopping_criteria=[stopping_criteria],
        )

    outputs = tokenizer.decode(output_ids[0, input_ids.shape[1] :]).strip()
    conv.messages[-1][-1] = outputs

    return jsonify({"input": prompt, "output": outputs})


if __name__ == "__main__":
    logging.info("Server is running!")
    app.run(host="0.0.0.0", port=8084, debug=False)
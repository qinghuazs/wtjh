"""Doubao Seedream 4.5 multi-reference -> group output node."""

from __future__ import annotations

from typing import Any, Dict, List

import torch

from ...base import BaseWyjhNode
from ....config import get_ssl_verify
from ....utils.image_io import decode_base64_image, download_image, extract_image_list, pil_to_tensor
from ....utils.timing import time_block
from .doubao_seedream_4_5_img2img import _split_image_inputs


class WyjhDoubaoSeedream45MultiRefGroup(BaseWyjhNode):
    """Multi reference images -> group images output."""

    INPUT_IS_LIST = ("image_urls",)

    SIZE_CHOICES = {
        "1024x1024 (1:1)": "1024x1024",
        "2048x2048 (1:1)": "2048x2048",
        "2304x1728 (4:3)": "2304x1728",
        "2496x1664 (3:2)": "2496x1664",
        "2560x1440 (16:9)": "2560x1440",
        "3024x1296 (21:9)": "3024x1296",
    }

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": "", "forceInput": True}),
                "image_urls": ("STRING", {"default": "", "forceInput": True}),
            },
            "optional": {
                "size": (list(cls.SIZE_CHOICES.keys()), {"default": "2048x2048 (1:1)"}),
                "max_images": ("INT", {"default": 4, "min": 1, "max": 8, "step": 1}),
                "watermark": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate"
    CATEGORY = "WYJH/Image2Image"

    def generate(
        self,
        prompt: str,
        image_urls: str,
        size: str = "2048x2048 (1:1)",
        max_images: int = 4,
        watermark: bool = False,
    ):
        with time_block("WYJH Doubao Seedream 4.5 Multi Ref Group"):
            if isinstance(prompt, (list, tuple)):
                prompt = prompt[0] if prompt else ""
            if isinstance(size, (list, tuple)):
                size = size[0] if size else "2048x2048 (1:1)"
            if isinstance(watermark, (list, tuple)):
                watermark = bool(watermark[0]) if watermark else False
            if isinstance(max_images, (list, tuple)):
                max_images = int(max_images[0]) if max_images else 4

            images: List[str] = []
            if isinstance(image_urls, (list, tuple)):
                for item in image_urls:
                    if isinstance(item, str):
                        images.extend(_split_image_inputs(item))
            else:
                images = _split_image_inputs(image_urls)
            if not images:
                raise ValueError("image_urls is required")

            size_value = self.SIZE_CHOICES.get(size, size)
            payload: Dict[str, Any] = {
                "model": "doubao-seedream-4-5-251128",
                "prompt": prompt,
                "image": images,
                "size": size_value,
                "sequential_image_generation": "auto",
                "sequential_image_generation_options": {
                    "max_images": max_images,
                },
                "stream": False,
                "response_format": "url",
                "watermark": watermark,
            }
            print("[WYJH] Doubao Seedream 4.5 Multi Ref Group payload:", payload)
            response = self.call("/v1/images/generations", payload)
            print("[WYJH] Doubao Seedream 4.5 Multi Ref Group response:", response)
            values = extract_image_list(response)
            images_out = []
            for value in values:
                if isinstance(value, str) and value.startswith("http"):
                    images_out.append(download_image(value, verify=get_ssl_verify()))
                else:
                    images_out.append(decode_base64_image(value))
            tensors = [pil_to_tensor(img) for img in images_out]
            batch = torch.cat(tensors, dim=0)
            return (batch,)

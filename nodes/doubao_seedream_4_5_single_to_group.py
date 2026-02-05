"""Doubao Seedream 4.5 single image -> group output node."""

from __future__ import annotations

from typing import Any, Dict

import torch

from .base import BaseWyjhNode
from ..config import get_ssl_verify
from ..utils.image_io import decode_base64_image, download_image, extract_image_list, pil_to_tensor
from ..utils.timing import time_block


class WyjhDoubaoSeedream45SingleToGroup(BaseWyjhNode):
    """Single image input -> multi image output."""

    SIZE_CHOICES = {
        "1K": "1K",
        "1024x1024 (1:1)": "1024x1024",
        "2K": "2K",
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
                "image_url": ("STRING", {"default": "", "forceInput": True}),
            },
            "optional": {
                "size": (list(cls.SIZE_CHOICES.keys()), {"default": "2048x2048 (1:1)"}),
                "max_images": ("INT", {"default": 4, "min": 1, "max": 8, "step": 1}),
                "watermark": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate"
    CATEGORY = "WYJH/Image2Image"

    def generate(
        self,
        prompt: str,
        image_url: str,
        size: str = "2048x2048 (1:1)",
        max_images: int = 4,
        watermark: bool = True,
    ):
        with time_block("WYJH Doubao Seedream 4.5 Single To Group"):
            if not image_url:
                raise ValueError("image_url is required")
            size_value = self.SIZE_CHOICES.get(size, size)
            payload: Dict[str, Any] = {
                "model": "doubao-seedream-4-5-251128",
                "prompt": prompt,
                "image": image_url,
                "size": size_value,
                "sequential_image_generation": "auto",
                "sequential_image_generation_options": {
                    "max_images": max_images,
                },
                "stream": False,
                "response_format": "url",
                "watermark": watermark,
            }
            print("[WYJH] Doubao Seedream 4.5 Single To Group payload:", payload)
            response = self.call("/v1/images/generations", payload)
            print("[WYJH] Doubao Seedream 4.5 Single To Group response:", response)
            values = extract_image_list(response)
            images = []
            for value in values:
                if isinstance(value, str) and value.startswith("http"):
                    images.append(download_image(value, verify=get_ssl_verify()))
                else:
                    images.append(decode_base64_image(value))
            tensors = [pil_to_tensor(img) for img in images]
            batch = torch.cat(tensors, dim=0)
            return (batch,)

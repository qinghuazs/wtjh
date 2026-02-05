"""Doubao Seedream 4.5 text-to-image node (single output)."""

from __future__ import annotations

from typing import Any, Dict

import torch

from .base import BaseWyjhNode
from ..config import get_ssl_verify
from ..utils.image_io import decode_base64_image, download_image, extract_image_list, pil_to_tensor
from ..utils.timing import time_block


class WyjhDoubaoSeedream45Txt2Img(BaseWyjhNode):
    """Text-to-image node for doubao-seedream-4-5-251128."""

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
            },
            "optional": {
                "size": (list(cls.SIZE_CHOICES.keys()), {"default": "2048x2048 (1:1)"}),
                "watermark": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate"
    CATEGORY = "WYJH/Text2Image"

    def generate(
        self,
        prompt: str,
        size: str = "2048x2048 (1:1)",
        watermark: bool = True,
    ):
        with time_block("WYJH Doubao Seedream 4.5 Txt2Img"):
            size_value = self.SIZE_CHOICES.get(size, size)
            payload: Dict[str, Any] = {
                "model": "doubao-seedream-4-5-251128",
                "prompt": prompt,
                "size": size_value,
                "sequential_image_generation": "disabled",
                "stream": False,
                "response_format": "url",
                "watermark": watermark,
            }
            print("[WYJH] Doubao Seedream 4.5 Txt2Img payload:", payload)
            response = self.call("/v1/images/generations", payload)
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

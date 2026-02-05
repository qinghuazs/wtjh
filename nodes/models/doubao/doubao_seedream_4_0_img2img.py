"""Doubao Seedream 4.0 image-to-image node."""

from __future__ import annotations

from typing import Any, Dict

import torch

from wyjh.nodes.base import BaseWyjhNode
from wyjh.config import get_ssl_verify
from wyjh.utils.image_io import decode_base64_image, download_image, extract_image_list, pil_to_tensor
from wyjh.utils.timing import time_block


class WyjhDoubaoSeedream40Img2Img(BaseWyjhNode):
    """Image-to-image node for doubao-seedream-4-0-250828."""

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
                "image_url": ("STRING", {"default": "", "forceInput": True}),
            },
            "optional": {
                "size": (list(cls.SIZE_CHOICES.keys()), {"default": "2048x2048 (1:1)"}),
                "watermark": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate"
    CATEGORY = "WYJH/Image2Image"

    def generate(
        self,
        prompt: str,
        image_url: str,
        size: str = "2048x2048",
        watermark: bool = False,
    ):
        with time_block("WYJH Doubao Seedream 4.0 Img2Img"):
            if not image_url:
                raise ValueError("image_url is required")
            size_value = self.SIZE_CHOICES.get(size, size)
            payload: Dict[str, Any] = {
                "model": "doubao-seedream-4-0-250828",
                "prompt": prompt,
                "image": image_url,
                "size": size_value,
                "sequential_image_generation": "disabled",
                "stream": False,
                "response_format": "url",
                "watermark": watermark,
            }
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

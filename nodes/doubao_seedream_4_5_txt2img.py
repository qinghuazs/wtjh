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

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": ""}),
            },
            "optional": {
                "size": ("STRING", {"default": "2048x2048"}),
                "sequential_image_generation": ("STRING", {"default": "disabled"}),
                "stream": ("BOOLEAN", {"default": False}),
                "response_format": ("STRING", {"default": "url"}),
                "watermark": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate"
    CATEGORY = "WYJH/Text2Image"

    def generate(
        self,
        prompt: str,
        size: str = "2048x2048",
        sequential_image_generation: str = "disabled",
        stream: bool = False,
        response_format: str = "url",
        watermark: bool = True,
    ):
        with time_block("WYJH Doubao Seedream 4.5 Txt2Img"):
            payload: Dict[str, Any] = {
                "model": "doubao-seedream-4-5-251128",
                "prompt": prompt,
                "size": size,
                "sequential_image_generation": sequential_image_generation,
                "stream": stream,
                "response_format": response_format,
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

"""Qwen Image Max text-to-image node."""

from __future__ import annotations

from typing import Any, Dict

from .base import BaseWyjhNode
from ..config import get_ssl_verify
from ..utils.image_io import decode_base64_image, download_image, extract_image_value, pil_to_tensor
from ..utils.timing import time_block


class WyjhQwenImageMax(BaseWyjhNode):
    """Text-to-image node for qwen-image-max."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": "", "forceInput": True}),
            },
            "optional": {
                "size": ("STRING", {"default": "1328x1328"}),
                "n": ("INT", {"default": 1, "min": 1, "max": 1, "step": 1}),
                "watermark": ("BOOLEAN", {"default": False}),
                "prompt_extend": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate"
    CATEGORY = "WYJH/Text2Image"

    def generate(
        self,
        prompt: str,
        size: str = "1328x1328",
        n: int = 1,
        watermark: bool = False,
        prompt_extend: bool = True,
    ):
        with time_block("WYJH Qwen Image Max"):
            if n != 1:
                raise ValueError("qwen-image-max only supports n=1")
            payload: Dict[str, Any] = {
                "model": "qwen-image-max",
                "prompt": prompt,
                "size": size,
                "n": n,
                "watermark": watermark,
                "prompt_extend": prompt_extend,
            }
            response = self.call("/v1/images/generations", payload)
            value = extract_image_value(response)
            if isinstance(value, str) and value.startswith("http"):
                pil = download_image(value, verify=get_ssl_verify())
            else:
                pil = decode_base64_image(value)
            return (pil_to_tensor(pil),)

"""Qwen Image Max text-to-image node."""

from __future__ import annotations

from typing import Any, Dict

from ...base import BaseWyjhNode
from ....config import get_ssl_verify
from ....utils.image_io import decode_base64_image, download_image, extract_image_value, pil_to_tensor
from ....utils.timing import time_block


SIZE_CHOICES = {
    "16:9 (1664x928)": "1664x928",
    "4:3 (1472x1104)": "1472x1104",
    "1:1 (1328x1328)": "1328x1328",
    "3:4 (1104x1472)": "1104x1472",
    "9:16 (928x1664)": "928x1664",
}


class WyjhQwenImageMax(BaseWyjhNode):
    """Text-to-image node for qwen-image-max."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": "", "forceInput": True}),
            },
            "optional": {
                "size": (
                    list(SIZE_CHOICES.keys()),
                    {"default": "16:9 (1664x928)"},
                ),
                "watermark": ("BOOLEAN", {"default": False}),
                "prompt_extend": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate"
    CATEGORY = "WYJH/Text2Image"

    def generate(
        self,
        prompt: str,
        size: str = "16:9 (1664x928)",
        watermark: bool = False,
        prompt_extend: bool = False,
    ):
        with time_block("WYJH Qwen Image Max"):
            size_value = SIZE_CHOICES.get(size, size)
            payload: Dict[str, Any] = {
                "model": "qwen-image-max",
                "prompt": prompt,
                "size": size_value,
                "n": 1,
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

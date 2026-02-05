"""Z-Image-Turbo text-to-image node."""

from __future__ import annotations

from typing import Any, Dict

from .base import BaseWyjhNode
from ..config import get_ssl_verify
from ..utils.image_io import decode_base64_image, download_image, extract_image_value, pil_to_tensor
from ..utils.timing import time_block


class WyjhZImageTurbo(BaseWyjhNode):
    """Text-to-image node for z-image-turbo."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": "", "forceInput": True}),
            },
            "optional": {
                "size": ("STRING", {"default": "1024x1024"}),
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
        size: str = "1024x1024",
        watermark: bool = False,
        prompt_extend: bool = True,
    ):
        with time_block("WYJH Z-Image-Turbo"):
            payload: Dict[str, Any] = {
                "model": "z-image-turbo",
                "prompt": prompt,
                "size": size,
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

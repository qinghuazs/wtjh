"""Z-Image-Turbo text-to-image node."""

from __future__ import annotations

from typing import Any, Dict

from wyjh.nodes.base import BaseWyjhNode
from wyjh.config import get_ssl_verify
from wyjh.utils.image_io import decode_base64_image, download_image, extract_image_value, pil_to_tensor
from wyjh.utils.timing import time_block


SIZE_CHOICES = {
    "1:1 (1024x1024)": "1024x1024",
    "2:3 (832x1248)": "832x1248",
    "3:2 (1248x832)": "1248x832",
    "3:4 (864x1152)": "864x1152",
    "4:3 (1152x864)": "1152x864",
    "7:9 (896x1152)": "896x1152",
    "9:7 (1152x896)": "1152x896",
    "9:16 (720x1280)": "720x1280",
    "9:21 (576x1344)": "576x1344",
    "16:9 (1280x720)": "1280x720",
    "21:9 (1344x576)": "1344x576",
}


class WyjhZImageTurbo(BaseWyjhNode):
    """Text-to-image node for z-image-turbo."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": "", "forceInput": True}),
            },
            "optional": {
                "size": (list(SIZE_CHOICES.keys()), {"default": "1:1 (1024x1024)"}),
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
        size: str = "1:1 (1024x1024)",
        watermark: bool = False,
        prompt_extend: bool = True,
    ):
        with time_block("WYJH Z-Image-Turbo"):
            size_value = SIZE_CHOICES.get(size, size)
            payload: Dict[str, Any] = {
                "model": "z-image-turbo",
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

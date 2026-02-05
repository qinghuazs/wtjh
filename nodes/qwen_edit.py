"""Qwen image edit model node."""

from __future__ import annotations

from typing import Any, Dict

from .base import BaseWyjhNode
from ..config import get_ssl_verify
from ..utils.image_io import decode_base64_image, download_image, extract_image_value, pil_to_tensor
from ..utils.timing import time_block


class WyjhQwenImageEdit(BaseWyjhNode):
    """Image edit node for Qwen model."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": "", "forceInput": True}),
                "image_url": ("STRING", {"default": "", "forceInput": True}),
                "model_name": ("STRING", {"default": "qwen-image-edit-2509"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "edit"
    CATEGORY = "WYJH/ImageEdit"

    def edit(self, prompt: str, image_url: str, model_name: str):
        with time_block("WYJH Qwen Image Edit"):
            if not image_url:
                raise ValueError("image_url is required")
            payload: Dict[str, Any] = {
                "model": model_name,
                "prompt": prompt,
                "image": image_url,
            }
            response = self.call("/v1/images/generations", payload)
            value = extract_image_value(response)
            if isinstance(value, str) and value.startswith("http"):
                pil = download_image(value, verify=get_ssl_verify())
            else:
                pil = decode_base64_image(value)
            return (pil_to_tensor(pil),)

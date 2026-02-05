"""Doubao Seedream 4.5 image-to-image nodes."""

from __future__ import annotations

from typing import Any, Dict, List

from .base import BaseWyjhNode
from ..config import get_ssl_verify
from ..utils.image_io import decode_base64_image, download_image, extract_image_list, pil_to_tensor
from ..utils.timing import time_block


def _split_image_inputs(text: str) -> List[str]:
    value = (text or "").strip()
    if not value:
        return []
    if value.startswith("data:image"):
        return [value]
    if "\n" in value:
        return [part.strip() for part in value.splitlines() if part.strip()]
    if "||" in value:
        return [part.strip() for part in value.split("||") if part.strip()]
    if "," in value and value.startswith("http"):
        return [part.strip() for part in value.split(",") if part.strip()]
    return [value]


class WyjhDoubaoSeedream45Img2Img(BaseWyjhNode):
    """Single image input -> single image output."""

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
        size: str = "2048x2048 (1:1)",
        watermark: bool = False,
    ):
        with time_block("WYJH Doubao Seedream 4.5 Img2Img"):
            if not image_url:
                raise ValueError("image_url is required")
            size_value = self.SIZE_CHOICES.get(size, size)
            payload: Dict[str, Any] = {
                "model": "doubao-seedream-4-5-251128",
                "prompt": prompt,
                "image": [image_url],
                "size": size_value,
                "sequential_image_generation": "disabled",
                "stream": False,
                "response_format": "url",
                "watermark": watermark,
            }
            response = self.call("/v1/images/generations", payload)
            values = extract_image_list(response)
            value = values[0]
            if isinstance(value, str) and value.startswith("http"):
                pil = download_image(value, verify=get_ssl_verify())
            else:
                pil = decode_base64_image(value)
            return (pil_to_tensor(pil),)


class WyjhDoubaoSeedream45MultiFusion(BaseWyjhNode):
    """Multi image inputs -> single image output."""

    SIZE_CHOICES = {
        "1024x1024 (1:1)": "1024x1024",
        "2048x2048 (1:1)": "2048x2048",
        "2304x1728 (4:3)": "2304x1728",
        "2496x1664 (3:2)": "2496x1664",
        "2560x1440 (16:9)": "2560x1440",
        "3024x1296 (21:9)": "3024x1296",
    }
    INPUT_IS_LIST = ("image_urls",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": "", "forceInput": True}),
                "image_urls": ("STRING", {"default": "", "forceInput": True}),
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
        image_urls: str,
        size: str = "2048x2048 (1:1)",
        watermark: bool = False,
    ):
        with time_block("WYJH Doubao Seedream 4.5 Multi Fusion"):
            if isinstance(prompt, (list, tuple)):
                prompt = prompt[0] if prompt else ""
            images: List[str] = []
            if isinstance(image_urls, (list, tuple)):
                for item in image_urls:
                    if isinstance(item, str):
                        images.extend(_split_image_inputs(item))
            else:
                images = _split_image_inputs(image_urls)
            if not images:
                raise ValueError("image_urls is required")
            if isinstance(size, (list, tuple)):
                size = size[0] if size else "2048x2048 (1:1)"
            if isinstance(watermark, (list, tuple)):
                watermark = bool(watermark[0]) if watermark else False
            size_value = self.SIZE_CHOICES.get(size, size)
            payload: Dict[str, Any] = {
                "model": "doubao-seedream-4-5-251128",
                "prompt": prompt,
                "image": images,
                "size": size_value,
                "sequential_image_generation": "disabled",
                "stream": False,
                "response_format": "url",
                "watermark": watermark,
            }
            print("[WYJH] Doubao Seedream 4.5 Multi Fusion payload:", payload)
            response = self.call("/v1/images/generations", payload)
            print("[WYJH] Doubao Seedream 4.5 Multi Fusion response:", response)
            values = extract_image_list(response)
            value = values[0]
            if isinstance(value, str) and value.startswith("http"):
                pil = download_image(value, verify=get_ssl_verify())
            else:
                pil = decode_base64_image(value)
            return (pil_to_tensor(pil),)

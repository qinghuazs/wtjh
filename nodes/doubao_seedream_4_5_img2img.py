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

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": ""}),
                "image_url": ("STRING", {"default": "", "forceInput": True}),
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
    CATEGORY = "WYJH/Image2Image"

    def generate(
        self,
        prompt: str,
        image_url: str,
        size: str = "2048x2048",
        sequential_image_generation: str = "disabled",
        stream: bool = False,
        response_format: str = "url",
        watermark: bool = True,
    ):
        with time_block("WYJH Doubao Seedream 4.5 Img2Img"):
            if not image_url:
                raise ValueError("image_url is required")
            payload: Dict[str, Any] = {
                "model": "doubao-seedream-4-5-251128",
                "prompt": prompt,
                "image": [image_url],
                "size": size,
                "sequential_image_generation": sequential_image_generation,
                "stream": stream,
                "response_format": response_format,
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
    INPUT_IS_LIST = ("image_urls",)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": ""}),
                "image_urls": ("STRING", {"default": "", "forceInput": True}),
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
    CATEGORY = "WYJH/Image2Image"

    def generate(
        self,
        prompt: str,
        image_urls: str,
        size: str = "2048x2048",
        sequential_image_generation: str = "disabled",
        stream: bool = False,
        response_format: str = "url",
        watermark: bool = True,
    ):
        with time_block("WYJH Doubao Seedream 4.5 Multi Fusion"):
            images: List[str] = []
            if isinstance(image_urls, (list, tuple)):
                for item in image_urls:
                    if isinstance(item, str):
                        images.extend(_split_image_inputs(item))
            else:
                images = _split_image_inputs(image_urls)
            if not images:
                raise ValueError("image_urls is required")
            payload: Dict[str, Any] = {
                "model": "doubao-seedream-4-5-251128",
                "prompt": prompt,
                "image": images,
                "size": size,
                "sequential_image_generation": sequential_image_generation,
                "stream": stream,
                "response_format": response_format,
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

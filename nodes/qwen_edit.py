"""Qwen image edit model node."""

from __future__ import annotations

import base64
import io
from typing import Any, Dict

import requests

from .base import BaseWyjhNode
from ..config import get_ssl_verify
from ..utils.timing import time_block


def _download_image(url: str) -> "Image.Image":
    from PIL import Image

    resp = requests.get(url, timeout=60, verify=get_ssl_verify())
    resp.raise_for_status()
    return Image.open(io.BytesIO(resp.content)).convert("RGB")


def _decode_base64_image(data: str) -> "Image.Image":
    from PIL import Image

    if data.startswith("data:image"):
        data = data.split(",", 1)[-1]
    raw = base64.b64decode(data)
    return Image.open(io.BytesIO(raw)).convert("RGB")


def _pil_to_tensor(image: "Image.Image"):
    import numpy as np
    import torch

    arr = np.array(image).astype("float32") / 255.0
    if arr.ndim == 2:
        arr = np.stack([arr, arr, arr], axis=-1)
    return torch.from_numpy(arr)[None,]


def _extract_image_value(payload: Dict[str, Any]) -> str:
    if isinstance(payload, dict):
        if "data" in payload and isinstance(payload["data"], list) and payload["data"]:
            item = payload["data"][0]
            if isinstance(item, dict):
                for key in ("url", "image_url", "image", "output", "result", "b64_json"):
                    if key in item:
                        return item[key]
        for key in ("url", "image_url", "image", "output", "result", "b64_json"):
            if key in payload:
                return payload[key]
    raise RuntimeError("Unrecognized image response format")


class WyjhQwenImageEdit(BaseWyjhNode):
    """Image edit node for Qwen model."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": ""}),
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
            value = _extract_image_value(response)
            if isinstance(value, str) and value.startswith("http"):
                pil = _download_image(value)
            else:
                pil = _decode_base64_image(value)
            return (_pil_to_tensor(pil),)

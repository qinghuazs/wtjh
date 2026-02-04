"""Image upload node for imageproxy."""

from __future__ import annotations

import io
from typing import Tuple

import requests

from ..config import get_image_upload_url, get_timeout
from ..utils.image import tensor_to_pil


class WyjhImageUpload:
    """Upload ComfyUI IMAGE to imageproxy and return URL."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            },
            "optional": {
                "filename": ("STRING", {"default": "upload.png"}),
                "upload_url": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("url",)
    FUNCTION = "upload"
    CATEGORY = "WYJH/Utils"

    def upload(self, image, filename: str = "upload.png", upload_url: str = "") -> Tuple[str]:
        pil = tensor_to_pil(image)
        buffer = io.BytesIO()
        pil.save(buffer, format="PNG")
        buffer.seek(0)

        url = upload_url.strip() or get_image_upload_url()
        files = {"file": (filename or "upload.png", buffer, "image/png")}
        response = requests.post(url, files=files, timeout=get_timeout())
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, dict) or "url" not in data:
            raise RuntimeError("Upload response missing url")
        return (data["url"],)

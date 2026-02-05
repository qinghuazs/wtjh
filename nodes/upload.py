"""Image upload node for imageproxy."""

from __future__ import annotations

import io
import os
from typing import Tuple

import requests
import folder_paths
from time import perf_counter

from ..config import get_image_upload_url, get_ssl_verify, get_timeout
from ..utils.image import tensor_to_pil
from ..utils.timing import time_block


class WyjhImageUpload:
    """Upload ComfyUI IMAGE tensor to imageproxy and return URL."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("url",)
    FUNCTION = "upload"
    CATEGORY = "WYJH/Utils"

    def upload(self, image) -> Tuple[str]:
        with time_block("WYJH Image Upload"):
            pil = tensor_to_pil(image)
            buffer = io.BytesIO()
            pil.save(buffer, format="PNG")
            buffer.seek(0)

            url = get_image_upload_url()
            print(f"[WYJH] HTTP POST {url}")
            files = {"file": ("upload.png", buffer, "image/png")}
            start = perf_counter()
            response = requests.post(
                url,
                files=files,
                timeout=get_timeout(),
                verify=get_ssl_verify(),
            )
            elapsed = perf_counter() - start
            print(f"[WYJH] response status: {response.status_code} ({elapsed:.3f}s)")
            response.raise_for_status()
            data = response.json()
            print(f"[WYJH] response body: {data}")
            if not isinstance(data, dict) or "url" not in data:
                raise RuntimeError("Upload response missing url")
            return (data["url"],)


class WyjhLocalImageUpload:
    """Select local image from ComfyUI input folder and upload to imageproxy."""

    @classmethod
    def INPUT_TYPES(cls):
        input_dir = folder_paths.get_input_directory()
        files = []
        if os.path.isdir(input_dir):
            for f in os.listdir(input_dir):
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp')):
                    files.append(f)
        return {
            "required": {
                "image": (sorted(files) if files else [""], {"image_upload": True}),
            },
        }

    RETURN_TYPES = ("STRING", "IMAGE")
    RETURN_NAMES = ("url", "image")
    FUNCTION = "upload"
    CATEGORY = "WYJH/Utils"

    def upload(self, image: str) -> Tuple[str, any]:
        from PIL import Image
        import numpy as np
        import torch

        with time_block("WYJH Local Image Upload"):
            image_path = folder_paths.get_annotated_filepath(image)
            pil = Image.open(image_path).convert("RGB")
            filename = os.path.basename(image_path)

            # Upload to imageproxy
            buffer = io.BytesIO()
            pil.save(buffer, format="PNG")
            buffer.seek(0)

            url = get_image_upload_url()
            print(f"[WYJH] HTTP POST {url}")
            files = {"file": (filename or "upload.png", buffer, "image/png")}
            start = perf_counter()
            response = requests.post(
                url,
                files=files,
                timeout=get_timeout(),
                verify=get_ssl_verify(),
            )
            elapsed = perf_counter() - start
            print(f"[WYJH] response status: {response.status_code} ({elapsed:.3f}s)")
            response.raise_for_status()
            data = response.json()
            print(f"[WYJH] response body: {data}")
            if not isinstance(data, dict) or "url" not in data:
                raise RuntimeError("Upload response missing url")

            # Convert to tensor for output
            arr = np.array(pil).astype(np.float32) / 255.0
            tensor = torch.from_numpy(arr)[None, ...]  # Add batch dimension

            return (data["url"], tensor)

    @classmethod
    def IS_CHANGED(cls, image):
        image_path = folder_paths.get_annotated_filepath(image)
        return os.path.getmtime(image_path)

    @classmethod
    def VALIDATE_INPUTS(cls, image):
        if not folder_paths.exists_annotated_filepath(image):
            return f"Invalid image file: {image}"
        return True

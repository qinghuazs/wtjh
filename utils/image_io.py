"""Image IO helpers for API responses."""

from __future__ import annotations

import base64
import io
from typing import Any, Dict

import requests
from time import perf_counter


def extract_image_value(payload: Dict[str, Any]) -> str:
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


def extract_image_list(payload: Dict[str, Any]) -> list[str]:
    values: list[str] = []
    if isinstance(payload, dict):
        if "data" in payload and isinstance(payload["data"], list) and payload["data"]:
            for item in payload["data"]:
                if isinstance(item, dict):
                    for key in ("url", "image_url", "image", "output", "result", "b64_json"):
                        if key in item and item[key]:
                            values.append(item[key])
                            break
        if not values:
            for key in ("url", "image_url", "image", "output", "result", "b64_json"):
                if key in payload and payload[key]:
                    values.append(payload[key])
                    break
    if not values:
        raise RuntimeError("Unrecognized image response format")
    return values


def download_image(url: str, *, timeout: int = 60, verify: bool = True) -> "Image.Image":
    from PIL import Image

    print(f"[WYJH] HTTP GET {url}")
    start = perf_counter()
    resp = requests.get(url, timeout=timeout, verify=verify)
    elapsed = perf_counter() - start
    print(f"[WYJH] response status: {resp.status_code} ({elapsed:.3f}s)")
    resp.raise_for_status()
    return Image.open(io.BytesIO(resp.content)).convert("RGB")


def decode_base64_image(data: str) -> "Image.Image":
    from PIL import Image

    if data.startswith("data:image"):
        data = data.split(",", 1)[-1]
    raw = base64.b64decode(data)
    return Image.open(io.BytesIO(raw)).convert("RGB")


def pil_to_tensor(image: "Image.Image"):
    import numpy as np
    import torch

    arr = np.array(image).astype("float32") / 255.0
    if arr.ndim == 2:
        arr = np.stack([arr, arr, arr], axis=-1)
    return torch.from_numpy(arr)[None,]

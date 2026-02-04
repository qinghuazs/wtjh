"""Gemini 3 Pro image preview generation node."""

from __future__ import annotations

from typing import Any, Dict

from .base import BaseWyjhNode
from ..utils.image_io import decode_base64_image, pil_to_tensor
from ..utils.timing import time_block


def _extract_inline_image_data(payload: Dict[str, Any]) -> str:
    if not isinstance(payload, dict):
        raise RuntimeError("Invalid response format")
    candidates = payload.get("candidates", [])
    if isinstance(candidates, list):
        for candidate in candidates:
            if not isinstance(candidate, dict):
                continue
            content = candidate.get("content", {})
            parts = content.get("parts", []) if isinstance(content, dict) else []
            if isinstance(parts, list):
                for part in parts:
                    if not isinstance(part, dict):
                        continue
                    inline = part.get("inline_data") or part.get("inlineData")
                    if isinstance(inline, dict):
                        data = inline.get("data")
                        if data:
                            return data
    raise RuntimeError("No image data found in response")


class WyjhGemini3ProImagePreview(BaseWyjhNode):
    """Text-to-image node for gemini-3-pro-image-preview."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": ""}),
            },
            "optional": {
                "aspect_ratio": ("STRING", {"default": "1:1"}),
                "image_quality": ("STRING", {"default": "HIGH"}),
                "use_query_key": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate"
    CATEGORY = "WYJH/Text2Image"

    def generate(self, prompt: str, aspect_ratio: str = "1:1", image_quality: str = "HIGH", use_query_key: bool = True):
        with time_block("WYJH Gemini 3 Pro Image Preview"):
            payload: Dict[str, Any] = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [
                            {"text": prompt},
                        ],
                    }
                ],
                "generationConfig": {},
                "responseModalities": ["IMAGE"],
                "imageConfig": {
                    "aspectRatio": aspect_ratio,
                    "imageQuality": image_quality,
                },
            }

            params = {"key": self.client.api_key} if use_query_key and self.client.api_key else None
            response = self.client.post(
                "/v1beta/models/gemini-3-pro-image-preview:generateContent",
                json=payload,
                params=params,
            )
            data = _extract_inline_image_data(response)
            pil = decode_base64_image(data)
            return (pil_to_tensor(pil),)

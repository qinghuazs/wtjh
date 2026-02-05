"""Gemini 2.5 Flash image generation node (basic)."""

from __future__ import annotations

from typing import Any, Dict

from .base import BaseWyjhNode
from ..utils.image_io import decode_base64_image, pil_to_tensor
from ..utils.timing import time_block
from .gemini_3_pro_image_preview import _extract_inline_image_data


class WyjhGemini25FlashImageBasic(BaseWyjhNode):
    """Text-to-image node for gemini-2.5-flash-image (no aspect controls)."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": "", "forceInput": True}),
            },
            "optional": {
                "use_query_key": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate"
    CATEGORY = "WYJH/Text2Image"

    def generate(self, prompt: str, use_query_key: bool = True):
        with time_block("WYJH Gemini 2.5 Flash Image Basic"):
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
            }

            params = {"key": self.client.api_key} if use_query_key and self.client.api_key else None
            response = self.client.post(
                "/v1beta/models/gemini-2.5-flash-image:generateContent",
                json=payload,
                params=params,
            )
            data = _extract_inline_image_data(response)
            pil = decode_base64_image(data)
            return (pil_to_tensor(pil),)

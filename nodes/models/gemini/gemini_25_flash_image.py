"""Gemini 2.5 Flash image generation node."""

from __future__ import annotations

from typing import Any, Dict

from wyjh.nodes.base import BaseWyjhNode
from wyjh.utils.image_io import decode_base64_image, pil_to_tensor
from wyjh.utils.timing import time_block
from .gemini_3_pro_image_preview import _extract_inline_image_data


class WyjhGemini25FlashImage(BaseWyjhNode):
    """Text-to-image node for gemini-2.5-flash-image."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": "", "forceInput": True}),
            },
            "optional": {
                "aspect_ratio": ("STRING", {"default": "1:1"}),
                "use_query_key": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate"
    CATEGORY = "WYJH/Text2Image"

    def generate(self, prompt: str, aspect_ratio: str = "1:1", use_query_key: bool = True):
        with time_block("WYJH Gemini 2.5 Flash Image"):
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
                },
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

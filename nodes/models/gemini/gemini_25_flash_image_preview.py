"""Gemini 2.5 Flash image preview generation node."""

from __future__ import annotations

from typing import Any, Dict

from ...base import BaseWyjhNode
from ....utils.image_io import decode_base64_image, pil_to_tensor
from ....utils.timing import time_block
from .gemini_3_pro_image_preview import _extract_inline_image_data


class WyjhGemini25FlashImagePreview(BaseWyjhNode):
    """Text-to-image node for gemini-2.5-flash-image-preview."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": "", "forceInput": True}),
            },
            "optional": {
                "use_query_key": ("BOOLEAN", {"default": True}),
                "include_text": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate"
    CATEGORY = "WYJH/Text2Image"

    def generate(self, prompt: str, use_query_key: bool = True, include_text: bool = False):
        with time_block("WYJH Gemini 2.5 Flash Image Preview"):
            response_modalities = ["IMAGE"]
            if include_text:
                response_modalities = ["TEXT", "IMAGE"]

            payload: Dict[str, Any] = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [
                            {"text": prompt},
                        ],
                    }
                ],
                "generationConfig": {
                    "responseModalities": response_modalities,
                },
            }

            params = {"key": self.client.api_key} if use_query_key and self.client.api_key else None
            response = self.client.post(
                "/v1beta/models/gemini-2.5-flash-image-preview:generateContent",
                json=payload,
                params=params,
            )
            data = _extract_inline_image_data(response)
            pil = decode_base64_image(data)
            return (pil_to_tensor(pil),)

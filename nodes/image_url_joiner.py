"""Join multiple image URLs in a fixed order."""

from __future__ import annotations

from typing import Tuple

from ..utils.timing import time_block


class WyjhImageUrlJoiner:
    """Join multiple image URL inputs into a single ordered string."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_url_1": ("STRING", {"default": "", "forceInput": True}),
            },
            "optional": {
                "image_url_2": ("STRING", {"default": "", "forceInput": True}),
                "image_url_3": ("STRING", {"default": "", "forceInput": True}),
                "image_url_4": ("STRING", {"default": "", "forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("image_urls",)
    FUNCTION = "join"
    CATEGORY = "WYJH/Utils"

    def join(
        self,
        image_url_1: str,
        image_url_2: str = "",
        image_url_3: str = "",
        image_url_4: str = "",
    ) -> Tuple[str]:
        with time_block("WYJH Image URL Joiner"):
            values = [image_url_1, image_url_2, image_url_3, image_url_4]
            ordered = [v.strip() for v in values if isinstance(v, str) and v.strip()]
            return ("\n".join(ordered),)

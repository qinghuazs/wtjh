"""Simple text input node."""

from __future__ import annotations

from typing import Tuple

from ...utils.timing import time_block


class WyjhTextInput:
    """User text input node."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "execute"
    CATEGORY = "WYJH/Utils"

    def execute(self, text: str) -> Tuple[str]:
        with time_block("WYJH Text Input"):
            return (text,)

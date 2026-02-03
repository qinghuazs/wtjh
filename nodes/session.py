"""Session/chat models."""

from __future__ import annotations

from typing import Dict, Any

from .base import BaseWyjhNode


class WyjhSessionChat(BaseWyjhNode):
    """Chat node for session models."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": ""}),
                "model_name": ("STRING", {"default": ""}),
            },
            "optional": {
                "session_id": ("STRING", {"default": ""}),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 2.0, "step": 0.05}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("reply", "session_id")
    FUNCTION = "chat"
    CATEGORY = "WYJH/Session"

    def chat(self, prompt: str, model_name: str, session_id: str = "", temperature: float = 0.7):
        payload: Dict[str, Any] = {
            "prompt": prompt,
            "model": model_name,
            "session_id": session_id or None,
            "temperature": temperature,
        }
        # TODO: replace with real endpoint path
        raise RuntimeError("WYJH session chat not implemented yet")

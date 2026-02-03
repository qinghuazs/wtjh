"""Video models."""

from __future__ import annotations

from typing import Dict, Any

from .base import BaseWyjhNode


class WyjhVideoGenerate(BaseWyjhNode):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": ""}),
                "model_name": ("STRING", {"default": ""}),
                "duration": ("FLOAT", {"default": 3.0, "min": 1.0, "max": 60.0, "step": 0.5}),
                "fps": ("INT", {"default": 24, "min": 1, "max": 120, "step": 1}),
            },
            "optional": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 2**31 - 1, "step": 1}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_url",)
    FUNCTION = "generate"
    CATEGORY = "WYJH/Video"

    def generate(self, prompt: str, model_name: str, duration: float, fps: int, seed: int = 0):
        payload: Dict[str, Any] = {
            "prompt": prompt,
            "model": model_name,
            "duration": duration,
            "fps": fps,
            "seed": seed,
        }
        # TODO: replace with real endpoint path
        raise RuntimeError("WYJH video generation not implemented yet")

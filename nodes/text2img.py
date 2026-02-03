"""Text-to-image models."""

from __future__ import annotations

from typing import Dict, Any

from .base import BaseWyjhNode


class WyjhText2Image(BaseWyjhNode):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": ""}),
                "model_name": ("STRING", {"default": ""}),
                "width": ("INT", {"default": 512, "min": 64, "max": 4096, "step": 64}),
                "height": ("INT", {"default": 512, "min": 64, "max": 4096, "step": 64}),
            },
            "optional": {
                "negative_prompt": ("STRING", {"multiline": True, "default": ""}),
                "steps": ("INT", {"default": 20, "min": 1, "max": 200, "step": 1}),
                "cfg_scale": ("FLOAT", {"default": 7.0, "min": 0.0, "max": 30.0, "step": 0.5}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 2**31 - 1, "step": 1}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "generate"
    CATEGORY = "WYJH/Text2Image"

    def generate(
        self,
        prompt: str,
        model_name: str,
        width: int,
        height: int,
        negative_prompt: str = "",
        steps: int = 20,
        cfg_scale: float = 7.0,
        seed: int = 0,
    ):
        payload: Dict[str, Any] = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "model": model_name,
            "width": width,
            "height": height,
            "steps": steps,
            "cfg_scale": cfg_scale,
            "seed": seed,
        }
        # TODO: replace with real endpoint path + image decode
        raise RuntimeError("WYJH text-to-image not implemented yet")

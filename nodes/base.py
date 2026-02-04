"""Shared node helpers."""

from __future__ import annotations

from typing import Any, Dict

from ..api import WyjhApiClient


class BaseWyjhNode:
    CATEGORY = "WYJH"

    def __init__(self):
        self.client = WyjhApiClient()

    def call(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self.client.api_key:
            raise RuntimeError(
                "WYJH_API_KEY not set. Add it to .env or environment variables."
            )
        return self.client.post(path, json=payload)

    def get(self, path: str) -> Dict[str, Any]:
        if not self.client.api_key:
            raise RuntimeError(
                "WYJH_API_KEY not set. Add it to .env or environment variables."
            )
        return self.client.get(path)

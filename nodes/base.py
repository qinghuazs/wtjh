"""Shared node helpers."""

from __future__ import annotations

from typing import Any, Dict

from ..api import WyjhApiClient


class BaseWyjhNode:
    CATEGORY = "WYJH"

    def __init__(self):
        self.client = WyjhApiClient()

    def call(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self.client.post(path, json=payload)

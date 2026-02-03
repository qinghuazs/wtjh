"""HTTP client for Wyjh API."""

from __future__ import annotations

from typing import Any, Dict, Optional

import requests

from ..config import get_base_url, get_timeout


class WyjhApiClient:
    def __init__(self, base_url: Optional[str] = None, timeout: Optional[int] = None):
        self.base_url = (base_url or get_base_url()).rstrip("/")
        self.timeout = timeout or get_timeout()

    def _url(self, path: str) -> str:
        path = path.lstrip("/")
        return f"{self.base_url}/{path}"

    def post(self, path: str, json: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(self._url(path), json=json, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        response = requests.get(self._url(path), params=params or {}, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

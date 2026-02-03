"""HTTP client for Wyjh API."""

from __future__ import annotations

from typing import Any, Dict, Optional

import requests

from ..config import get_api_key, get_base_url, get_timeout


class WyjhApiClient:
    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
        api_key: Optional[str] = None,
    ):
        self.base_url = (base_url or get_base_url()).rstrip("/")
        self.timeout = timeout or get_timeout()
        self.api_key = api_key if api_key is not None else get_api_key()

    def _url(self, path: str) -> str:
        path = path.lstrip("/")
        return f"{self.base_url}/{path}"

    def _headers(self, extra: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        headers: Dict[str, str] = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        if extra:
            headers.update(extra)
        return headers

    def post(
        self,
        path: str,
        json: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        response = requests.post(
            self._url(path),
            json=json,
            headers=self._headers(headers),
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        response = requests.get(
            self._url(path),
            params=params or {},
            headers=self._headers(headers),
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

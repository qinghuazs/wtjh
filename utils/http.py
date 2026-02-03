"""HTTP helpers."""

from __future__ import annotations

from typing import Any, Dict, Optional

import requests

from .errors import WyjhError


def request_json(method: str, url: str, *, json: Optional[Dict[str, Any]] = None, timeout: int = 60) -> Dict[str, Any]:
    try:
        response = requests.request(method, url, json=json, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise WyjhError(f"Request failed: {exc}") from exc

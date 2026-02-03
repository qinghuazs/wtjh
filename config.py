"""Global configuration for Wyjh ComfyUI custom nodes."""

import os

DEFAULT_BASE_URL = "https://www.wyjh.top"
DEFAULT_TIMEOUT = 60


def get_base_url() -> str:
    """Get base URL from env or default."""
    return os.getenv("WYJH_BASE_URL", DEFAULT_BASE_URL).rstrip("/")


def get_timeout() -> int:
    """Get request timeout from env or default."""
    value = os.getenv("WYJH_TIMEOUT", "")
    try:
        return int(value)
    except ValueError:
        return DEFAULT_TIMEOUT


def get_api_key() -> str:
    """Get API key from env (optional)."""
    return os.getenv("WYJH_API_KEY", "")

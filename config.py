"""Global configuration for Wyjh ComfyUI custom nodes."""

import os

DEFAULT_BASE_URL = "https://www.wyjh.top"
DEFAULT_TIMEOUT = 60
DEFAULT_IMAGE_UPLOAD_URL = "https://imageproxy.zhongzhuan.chat/api/upload"


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


def get_image_upload_url() -> str:
    """Get image upload URL from env or default."""
    return os.getenv("WYJH_IMAGE_UPLOAD_URL", DEFAULT_IMAGE_UPLOAD_URL).rstrip("/")

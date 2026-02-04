"""Global configuration for Wyjh ComfyUI custom nodes."""

import os

_DOTENV_LOADED = False


def _load_dotenv(path: str = ".env") -> None:
    """Lightweight .env loader without external deps."""
    global _DOTENV_LOADED
    if _DOTENV_LOADED:
        return
    _DOTENV_LOADED = True
    if not os.path.exists(path):
        return
    try:
        with open(path, "r", encoding="utf-8") as handle:
            for raw_line in handle:
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip("'").strip('"')
                if key and key not in os.environ:
                    os.environ[key] = value
    except OSError:
        # Ignore .env read errors to avoid breaking runtime.
        return

DEFAULT_BASE_URL = "https://www.wyjh.top"
DEFAULT_TIMEOUT = 60
DEFAULT_IMAGE_UPLOAD_URL = "https://imageproxy.zhongzhuan.chat/api/upload"


def get_base_url() -> str:
    """Get base URL from env or default."""
    _load_dotenv()
    return os.getenv("WYJH_BASE_URL", DEFAULT_BASE_URL).rstrip("/")


def get_timeout() -> int:
    """Get request timeout from env or default."""
    _load_dotenv()
    value = os.getenv("WYJH_TIMEOUT", "")
    try:
        return int(value)
    except ValueError:
        return DEFAULT_TIMEOUT


def get_api_key() -> str:
    """Get API key from env (optional)."""
    _load_dotenv()
    return os.getenv("WYJH_API_KEY", "")


def get_image_upload_url() -> str:
    """Get image upload URL from env or default."""
    _load_dotenv()
    return os.getenv("WYJH_IMAGE_UPLOAD_URL", DEFAULT_IMAGE_UPLOAD_URL).rstrip("/")

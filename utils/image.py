"""Image conversion helpers (placeholders)."""

from __future__ import annotations

from typing import Any

try:
    import numpy as np
    from PIL import Image
except Exception:  # pragma: no cover - optional imports for runtime
    np = None
    Image = None


def pil_to_tensor(image: "Image.Image") -> Any:
    """Convert PIL image to ComfyUI tensor (placeholder)."""
    if np is None:
        raise RuntimeError("numpy/PIL not available")
    arr = np.array(image).astype("float32") / 255.0
    # ComfyUI uses torch tensors; leave conversion to caller for now.
    return arr


def tensor_to_pil(tensor: Any) -> "Image.Image":
    """Convert tensor/ndarray to PIL image (placeholder)."""
    if Image is None:
        raise RuntimeError("PIL not available")
    if hasattr(tensor, "detach"):
        tensor = tensor.detach().cpu().numpy()
    arr = (tensor * 255.0).clip(0, 255).astype("uint8")
    if arr.ndim == 4:
        arr = arr[0]
    return Image.fromarray(arr)

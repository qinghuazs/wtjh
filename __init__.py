"""ComfyUI custom nodes for WYJH."""

from __future__ import annotations

import os
import sys

# Ensure the package is importable as `wyjh` even when loaded via a file path.
_pkg_dir = os.path.dirname(__file__)
_parent_dir = os.path.dirname(_pkg_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)
if __name__ != "wyjh":
    sys.modules.setdefault("wyjh", sys.modules[__name__])

from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

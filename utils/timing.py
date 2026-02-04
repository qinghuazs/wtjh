"""Timing utilities for node execution."""

from __future__ import annotations

from contextlib import contextmanager
from time import perf_counter
from typing import Iterator


@contextmanager
def time_block(label: str) -> Iterator[None]:
    start = perf_counter()
    try:
        yield
    finally:
        end = perf_counter()
        duration = end - start
        print(f"[WYJH] {label} took {duration:.3f}s")

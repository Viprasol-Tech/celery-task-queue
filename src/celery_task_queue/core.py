"""Part of Celery Task Queue by Viprasol Tech Private Limited (https://viprasol.com).

Pure task logic. Every Celery task in :mod:`celery_task_queue.tasks` is a thin
wrapper around a function defined here. Keeping the logic pure means the test
suite can exercise it directly, with no broker, worker, or Redis involved.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Sequence


class TaskInputError(ValueError):
    """Raised when task input fails validation."""


def add(x: float, y: float) -> float:
    """Return the sum of two numbers."""
    return x + y


def multiply(numbers: Sequence[float]) -> float:
    """Return the product of a sequence of numbers.

    Raises:
        TaskInputError: if ``numbers`` is empty.
    """
    if not numbers:
        raise TaskInputError("multiply() requires at least one number")
    product = 1.0
    for n in numbers:
        product *= n
    return product


def double(x: float) -> float:
    """Return ``x`` multiplied by two (handy as a chain step)."""
    return x * 2


def normalize_text(text: str) -> str:
    """Collapse whitespace and lower-case ``text`` for stable processing."""
    return " ".join(text.split()).lower()


def word_count(text: str) -> dict[str, int]:
    """Return a word-frequency map for ``text`` after normalisation."""
    counts: dict[str, int] = {}
    for word in normalize_text(text).split():
        counts[word] = counts.get(word, 0) + 1
    return counts


def chunk(items: Sequence[int], size: int) -> list[list[int]]:
    """Split ``items`` into consecutive chunks of at most ``size`` elements.

    Raises:
        TaskInputError: if ``size`` is not a positive integer.
    """
    if size <= 0:
        raise TaskInputError("chunk size must be a positive integer")
    return [list(items[i : i + size]) for i in range(0, len(items), size)]


def summarize_numbers(numbers: Iterable[float]) -> dict[str, float]:
    """Compute count, sum, mean, min and max for ``numbers``.

    Raises:
        TaskInputError: if ``numbers`` is empty.
    """
    values = list(numbers)
    if not values:
        raise TaskInputError("summarize_numbers() requires at least one value")
    total = math.fsum(values)
    return {
        "count": float(len(values)),
        "sum": total,
        "mean": total / len(values),
        "min": min(values),
        "max": max(values),
    }


def compute_backoff(retries: int, base: float = 1.0, cap: float = 600.0) -> float:
    """Exponential backoff (in seconds) for a given retry attempt.

    The value is ``base * 2 ** retries`` clamped to ``cap``. Useful for the
    ``retry`` countdown of a flaky task.

    Raises:
        TaskInputError: if ``retries`` is negative.
    """
    if retries < 0:
        raise TaskInputError("retries must be >= 0")
    return min(base * (2.0**retries), cap)


def safe_divide(numerator: float, denominator: float) -> float:
    """Divide two numbers, raising a clear error on division by zero.

    Mirrors the kind of transient/permanent failure a real task must classify
    before deciding whether to retry.

    Raises:
        TaskInputError: if ``denominator`` is zero.
    """
    if denominator == 0:
        raise TaskInputError("cannot divide by zero")
    return numerator / denominator

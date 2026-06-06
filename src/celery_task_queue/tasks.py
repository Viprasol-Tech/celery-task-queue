"""Part of Celery Task Queue by Viprasol Tech Private Limited (https://viprasol.com).

Celery task definitions. Each task is intentionally thin: it validates/forwards
to a pure function in :mod:`celery_task_queue.core`. This keeps the business
logic fully unit-testable offline while the tasks add the Celery concerns
(retries, rate limits, queues, workflows).
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from celery import shared_task
from celery.utils.log import get_task_logger

from celery_task_queue import core

logger = get_task_logger(__name__)


@shared_task(name="ctq.add")
def add_task(x: float, y: float) -> float:
    """Add two numbers (thin wrapper over :func:`core.add`)."""
    return core.add(x, y)


@shared_task(name="ctq.multiply")
def multiply_task(numbers: Sequence[float]) -> float:
    """Multiply a sequence of numbers."""
    return core.multiply(numbers)


@shared_task(name="ctq.double")
def double_task(x: float) -> float:
    """Double a single number — composes cleanly in a chain."""
    return core.double(x)


@shared_task(name="ctq.word_count", rate_limit="100/m")
def word_count_task(text: str) -> dict[str, int]:
    """Count words in ``text``, rate-limited to 100 calls/minute per worker."""
    return core.word_count(text)


@shared_task(name="ctq.summarize")
def summarize_task(numbers: Sequence[float]) -> dict[str, float]:
    """Summarise a list of numbers (count/sum/mean/min/max)."""
    return core.summarize_numbers(numbers)


@shared_task(
    name="ctq.divide",
    bind=True,
    max_retries=3,
    default_retry_delay=2,
    autoretry_for=(core.TaskInputError,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
)
def divide_task(self: Any, numerator: float, denominator: float) -> float:
    """Divide two numbers with automatic exponential-backoff retries.

    Demonstrates the retry pattern: the pure function raises a typed error,
    and Celery retries with backoff. The backoff schedule itself is computed
    by :func:`core.compute_backoff`, which is unit-tested offline.
    """
    logger.info("divide_task attempt %s", self.request.retries)
    return core.safe_divide(numerator, denominator)


@shared_task(name="ctq.reduce_sum")
def reduce_sum_task(values: Sequence[float]) -> float:
    """Sum a list of values — used as the callback in a chord/group workflow."""
    return float(core.summarize_numbers(values)["sum"]) if values else 0.0

"""Part of Celery Task Queue by Viprasol Tech Private Limited (https://viprasol.com).

Canvas workflow builders: chains, groups and chords assembled from the tasks in
:mod:`celery_task_queue.tasks`. These return Celery *signatures*, so they can be
constructed and inspected offline (and executed eagerly in tests).
"""

from __future__ import annotations

from collections.abc import Sequence

from celery import chain, chord, group
from celery.canvas import Signature

from celery_task_queue.tasks import (
    add_task,
    double_task,
    multiply_task,
    reduce_sum_task,
)


def add_then_double(x: float, y: float) -> Signature:
    """Chain: ``add(x, y)`` then double the result."""
    return chain(add_task.s(x, y), double_task.s())


def parallel_products(pairs: Sequence[tuple[float, float]]) -> Signature:
    """Group: multiply each pair in parallel, returning a list of products."""
    return group(multiply_task.s([a, b]) for a, b in pairs)


def sum_of_products(pairs: Sequence[tuple[float, float]]) -> Signature:
    """Chord: multiply each pair in parallel, then sum all products."""
    header = group(multiply_task.s([a, b]) for a, b in pairs)
    return chord(header, reduce_sum_task.s())

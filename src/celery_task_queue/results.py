"""Part of Celery Task Queue by Viprasol Tech Private Limited (https://viprasol.com).

A small helper for retrieving task results, with a polite timeout and a typed
status snapshot so callers don't have to wrangle Celery's ``AsyncResult`` API
directly.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from celery.result import AsyncResult


@dataclass(frozen=True, slots=True)
class ResultSnapshot:
    """A point-in-time view of a task's state and value."""

    task_id: str
    status: str
    ready: bool
    successful: bool
    value: Any


def snapshot(result: AsyncResult) -> ResultSnapshot:
    """Capture the current state of an ``AsyncResult`` without blocking."""
    ready = bool(result.ready())
    return ResultSnapshot(
        task_id=result.id,
        status=str(result.status),
        ready=ready,
        successful=bool(result.successful()) if ready else False,
        value=result.result if ready else None,
    )


def wait_for(result: AsyncResult, timeout: float = 10.0) -> Any:
    """Block until ``result`` is ready (or ``timeout`` seconds elapse).

    Args:
        result: The Celery ``AsyncResult`` to wait on.
        timeout: Maximum seconds to wait before raising.

    Returns:
        The task's return value.
    """
    return result.get(timeout=timeout)

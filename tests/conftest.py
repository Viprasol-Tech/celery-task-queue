"""Shared pytest fixtures — force Celery into eager (offline) mode."""

from __future__ import annotations

import os

import pytest

# Set BEFORE importing the app so create_app() picks up eager mode.
os.environ.setdefault("CELERY_TASK_ALWAYS_EAGER", "true")
os.environ.setdefault("CELERY_BROKER_URL", "memory://")
os.environ.setdefault("CELERY_RESULT_BACKEND", "cache+memory://")

from celery_task_queue.app import create_app
from celery_task_queue.config import CeleryConfig


@pytest.fixture
def eager_app() -> object:
    """A Celery app configured to execute tasks inline, no broker required."""
    cfg = CeleryConfig(
        broker_url="memory://",
        result_backend="cache+memory://",
        task_always_eager=True,
        task_eager_propagates=True,
    )
    return create_app(cfg)

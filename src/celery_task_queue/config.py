"""Part of Celery Task Queue by Viprasol Tech Private Limited (https://viprasol.com).

Typed configuration for the Celery application, loadable from environment
variables so the same code runs in tests (eager, offline) and production
(Redis broker + result backend).
"""

from __future__ import annotations

import os
from dataclasses import dataclass

_DEFAULT_BROKER_URL = "redis://localhost:6379/0"
_DEFAULT_RESULT_BACKEND = "redis://localhost:6379/1"
_DEFAULT_TASK_ALWAYS_EAGER = False


def _env_bool(name: str, default: bool) -> bool:
    """Parse a boolean environment variable with sensible truthy values."""
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True, slots=True)
class CeleryConfig:
    """Strongly-typed Celery configuration.

    Attributes mirror Celery setting names (lower-cased) and are applied to the
    app via :meth:`as_celery_dict`.
    """

    broker_url: str = _DEFAULT_BROKER_URL
    result_backend: str = _DEFAULT_RESULT_BACKEND
    task_always_eager: bool = _DEFAULT_TASK_ALWAYS_EAGER
    task_eager_propagates: bool = True
    task_default_queue: str = "default"
    task_serializer: str = "json"
    result_serializer: str = "json"
    accept_content: tuple[str, ...] = ("json",)
    timezone: str = "UTC"
    enable_utc: bool = True
    task_track_started: bool = True
    result_expires: int = 3600
    worker_prefetch_multiplier: int = 1
    task_acks_late: bool = True

    def as_celery_dict(self) -> dict[str, object]:
        """Render the config as a dict consumable by ``Celery.conf.update``."""
        return {
            "broker_url": self.broker_url,
            "result_backend": self.result_backend,
            "task_always_eager": self.task_always_eager,
            "task_eager_propagates": self.task_eager_propagates,
            "task_default_queue": self.task_default_queue,
            "task_serializer": self.task_serializer,
            "result_serializer": self.result_serializer,
            "accept_content": list(self.accept_content),
            "timezone": self.timezone,
            "enable_utc": self.enable_utc,
            "task_track_started": self.task_track_started,
            "result_expires": self.result_expires,
            "worker_prefetch_multiplier": self.worker_prefetch_multiplier,
            "task_acks_late": self.task_acks_late,
        }


def load_config() -> CeleryConfig:
    """Build a :class:`CeleryConfig` from environment variables.

    Recognised variables (all optional):

    - ``CELERY_BROKER_URL``
    - ``CELERY_RESULT_BACKEND``
    - ``CELERY_TASK_ALWAYS_EAGER`` — set to ``true`` to run tasks inline,
      with no broker, which is exactly what the offline test suite uses.
    """
    return CeleryConfig(
        broker_url=os.getenv("CELERY_BROKER_URL", _DEFAULT_BROKER_URL),
        result_backend=os.getenv("CELERY_RESULT_BACKEND", _DEFAULT_RESULT_BACKEND),
        task_always_eager=_env_bool(
            "CELERY_TASK_ALWAYS_EAGER", _DEFAULT_TASK_ALWAYS_EAGER
        ),
    )

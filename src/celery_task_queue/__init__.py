"""Part of Celery Task Queue by Viprasol Tech Private Limited (https://viprasol.com).

A clean, batteries-included Celery task-queue starter: a configured Celery app,
example tasks with retries / rate limits / workflows, a results helper, and
pure-function task logic that is fully testable offline.
"""

from __future__ import annotations

from celery_task_queue.app import create_app
from celery_task_queue.config import CeleryConfig, load_config

__all__ = ["CeleryConfig", "__version__", "create_app", "load_config"]

__version__ = "0.1.0"

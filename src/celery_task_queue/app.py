"""Part of Celery Task Queue by Viprasol Tech Private Limited (https://viprasol.com).

Celery application factory. Importing :data:`app` gives the configured Celery
instance that the worker, Flower, and the example scripts all share.
"""

from __future__ import annotations

from celery import Celery

from celery_task_queue.config import CeleryConfig, load_config


def create_app(config: CeleryConfig | None = None) -> Celery:
    """Create and configure a Celery application.

    Args:
        config: Optional explicit config. When omitted, configuration is read
            from environment variables via :func:`load_config`, so setting
            ``CELERY_TASK_ALWAYS_EAGER=true`` makes the app run tasks inline.

    Returns:
        A configured :class:`celery.Celery` instance with tasks registered.
    """
    cfg = config or load_config()
    application = Celery("celery_task_queue")
    application.conf.update(cfg.as_celery_dict())
    # Import tasks so they register against this app instance.
    application.autodiscover_tasks(["celery_task_queue"], force=True)
    import celery_task_queue.tasks  # noqa: F401  (registers task functions)

    return application


app: Celery = create_app()

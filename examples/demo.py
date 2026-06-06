"""Part of Celery Task Queue by Viprasol Tech Private Limited (https://viprasol.com).

Runnable demo. By default it runs fully OFFLINE in eager mode (no Redis), so you
can see tasks and workflows execute immediately:

    python examples/demo.py

To run against a real worker + Redis instead, start the stack with
``docker compose up`` and set ``CELERY_TASK_ALWAYS_EAGER=false`` plus the broker
URLs before invoking this script.
"""

from __future__ import annotations

import os


def main() -> None:
    # Default to offline eager mode unless the caller overrides it.
    os.environ.setdefault("CELERY_TASK_ALWAYS_EAGER", "true")
    os.environ.setdefault("CELERY_BROKER_URL", "memory://")
    os.environ.setdefault("CELERY_RESULT_BACKEND", "cache+memory://")

    from celery_task_queue import results, workflows
    from celery_task_queue.tasks import add_task, divide_task, summarize_task

    print("add(2, 40) =", add_task.apply(args=(2, 40)).get())

    summary = summarize_task.apply(args=([10, 20, 30],)).get()
    print("summarize([10,20,30]) =", summary)

    chord_result = workflows.sum_of_products([(2, 3), (4, 5)]).apply()
    print("sum_of_products([(2,3),(4,5)]) =", chord_result.get())

    divide = divide_task.apply(args=(9, 3))
    print("divide(9, 3) snapshot =", results.snapshot(divide))


if __name__ == "__main__":
    main()

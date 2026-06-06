"""Offline tests for Celery tasks, run in eager mode (no broker/Redis)."""

from __future__ import annotations

import pytest
from celery import Celery

from celery_task_queue import results
from celery_task_queue.tasks import (
    add_task,
    divide_task,
    multiply_task,
    summarize_task,
    word_count_task,
)


def test_add_task_eager(eager_app: Celery) -> None:
    res = add_task.apply(args=(4, 5))
    assert res.get() == 9
    assert res.successful()


def test_multiply_task_eager(eager_app: Celery) -> None:
    assert multiply_task.apply(args=([2, 5, 10],)).get() == 100


def test_word_count_task_eager(eager_app: Celery) -> None:
    assert word_count_task.apply(args=("go go stop",)).get() == {
        "go": 2,
        "stop": 1,
    }


def test_summarize_task_eager(eager_app: Celery) -> None:
    out = summarize_task.apply(args=([2, 4, 6],)).get()
    assert out["mean"] == 4.0


def test_divide_task_eager(eager_app: Celery) -> None:
    assert divide_task.apply(args=(9, 3)).get() == 3


def test_divide_task_by_zero_raises(eager_app: Celery) -> None:
    # In eager mode an invalid divide triggers the autoretry path, which
    # surfaces as an exception rather than a successful result.
    with pytest.raises(Exception):  # noqa: B017
        divide_task.apply(args=(1, 0)).get()


def test_results_snapshot(eager_app: Celery) -> None:
    res = add_task.apply(args=(1, 1))
    snap = results.snapshot(res)
    assert snap.ready is True
    assert snap.successful is True
    assert snap.value == 2


def test_results_wait_for(eager_app: Celery) -> None:
    res = add_task.apply(args=(7, 8))
    assert results.wait_for(res, timeout=5) == 15


def test_word_count_task_has_rate_limit() -> None:
    assert word_count_task.rate_limit == "100/m"


def test_divide_task_retry_config() -> None:
    assert divide_task.max_retries == 3


@pytest.mark.parametrize("value", [0, 1, 2])
def test_add_task_parametrized(eager_app: Celery, value: int) -> None:
    assert add_task.apply(args=(value, value)).get() == value * 2

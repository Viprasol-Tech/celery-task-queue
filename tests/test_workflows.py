"""Offline tests for canvas workflows (chain/group/chord) in eager mode."""

from __future__ import annotations

from celery import Celery

from celery_task_queue import workflows


def test_add_then_double(eager_app: Celery) -> None:
    sig = workflows.add_then_double(3, 4)
    assert sig.apply().get() == 14  # (3 + 4) * 2


def test_parallel_products(eager_app: Celery) -> None:
    sig = workflows.parallel_products([(2, 3), (4, 5)])
    assert sorted(sig.apply().get()) == [6, 20]


def test_sum_of_products(eager_app: Celery) -> None:
    sig = workflows.sum_of_products([(2, 3), (4, 5)])
    assert sig.apply().get() == 26  # 6 + 20


def test_workflow_signatures_are_constructable() -> None:
    # Signatures can be built with no broker connection at all.
    assert workflows.add_then_double(1, 1) is not None
    assert workflows.parallel_products([(1, 1)]) is not None

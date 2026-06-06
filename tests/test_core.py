"""Offline unit tests for the pure task logic in :mod:`celery_task_queue.core`."""

from __future__ import annotations

import pytest

from celery_task_queue import core


def test_add() -> None:
    assert core.add(2, 3) == 5


def test_multiply() -> None:
    assert core.multiply([2, 3, 4]) == 24


def test_multiply_empty_raises() -> None:
    with pytest.raises(core.TaskInputError):
        core.multiply([])


def test_double() -> None:
    assert core.double(21) == 42


def test_normalize_text() -> None:
    assert core.normalize_text("  Hello   WORLD\n") == "hello world"


def test_word_count() -> None:
    assert core.word_count("a a b") == {"a": 2, "b": 1}


def test_chunk() -> None:
    assert core.chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_chunk_invalid_size() -> None:
    with pytest.raises(core.TaskInputError):
        core.chunk([1, 2, 3], 0)


def test_summarize_numbers() -> None:
    out = core.summarize_numbers([1, 2, 3, 4])
    assert out["count"] == 4
    assert out["sum"] == 10
    assert out["mean"] == 2.5
    assert out["min"] == 1
    assert out["max"] == 4


def test_summarize_empty_raises() -> None:
    with pytest.raises(core.TaskInputError):
        core.summarize_numbers([])


@pytest.mark.parametrize(
    ("retries", "expected"),
    [(0, 1.0), (1, 2.0), (3, 8.0), (20, 600.0)],
)
def test_compute_backoff(retries: int, expected: float) -> None:
    assert core.compute_backoff(retries) == expected


def test_compute_backoff_negative_raises() -> None:
    with pytest.raises(core.TaskInputError):
        core.compute_backoff(-1)


def test_safe_divide() -> None:
    assert core.safe_divide(10, 2) == 5


def test_safe_divide_by_zero_raises() -> None:
    with pytest.raises(core.TaskInputError):
        core.safe_divide(1, 0)

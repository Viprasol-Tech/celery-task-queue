# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-01

### Added

- Configured Celery application factory (`create_app`) with environment-driven,
  typed `CeleryConfig`.
- Pure task logic in `core.py` (add, multiply, double, text/word-count,
  summarize, backoff, safe-divide) with thin Celery task wrappers.
- Retry-with-backoff task (`divide_task`) and a rate-limited task
  (`word_count_task`).
- Canvas workflow builders: chain, group, and chord (`workflows.py`).
- Results helper with a typed `ResultSnapshot` and `wait_for`.
- Fully offline test suite (34 tests) using `task_always_eager`.
- Docker Compose stack (Redis + worker), Dockerfile, and Flower notes.
- CI matrix (Ubuntu/macOS/Windows × Python 3.11–3.13), ruff, mypy strict,
  pytest, Dependabot, issue/PR templates.

[0.1.0]: https://github.com/Viprasol-Tech/celery-task-queue/releases/tag/v0.1.0

# Contributing to Celery Task Queue

Thanks for your interest in improving this project, maintained by
[Viprasol Tech](https://viprasol.com)! Contributions of all sizes are welcome.

## Getting started

```bash
git clone https://github.com/Viprasol-Tech/celery-task-queue.git
cd celery-task-queue
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Development workflow

1. Create a feature branch off `main`.
2. Keep business logic in `src/celery_task_queue/core.py` as **pure functions**;
   Celery tasks should stay thin wrappers. This is what keeps tests offline.
3. Add or update tests under `tests/` — they must run in eager mode (no broker).
4. Run the full check suite locally before opening a PR:

   ```bash
   python -m ruff check .
   python -m ruff format --check .
   python -m mypy src
   python -m pytest
   ```

5. Open a pull request using the provided template. CI runs on
   Ubuntu/macOS/Windows across Python 3.11–3.13.

## Code style

- Formatting & linting: **ruff**.
- Types: **mypy --strict**. New code should be fully typed.
- Conventional, descriptive commit messages are appreciated.

## Reporting bugs / requesting features

Use the GitHub issue templates. For security issues, see [SECURITY.md](SECURITY.md).

By contributing, you agree your contributions are licensed under the MIT License.

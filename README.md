<p align="center"><img src="docs/assets/logo.png" width="120"></p>

# Celery Task Queue

**A clean, production-shaped Celery starter — configured app, example tasks with retries & rate limits, chained/grouped/chord workflows, a results helper, and a fully offline test suite.**

*Built and maintained by [Viprasol Tech](https://viprasol.com) — Fintech Experts. Full-Stack Builders.*

<p align="center">
  <img src="https://img.shields.io/github/actions/workflow/status/Viprasol-Tech/celery-task-queue/ci.yml?branch=main&style=flat-square" alt="CI">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT License">
  <img src="https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue?style=flat-square" alt="Python">
  <img src="https://img.shields.io/badge/lint-ruff-261230?style=flat-square" alt="Ruff">
  <img src="https://img.shields.io/badge/Telegram-viprasol__help-26A5E4?style=flat-square&logo=telegram" alt="Telegram">
  <img src="https://img.shields.io/github/stars/Viprasol-Tech/celery-task-queue?style=flat-square" alt="Stars">
</p>

---

## ✨ Features

- 🧱 **Pre-configured Celery app** via a clean application factory (`create_app`).
- 🧠 **Pure task logic** — all business logic lives in a `core` module of plain functions; tasks are thin wrappers.
- 🧪 **Fully offline tests** — the suite runs with `task_always_eager` (no broker, no Redis, no worker). 34 tests.
- 🔁 **Retries with backoff** — `divide_task` shows `autoretry_for`, exponential `retry_backoff`, jitter and `max_retries`.
- 🚦 **Rate limiting** — `word_count_task` is capped at `100/m` per worker.
- 🔗 **Workflows** — ready-made `chain`, `group`, and `chord` builders in `workflows.py`.
- 📦 **Typed config** — environment-driven `CeleryConfig` dataclass, strict-mypy clean.
- 📊 **Results helper** — typed `ResultSnapshot` + a polite `wait_for` wrapper around `AsyncResult`.
- 🐳 **Docker-first** — `docker compose up` gives you Redis + a worker instantly.
- 🌸 **Flower monitoring** — one command to watch tasks live (see below).
- ⚙️ **CI matrix** — Ubuntu / macOS / Windows × Python 3.11–3.13.
- 🧹 **Tooling** — ruff (lint + format), mypy `--strict`, pytest, Dependabot.

## 🚀 Quickstart

### Option A — Docker (Redis + worker), recommended for real use

```bash
git clone https://github.com/Viprasol-Tech/celery-task-queue.git
cd celery-task-queue
cp .env.example .env
docker compose up --build
```

This starts Redis and a Celery worker wired to it.

### Option B — Local, fully offline (no broker)

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
python examples/demo.py        # runs tasks + workflows inline, eager mode
pytest                         # 34 offline tests
```

## 🧑‍💻 Usage

```python
import os
os.environ["CELERY_TASK_ALWAYS_EAGER"] = "true"   # offline; drop in production

from celery_task_queue import workflows
from celery_task_queue.tasks import add_task, divide_task

# Simple task
print(add_task.apply(args=(2, 40)).get())          # -> 42

# Chained workflow: (3 + 4) then doubled
print(workflows.add_then_double(3, 4).apply().get())  # -> 14

# Chord: multiply pairs in parallel, then sum the products
print(workflows.sum_of_products([(2, 3), (4, 5)]).apply().get())  # -> 26

# Retry-on-error task (exponential backoff configured)
print(divide_task.apply(args=(9, 3)).get())        # -> 3
```

In production, set `CELERY_TASK_ALWAYS_EAGER=false`, point `CELERY_BROKER_URL` /
`CELERY_RESULT_BACKEND` at Redis, and start a worker:

```bash
celery -A celery_task_queue.app:app worker --loglevel=info
```

### 🌸 Monitoring with Flower

```bash
pip install ".[monitoring]"
celery -A celery_task_queue.app:app flower --port=5555
# open http://localhost:5555
```

## 🗺️ Roadmap

- [ ] Periodic tasks via Celery Beat (scheduled jobs).
- [ ] Dead-letter queue example + failure inspection.
- [ ] Prometheus metrics exporter for workers.
- [ ] RabbitMQ broker profile alongside Redis.
- [ ] Result-backend examples for PostgreSQL.

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) and our
[Code of Conduct](CODE_OF_CONDUCT.md). Open an issue or a PR — every check
(ruff, mypy, pytest) must be green.

## 📬 Contact — Viprasol Tech Private Limited

- 🌐 Website: [viprasol.com](https://viprasol.com)
- ✉️ Email: [support@viprasol.com](mailto:support@viprasol.com)
- 💬 Telegram: [t.me/viprasol_help](https://t.me/viprasol_help) · 📱 WhatsApp: +91 96336 52112
- 🐙 GitHub: [@Viprasol-Tech](https://github.com/Viprasol-Tech) · 💼 [LinkedIn](https://www.linkedin.com/in/viprasol/) · 𝕏 [@viprasol](https://twitter.com/viprasol)

> *Viprasol Tech — fintech software, algorithmic trading systems, MT4/MT5 bots, AI voice agents, and B2B SaaS. Need a custom build? [Get in touch](mailto:support@viprasol.com).*

## 📄 License

MIT © 2025 Viprasol Tech Private Limited. See [LICENSE](LICENSE).

# MiniShop

A small product-management web app and REST API (Python + Flask), built as a beginner DevOps project:
Git, GitHub Pull Requests, automated tests, CI with GitHub Actions, Docker, version tags and rollback.

## Pipeline

```
commit -> branch -> Pull Request -> CI (install, pytest, docker build, smoke test) -> merge -> tag vX.Y.Z -> Docker image -> run / rollback
```

## Run it locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python app.py
```

Open http://localhost:8000

## Run the tests

```bash
pytest -v
```

## Run with Docker

```bash
docker build -t minishop:v1.0.0 .
docker run -d --name minishop -p 8000:8000 minishop:v1.0.0
curl localhost:8000/health
```

## API

| Method | Path | What it does |
|---|---|---|
| GET | `/` | Web page |
| GET | `/health` | `{"status": "ok", "version": "..."}` |
| GET | `/products` | List products |
| POST | `/products` | Add a product `{"name": "Pen", "price": 10}` |
| PUT | `/products/<id>` | Update name and/or price |
| DELETE | `/products/<id>` | Delete a product |

## CI

`.github/workflows/ci.yml` runs on every push to `main`, every pull request and every `v*` tag:
1. Install dependencies and run pytest.
2. Build the Docker image, start it and call `/health`.

## Releases and rollback

Versions follow SemVer and live in the `VERSION` file. Each release is a Git tag (`v1.0.0`, `v1.1.0`) and a Docker image with the same tag.
Rollback means running the previous image again, for example `minishop:v1.0.0`.

## Screenshots

_Add: green CI run, red CI run on a failing test, app running with version badge, v1.1.0 vs v1.0.0._

## Known limits and phase 2

- Products are stored in memory and reset on restart. Next: a database (Postgres with Docker Compose).
- Not done yet: container registry (GHCR), cloud deployment, Terraform, CD workflow, security scanning, monitoring.

## What I learned

_Write 5 to 6 lines: what broke, why, and how you fixed it._


# Bootstrap Module

<p align="right"><em>Part of the <strong>SAI Gen-AI Monorepo</strong></em></p>

The Bootstrap module is responsible for initializing, and load testing AI service infrastructure and data pipelines. It provides scripts and utilities for document embedding, data ingestion, and load testing, and is typically run as a containerized service. This module is designed for rapid setup and reproducible deployments in both local and production environments.

## Features

- **Embedding & Data Ingestion:**
  - Utilities to embed documents and ingest data into vector stores (e.g., Qdrant).
  - Supports batch processing and custom data sources.
- **Load Testing:**
  - Locust-based load testing for API endpoints.
  - Result plotting utilities for performance analysis.
- **Environment Management:**
  - Loads environment variables from `.env`.
  - Supports configuration via environment variables or Docker.
- **Containerized Deployment:**
  - Multi-stage Dockerfile and init scripts for reproducible builds and deployments.
  - Easy integration with CI/CD pipelines.

## Directory Structure

- `src/` — Main source code for embedding, deployment, and utilities
  - `env.py` — Loads environment variables and manages configuration
  - `force_deploy.py` — Main entrypoint for deployment and embedding workflows
  - `utils/` — Logging and helper utilities
  - `source_ai/` — Data source folders (UUID-named for isolation)
- `tests/` — Load testing and result analysis
  - `locustfile.py` — Locust test scenarios for API endpoints
  - `plot_locust_results.py` — Utility to plot and analyze load test results
  - `questions.yaml` — Sample questions for load tests
- `Dockerfile` — Multi-stage build for production containers
- `init.sh` — Entrypoint script for container initialization
- `pyproject.toml` — Poetry project configuration

## Getting Started

### Prerequisites

- Python 3.12 or higher
- [Poetry](https://python-poetry.org/) for dependency management
- Docker (for containerized usage)

### Local Development

1. **Install dependencies:**
   ```bash
   poetry install
   ```
2. **Set environment variables:**
   - Copy and edit your `.env` file as needed (see `src/env.py` for required variables).
3. **Run embedding/deployment:**
   ```bash
   poetry run python src/force_deploy.py
   ```

### Running in Docker

Build and run the container:

```bash
docker build -t bootstrap .
docker run --env-file .env bootstrap
```

### Load Testing

1. Edit `tests/questions.yaml` with your test questions.
2. Run Locust load tests:
   ```bash
   poetry run locust -f tests/locustfile.py --host=http://your-api-host
   ```
3. Analyze results with the provided plotting script:
   ```bash
   poetry run python tests/plot_locust_results.py
   ```

## Environment Variables

See `src/env.py` for all supported environment variables (e.g., API keys, Qdrant/Redis/Postgres connection info).

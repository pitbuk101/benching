# Chat Service

A modular, extensible chat service built with Python 3.12, FastAPI, and Celery, designed for real-time, AI-powered conversational experiences. This service supports advanced prompt handling, internet search integration, and structured response parsing.

## Features

- **FastAPI**-based web service for chat endpoints
- Modular pipeline architecture for extensibility
- Integration with LLMs (e.g., OpenAI) and internet search
- Celery-based background task processing
- Configurable via environment variables and YAML
- Dockerized for easy deployment

## Project Structure

```text
chat-service/
├── Dockerfile
├── poetry.lock
├── pyproject.toml
├── README.md
├── src/
│   ├── main.py           # FastAPI app entrypoint
│   ├── env.py            # Environment variable handling
│   ├── celery_tasks/     # Celery config and tasks
│   ├── configs/          # Configuration models
│   ├── datamodels/       # Pydantic data models
│   ├── middleware/       # Custom middleware (e.g., auth)
│   ├── models/           # ORM or business models
│   ├── pipelines/        # Chat pipelines (generation, parsing, etc.)
│   ├── providers/        # LLM and prompt providers
│   ├── routers/          # FastAPI routers
│   ├── source_ai/        # AI source integrations
│   └── utils/            # Utility functions
└── test/
    └── test_api_bridge.py # Example test
```

## Getting Started

### Prerequisites

- Python 3.12+
- [Poetry](https://python-poetry.org/) for dependency management
- Docker (optional, for containerized deployment)

### Installation (Local)

1. **Clone the repository**
    ```bash
    git clone <repo-url>
    cd chat-service
    ```

2. **Install dependencies**
    ```bash
    poetry install
    ```

3. **Set up environment variables**
    - Copy `.env.example` to `.env` and update as needed.

4. **Run the service**
    ```bash
    poetry run python -m uvicorn src.__main__:app --host 0.0.0.0 --port 8088 --loop uvloop --http httptools
    ```

### Running with Docker

1. **Build and run the container**
    ```bash
    docker build -t chat-service .
    docker run -p 8088:8088 --env-file .env chat-service
    ```

## Configuration

- Main configuration is handled via environment variables and YAML files in `src/configs/`.
- Update `config.yaml` and `.env` as needed for your environment.

## Development

- Main app entrypoint: [`src/__main__.py`](src/__main__.py)
- Add new chat pipelines in [`src/pipelines/`](src/pipelines/)
- Add or modify data models in [`src/datamodels/`](src/datamodels/)

## Testing

- Place tests in the `test/` directory.
- Run tests with your preferred test runner (e.g., pytest).

## Example Pipelines

- [`openworld.py`](src/pipelines/generation/openworld.py): Handles open-world question answering with internet search and LLMs.
- [`openworldsummary.py`](src/pipelines/generation/openworldsummary.py): Summarizes open-world responses.
- [`kfsummary.py`](src/pipelines/generation/kfsummary.py): Summarizes knowledge-fusion outputs.

## License

MIT License

---

For more details, see the code and comments in each module.
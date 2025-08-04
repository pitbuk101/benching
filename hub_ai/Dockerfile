# FROM python:3.10-slim

# ENV POETRY_VERSION=1.8.1
# ENV POETRY_VIRTUALENVS_CREATE=false \
#     POETRY_CACHE_DIR='/var/cache/pypoetry' \
#     PLAYWRIGHT_BROWSERS_PATH=/usr/local/share/ms-playwright

# WORKDIR /app

# # System deps
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     curl \
#     build-essential \
#     git \
#     && rm -rf /var/lib/apt/lists/*

# # Install Poetry
# RUN curl -sSL https://install.python-poetry.org | python3 -

# ENV PATH="/root/.local/bin:$PATH"

# # Copy only dependency files for caching
# COPY pyproject.toml poetry.lock* /app/

# RUN poetry install --no-root --only main --no-cache

# # Install Playwright & browsers
# RUN pip install playwright && playwright install --with-deps

# # Copy project source
# COPY . /app

# # Expose FastAPI port
# EXPOSE 8000

# # Clean up (optional)
# RUN rm -rf /root/.cache /var/cache/pypoetry

# # Start FastAPI app
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]




# Use official Python slim image
FROM python:3.10-slim

# Set environment variables
ENV POETRY_VERSION=1.8.1
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry'

# Set Playwright browsers path
ENV PLAYWRIGHT_BROWSERS_PATH=/usr/local/share/ms-playwright

# Set workdir inside container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy Poetry files
COPY pyproject.toml poetry.lock* /app/

# Install dependencies without caching and dev deps
RUN poetry install --no-root --only main --no-cache

# Ensure playwright is installed before calling playwright install
RUN pip install playwright

# Install Playwright browsers to custom directory
RUN playwright install --with-deps

# Copy your project files last (after deps are cached)
COPY . /app

# Optional cleanup to save space
RUN rm -rf /root/.cache /var/cache/pypoetry ~/.npm ~/.cache

# Default command
CMD ["python", "app.py"]
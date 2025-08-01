FROM python:3.12-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y gcc g++ build-essential

# Set the working directory
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry==2.0.1

# Copy only the dependency files first to leverage Docker cache
COPY pyproject.toml /app/

# Install dependencies
# RUN poetry install --no-root --no-cache
RUN poetry install --no-root

# Copy the rest of the application code into the container
COPY . /app/

# Make entrypoint.sh executable
RUN chmod +x /app/entrypoint.sh

# Expose port 8000 for the FastAPI app
EXPOSE 5000

# Set entrypoint to run the entrypoint.sh script
ENTRYPOINT ["/app/entrypoint.sh"]

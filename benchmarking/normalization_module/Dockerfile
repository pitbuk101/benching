# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

# Install poetry for dependency management
RUN pip install --no-cache-dir poetry

# Copy only the dependency definition files to leverage Docker layer caching
COPY poetry.lock pyproject.toml README.md /app/

# Install project dependencies using poetry
# virtualenvs.create false installs dependencies into the system's site-packages, standard for Docker
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --only main --no-root

# Copy the rest of the application source code into the container
COPY . /app

# Expose the port the app runs on
EXPOSE 8001

# Define the command to run the application
# This will start the Uvicorn server to serve the FastAPI app

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]

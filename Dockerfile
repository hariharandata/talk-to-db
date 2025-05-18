# Use official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy only pyproject.toml and poetry.lock first for caching
COPY pyproject.toml poetry.lock* /app/

# Configure Poetry to not use a virtualenv
RUN poetry config virtualenvs.create false \
  && poetry lock \
  && poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the app
COPY . /app

# Ensure .env file is copied (if it exists)
COPY .env* /app/src/

# Expose the FastAPI app
CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8002"]
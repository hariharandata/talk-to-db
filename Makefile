# Makefile for Talk to DB Project

# Docker image details
IMAGE_NAME := hariharan26/talk-to-db
IMAGE_TAG := latest

# Build Docker image
build:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

# Push Docker image to registry
push:
	docker push $(IMAGE_NAME):$(IMAGE_TAG)

# Run Docker container
run:
	docker run -d --name talk-to-db \
		-p 8002:8002 \
		-e DB_HOST=host.docker.internal \
		$(IMAGE_NAME):$(IMAGE_TAG)

# Stop and remove Docker container
stop:
	docker stop talk-to-db || true
	docker rm talk-to-db || true

# Run Ruff linting
lint:
	poetry run ruff check src

# Auto-fix lint issues
lint-fix:
	poetry run ruff check src --fix

# Format code
format:
	poetry run ruff check src --fix
	poetry run ruff format src


# Clean up
clean:
	docker rmi $(IMAGE_NAME):$(IMAGE_TAG) || true
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

.PHONY: build push run stop lint lint-fix format test clean
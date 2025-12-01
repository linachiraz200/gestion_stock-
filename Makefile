.PHONY: help install test lint format security clean docker-build docker-run

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install black isort flake8 coverage safety bandit pytest-django

test:  ## Run tests
	python manage.py test

test-coverage:  ## Run tests with coverage
	coverage run --source='.' manage.py test
	coverage report --show-missing
	coverage html

lint:  ## Run linting
	flake8 .
	black --check .
	isort --check-only .

format:  ## Format code
	black .
	isort .

security:  ## Run security checks
	safety check --ignore=70612
	bandit -r . -x tests/,venv/ -ll

quality:  ## Run all quality checks
	$(MAKE) lint
	$(MAKE) security
	$(MAKE) test-coverage

migrate:  ## Run database migrations
	python manage.py migrate

collectstatic:  ## Collect static files
	python manage.py collectstatic --noinput

runserver:  ## Run development server
	python manage.py runserver

docker-build:  ## Build Docker image
	docker build -t gestion-stock .

docker-run:  ## Run Docker container
	docker run -p 8000:8000 gestion-stock

docker-test:  ## Test Docker image
	docker run --rm -e USE_MONGODB=False -e DEBUG=True -e SECRET_KEY=test-key gestion-stock python manage.py test

clean:  ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .coverage htmlcov/ .pytest_cache/

setup-dev:  ## Set up development environment
	$(MAKE) install
	cp .env.example .env
	$(MAKE) migrate
	@echo "Development environment ready!"

ci:  ## Run CI pipeline locally
	$(MAKE) quality
	$(MAKE) docker-build
	$(MAKE) docker-test
	@echo "✅ CI pipeline completed successfully!"
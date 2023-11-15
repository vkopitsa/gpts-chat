clean: ## clean 
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -f .coverage

down: ## down
	docker-compose down

lint: ## lint
	docker-compose run --rm app-test sh -c " \
		pip install -r requirements-dev.txt && \
		flake8 . && \
		isort --check --diff . && \
		mypy app/"

up: ## up
	docker-compose up app

test: ## test
	docker-compose run --rm app-test

coverage: ## coverage
	docker-compose run --rm app-test sh -c " \
		pip install -r requirements-dev.txt && \
		coverage run -m pytest && \
		coverage report -m "

ci: lint test coverage ## ci

# Absolutely awesome: https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

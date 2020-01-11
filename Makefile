.PHONY: cleanup
cleanup: ## Cleanup
	# alias pyclean='find . -name "*.py[co]" -o -name __pycache__ -exec rm -rf {} +'
	find . -name "*.py[co]" -o -name __pycache__ -exec rm -rf {} +

.PHONY: dbshell
dbshell: ## Open a shell to the db running in the docker container (must run in container)
	pip install pgcli
	pgcli -h db -p 5432 -u postgres

.PHONY: test
test: ## Run unittests.
	docker-compose run --service-ports app make run-tests

.PHONY: run-tests
run-tests: ## Run tests (must run in container)
	pytest -s --cov=app --no-cov-on-fail --cov-fail-under=80

.PHONY: shell
shell: ## Run container.
	docker-compose run --service-ports app /bin/bash

.PHONY: fmt
fmt: ## Format files.
	docker-compose run app make run-fmt

.PHONY: run-fmt
run-fmt: ## Format files.
	black app/
	
.PHONY: build
build: ## Build the docker container
	git config core.hooksPath .githooks
	docker-compose build
	docker-compose down

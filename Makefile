.PHONY: cleanup
cleanup: ## Cleanup
	# alias pyclean='find . -name "*.py[co]" -o -name __pycache__ -exec rm -rf {} +'
	find . -name "*.py[co]" -o -name __pycache__ -exec rm -rf {} +

.PHONY: dbshell
dbshell: ## Open a shell to the db running in the docker container (must run in container)
	pip install pgcli
	pgcli -h db -p 5432 -u postgres

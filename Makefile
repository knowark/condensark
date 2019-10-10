
clean:
	find . -name '__pycache__' -exec rm -fr {} +
	rm -rf ./.cache .mypy_cache ./schema/.mypy_cache .coverage

test:
	pytest

coverage-application: 
	pytest -x --cov=integrark/application tests/application/ \
	--cov-report term-missing -s

coverage-infrastructure: 
	pytest -x --cov=integrark/infrastructure tests/infrastructure/ \
	--cov-report term-missing -s

coverage: 
	pytest -x --cov=integrark tests/ --cov-report term-missing -s

serve:
	python -m integrark serve
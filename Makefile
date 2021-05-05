
clean:
	find . -name '__pycache__' -exec rm -fr {} +
	rm -rf ./.cache .mypy_cache ./schema/.mypy_cache .coverage

test:
	pytest

PROJECT = integrark

mypy:
	mypy $(PROJECT)

coverage-application:
	pytest -x --cov=$(PROJECT)/application tests/application/ \
	--cov-report term-missing -s

coverage-infrastructure:
	pytest -x --cov=$(PROJECT)/infrastructure tests/infrastructure/ \
	--cov-report term-missing -s

COVFILE ?= /tmp/.coverage

coverage:
	export COVERAGE_FILE=$(COVFILE); pytest -x --cov=$(PROJECT) \
	tests/ --cov-report term-missing -s -vv \
	-o cache_dir=/tmp/integrark/cache

serve:
	python -m $(PROJECT) serve

deploy:
	ansible-playbook -c local -i localhost, setup/deploy.yml

local:
	./setup/local.sh

PART ?= patch

version:
	bump2version $(PART) $(PROJECT)/__init__.py --tag --commit

gitmessage:
	touch .gitmessage
	echo "\n# commit message\n.gitmessage" >> .gitignore
	git config commit.template .gitmessage

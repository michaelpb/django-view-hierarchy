.PHONY: clean-pyc clean-build docs help
.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

clean: clean-build clean-pyc

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint: ## check style with flake8
	flake8 django_view_hierarchy tests

test: ## run tests quickly with the default Python
	python runtests.py tests

test-watch: ## run tests repeatedly watching for directory changes
	find django_view_hierarchy/ example/ tests/ -name \*.py | entr python runtests.py tests

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source django_view_hierarchy runtests.py tests
	coverage report -m
	coverage html
	open htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/django_view_hierarchy.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ django_view_hierarchy
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

release: clean ## package and upload a release
	python setup.py sdist upload
	python setup.py bdist_wheel upload

sdist: clean ## package
	python setup.py sdist
	ls -l dist

bump-and-push: test lint
	bumpversion patch
	git push
	git push --tags
	make release

cleanup-pep8: ## Auto fix a few issues
	autoflake --in-place --remove-all-unused-imports --remove-unused-variables -r django_view_hierarchy
	autoflake --in-place --remove-all-unused-imports --remove-unused-variables -r example
	autoflake --in-place --remove-all-unused-imports --remove-unused-variables -r tests
	autopep8 --in-place -r django_view_hierarchy
	autopep8 --in-place -r example
	autopep8 --in-place -r tests
	isort -rc --atomic django_view_hierarchy
	isort -rc --atomic example
	isort -rc --atomic tests


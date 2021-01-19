.PHONY: run dev dist pypi test-pypi prod-pypi build experiment

# If the first argument is "run"...
ifeq (run,$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "run"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif

experiment:
	$(shell ./experiment.sh)

dev:
	pip install -e'.[dev]'

run:
	python bin/vshot $(RUN_ARGS)

dist:
	python setup.py sdist

pypi:
	$(MAKE) dist
	twine check dist/*

test-pypi:
	$(MAKE) pypi
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

prod-pypi:
	$(MAKE) pypi
	twine upload --repository-url https:/.pypi.org/ dist/*

build:
	docker build . -t lowess/vshot

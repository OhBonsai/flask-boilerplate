.PHONY: test

default: test

test:
	pytest -s -v tests

coverage:
	pytest --cov-app tests/

test-report:
	pytest -s -v tests --html=docs/test/index.html

doc:
	cd docs/api/ && apidoc -i ../../app/api -o html/

build:
	python setup.py sdist

clean:
	rm -rf ./docs/api/html
	rm -rf ./docs/test
	rm -rf ./docs/coverage
	rm -f database.db
	rm -f test.db
	rm -f .coverage
	rm -rf .cache
	rm -rf dist

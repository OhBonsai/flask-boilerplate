.PHONY: test

default: test

test:
	echo "do some test"

doc:
	cd docs/api/ && apidoc -i ../../app/api -o html/

clean:
	rm -rf ./docs/api/html
	rm -f database.db

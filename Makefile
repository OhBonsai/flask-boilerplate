.PHONY: test

default: test

test:
	echo "do some test"

doc:
	cd docs/api/ && apidoc -i ../../app/api -o html/

clean:
	rm -r ./docs/api/html

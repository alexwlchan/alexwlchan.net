ROOT = $(shell git rev-parse --show-toplevel)
TESTS = $(ROOT)/tests

TESTS_IMAGE = alexwlchan/alexwlchan.net_tests
FLAKE8_IMAGE = alexwlchan/flake8
SERVE_CONTAINER = server


$(ROOT)/.docker/tests: $(TESTS)/Dockerfile $(TESTS)/*.py $(TESTS)/requirements.txt
	docker build --tag $(TESTS_IMAGE) --file $(TESTS)/Dockerfile $(TESTS)
	mkdir -p $(ROOT)/.docker
	touch $(ROOT)/.docker/tests

$(ROOT)/.docker/flake8: $(TESTS)/flake8.Dockerfile
	docker build --tag $(FLAKE8_IMAGE) --file $(TESTS)/flake8.Dockerfile $(TESTS)
	mkdir -p $(ROOT)/.docker
	touch $(ROOT)/.docker/flake8


check-format: $(ROOT)/.docker/flake8
	docker run --volume $(ROOT):/src --rm $(FLAKE8_IMAGE) --exclude=/src

tests/requirements.txt: tests/requirements.in
	docker run --volume $(TESTS):/src --rm micktwomey/pip-tools
	touch $(TESTS)/requirements.txt

test: $(ROOT)/.docker/tests
	docker run \
		--volume $(ROOT):/repo \
		--env HOSTNAME=$(SERVE_CONTAINER) \
		--link $(SERVE_CONTAINER) \
		--tty --rm $(TESTS_IMAGE)


.PHONY: check-format test

ROOT = $(shell git rev-parse --show-toplevel)
TESTS = $(ROOT)/tests

TESTS_IMAGE = alexwlchan/alexwlchan.net_tests
SERVE_CONTAINER = server


$(ROOT)/.docker/tests: tests/Dockerfile tests/*.py tests/requirements.txt
	docker build --tag $(TESTS_IMAGE) --file $(TESTS)/Dockerfile $(TESTS)
	mkdir -p $(ROOT)/.docker
	touch $(ROOT)/.docker/tests

tests/requirements.txt: tests/requirements.in
	docker run --volume $(TESTS):/src --rm micktwomey/pip-tools
	touch $(TESTS)/requirements.txt

test: $(ROOT)/.docker/tests
	docker run \
		--volume $(ROOT):/repo \
		--env HOSTNAME=$(SERVE_CONTAINER) \
		--link $(SERVE_CONTAINER) \
		--tty --rm $(TESTS_IMAGE)


.PHONY: test

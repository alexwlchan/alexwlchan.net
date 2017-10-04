BUNDLER_IMAGE = alexwlchan/bundler-base
BUILD_IMAGE = alexwlchan/alexwlchan.net
TESTS_IMAGE = alexwlchan/alexwlchan.net_tests
SERVE_CONTAINER = server

RSYNC_HOST = 139.162.244.147
RSYNC_USER = alexwlchan
RSYNC_DIR = /home/alexwlchan/sites/alexwlchan.net

ROOT = $(shell git rev-parse --show-toplevel)
SRC = $(ROOT)/src
TESTS = $(ROOT)/tests

.docker/bundler: bundler.Dockerfile
	docker build --tag $(BUNDLER_IMAGE) --file bundler.Dockerfile .
	mkdir -p .docker && touch .docker/bundler

.docker/build: .docker/bundler Dockerfile install_jekyll.sh install_specktre.sh
	docker build --tag $(BUILD_IMAGE) .
	mkdir -p .docker
	touch .docker/build

.docker/tests: tests/Dockerfile tests/*.py tests/requirements* tests/tox.ini
	docker build --tag $(TESTS_IMAGE) --file $(TESTS)/Dockerfile $(TESTS)
	mkdir -p .docker
	touch .docker/tests


clean: .docker/build
	docker run --volume $(SRC):/site $(BUILD_IMAGE) clean
	rm -rf .docker
	docker rm -f alexwlchan.net_serve
	docker rmi --force $(BUILD_IMAGE)
	docker rmi --force $(TESTS_IMAGE)

build: .docker/build
	docker run --volume $(SRC):/site $(BUILD_IMAGE) build

serve: .docker/build
	@# Clean up old running containers
	@docker stop $(SERVE_CONTAINER) >/dev/null 2>&1 || true
	@docker rm $(SERVE_CONTAINER) >/dev/null 2>&1 || true

	docker run \
		--publish 5757:5757 \
		--volume $(SRC):/site \
		--name $(SERVE_CONTAINER) \
		--hostname $(SERVE_CONTAINER) \
		--tty --detach $(BUILD_IMAGE) \
		serve --host $(SERVE_CONTAINER) --port 5757 --watch

serve-debug: .docker/build
	@# Clean up old running containers
	@docker stop $(SERVE_CONTAINER) >/dev/null 2>&1 || true
	@docker rm $(SERVE_CONTAINER) >/dev/null 2>&1 || true

	docker run \
		--publish 5757:5757 \
		--volume $(SRC):/site \
		--name $(SERVE_CONTAINER) \
		--hostname $(SERVE_CONTAINER) \
		--tty $(BUILD_IMAGE) \
		serve --host $(SERVE_CONTAINER) --port 5757 --watch

publish: build

deploy: publish
	rsync \
		--archive \
		--verbose \
		--compress \
		--delete \
		--rsh="ssh$(SSHOPTS)" \
		src/_site/ "$(RSYNC_USER)"@"$(RSYNC_HOST)":"$(RSYNC_DIR)"

test: .docker/tests
	docker run \
		--volume $(TESTS):/tests \
		--env HOSTNAME=$(SERVE_CONTAINER) \
		--link $(SERVE_CONTAINER) \
		--tty $(TESTS_IMAGE)

Gemfile.lock: .docker/bundler
	docker run \
		--volume $(ROOT):/site \
		--workdir /site \
		--tty $(BUNDLER_IMAGE) \
		lock --update


.PHONY: clean build watch serve serve-debug publish deploy test

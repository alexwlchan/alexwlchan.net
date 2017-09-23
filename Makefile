BUILD_IMAGE = alexwlchan/alexwlchan.net
TESTS_IMAGE = alexwlchan/alexwlchan.net_tests
SERVE_CONTAINER = server

RSYNC_HOST = 139.162.244.147
RSYNC_USER = alexwlchan
RSYNC_DIR = /home/alexwlchan/sites/alexwlchan.net

ROOT = $(shell git rev-parse --show-toplevel)
SRC = $(ROOT)/src

.docker/build:
	docker build --tag $(BUILD_IMAGE) .
	mkdir -p .docker
	touch .docker/build

.docker/tests:
	docker build --tag $(TESTS_IMAGE) --file tests/Dockerfile tests
	mkdir -p .docker
	touch .docker/tests


clean: .docker/build
	docker run --volume $(SRC):/site $(BUILD_IMAGE) clean
	rm -rf .docker
	docker rm -f alexwlchan.net_serve
	docker rmi --force $(BUILD_IMAGE)

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
		--tty --detach $(BUILD_IMAGE) \
		serve --host 0.0.0.0 --port 5757 --watch

serve-debug: .docker/build
	@# Clean up old running containers
	@docker stop $(SERVE_CONTAINER) >/dev/null 2>&1 || true
	@docker rm $(SERVE_CONTAINER) >/dev/null 2>&1 || true

	docker run \
		--publish 5757:5757 \
		--volume $(SRC):/site \
		--name $(SERVE_CONTAINER) \
		--tty $(BUILD_IMAGE) \
		serve --host 0.0.0.0 --port 5757 --watch

publish: build

deploy: publish
	rsync \
		--archive \
		--verbose \
		--compress \
		--delete \
		--rsh="ssh$(SSHOPTS)" \
		src/_site/ "$(RSYNC_USER)"@"$(RSYNC_HOST)":"$(RSYNC_DIR)"


.PHONY: clean build watch serve serve-debug publish deploy

DOCKER_IMAGE = alexwlchan/alexwlchan.net

RSYNC_HOST = 139.162.244.147
RSYNC_USER = alexwlchan
RSYNC_DIR = /home/alexwlchan/sites/alexwlchan.net

ROOT = $(shell git rev-parse --show-toplevel)

.docker/build:
	docker build --tag $(DOCKER_IMAGE) .
	mkdir -p .docker
	touch .docker/build


clean: .docker/build
	docker run --volume $$(pwd):/site $(DOCKER_IMAGE) clean
	rm -rf .docker
	docker rm -f alexwlchan.net_serve
	docker rmi --force $(DOCKER_IMAGE)

build: .docker/build
	docker run --volume $$(pwd):/site $(DOCKER_IMAGE) build

serve: .docker/build
	# Clean up old running containers
	@docker stop alexwlchan.net_serve >/dev/null || true
	@docker rm alexwlchan.net_serve >/dev/null || true

	docker run \
		--publish 5757:5757 \
		--volume $(ROOT):/site \
		--name alexwlchan.net_serve \
		--tty --detach $(DOCKER_IMAGE) \
		serve --host 0.0.0.0 --port 5757 --watch

publish: specktre-assets build

deploy: publish
	rsync \
		--archive \
		--verbose \
		--compress \
		--delete \
		--rsh="ssh$(SSHOPTS)" \
		_site/ "$(RSYNC_USER)"@"$(RSYNC_HOST)":"$(RSYNC_DIR)"


.PHONY: clean build watch serve stop publish deploy

include _specktre/Makefile

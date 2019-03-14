export DOCKER_IMAGE_NAME = greengloves/alexwlchan.net
export DOCKER_IMAGE_VERSION = 4
DOCKER_IMAGE = $(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_VERSION)

SERVE_CONTAINER = server

RSYNC_HOST = 139.162.244.147
RSYNC_USER = alexwlchan
RSYNC_DIR = /home/alexwlchan/sites/alexwlchan.net

ROOT = $(shell git rev-parse --show-toplevel)
SRC = $(ROOT)/src
DST = $(ROOT)/_site

publish-docker:
	python3 publish_docker_image.py

build:
	docker run --volume $(ROOT):$(ROOT) --workdir $(ROOT) $(DOCKER_IMAGE) build

stop:
	@# Clean up old running containers
	@docker stop $(SERVE_CONTAINER) >/dev/null 2>&1 || true
	@docker rm $(SERVE_CONTAINER) >/dev/null 2>&1 || true

serve: stop
	docker run \
		--publish 5757:5757 \
		--volume $(ROOT):$(ROOT) \
		--workdir $(ROOT) \
		--name $(SERVE_CONTAINER) \
		--hostname $(SERVE_CONTAINER) \
		--tty --rm $(DOCKER_IMAGE) \
		serve --host $(SERVE_CONTAINER) --port 5757 --watch --drafts --incremental

publish-drafts:
	docker run \
		--volume $(ROOT):$(ROOT) \
		--workdir $(ROOT) \
		--volume ~/.gitconfig:/root/.gitconfig \
		--volume ~/.ssh:/root/.ssh \
		--tty --rm $(DOCKER_IMAGE) \
		publish-drafts

publish: publish-drafts build

rsync:
	docker run --rm --tty \
		--volume ~/.ssh/id_rsa:/root/.ssh/id_rsa \
		--volume $(DST):/data \
		instrumentisto/rsync-ssh \
		rsync \
		--archive \
		--verbose \
		--compress \
		--delete \
		--exclude=".well-known" \
		--exclude=".DS_Store" \
		--exclude="attic/" \
		--exclude="ideas-for-inclusive-events/" \
		--rsh="ssh -o StrictHostKeyChecking=no -i ~/.ssh/id_rsa" \
		/data/ "$(RSYNC_USER)"@"$(RSYNC_HOST)":"$(RSYNC_DIR)"

deploy: publish rsync

Gemfile.lock: Gemfile
	docker run \
		--volume $(ROOT):$(ROOT) \
		--workdir $(ROOT) \
		--tty --rm $(shell cat Dockerfile | grep FROM | awk '{print $$2}') \
		bundle lock --update

nginx-serve:
	docker run --rm \
		--volume $(ROOT)/infra/alexwlchan.net.nginx.conf:/etc/nginx/nginx.conf \
		--volume $(DST):/usr/share/nginx/html \
		--publish 5858:80 \
		--hostname alexwlchan \
		--name alexwlchan \
		--detach nginx:alpine


include analytics/Makefile
include certs/Makefile
include infra/Makefile


.PHONY: publish-docker build stop serve publish-drafts publish rsync deploy renew-certbot

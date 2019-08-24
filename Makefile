export DOCKER_IMAGE_NAME = greengloves/alexwlchan.net
export DOCKER_IMAGE_VERSION = 12
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
	docker run --tty --rm --volume $(ROOT):$(ROOT) --workdir $(ROOT) $(DOCKER_IMAGE) build

build-drafts:
	docker run --tty --rm --volume $(ROOT):$(ROOT) --workdir $(ROOT) $(DOCKER_IMAGE) build-drafts

lint:
	docker run --tty --rm --volume $(ROOT):$(ROOT) --workdir $(ROOT) $(DOCKER_IMAGE) lint

serve:
	docker run --tty --rm \
		--volume $(ROOT):$(ROOT) \
		--workdir $(ROOT) \
		--publish 5757:5757 \
		$(DOCKER_IMAGE) \
		serve

publish-drafts:
	docker run --tty --rm \
		--volume $(ROOT):$(ROOT) \
		--workdir $(ROOT) \
		--volume ~/.gitconfig:/root/.gitconfig \
		--volume ~/.ssh:/root/.ssh \
		$(DOCKER_IMAGE) \
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
		--exclude="files/" \
		--exclude="ideas-for-inclusive-events/" \
		--rsh="ssh -o StrictHostKeyChecking=no -i ~/.ssh/id_rsa" \
		/data/ "$(RSYNC_USER)"@"$(RSYNC_HOST)":"$(RSYNC_DIR)"
	docker run --rm --tty \
		--volume ~/.ssh/id_rsa:/root/.ssh/id_rsa \
		--volume $(DST)/files:/data \
		instrumentisto/rsync-ssh \
		rsync \
		--archive \
		--verbose \
		--compress \
		--rsh="ssh -o StrictHostKeyChecking=no -i ~/.ssh/id_rsa" \
		/data/ "$(RSYNC_USER)"@"$(RSYNC_HOST)":"$(RSYNC_DIR)/files"

deploy: publish rsync

Gemfile.lock: Gemfile
	docker run \
		--volume $(ROOT):$(ROOT) \
		--workdir $(ROOT) \
		--tty --rm $(shell cat Dockerfile | grep FROM | awk '{print $$2}') \
		bundle lock --update


.PHONY: publish-docker build stop serve publish-drafts publish rsync deploy

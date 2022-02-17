export DOCKER_IMAGE_NAME = greengloves/alexwlchan.net
export DOCKER_IMAGE_VERSION = 19
DOCKER_IMAGE = $(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_VERSION)

SERVE_CONTAINER = server

RSYNC_HOST = 139.162.244.147
RSYNC_USER = alexwlchan
RSYNC_DIR = /home/alexwlchan/sites/alexwlchan.net

ROOT = $(shell git rev-parse --show-toplevel)
SRC = $(ROOT)/src
DST = $(ROOT)/_site

publish-docker:
	python3 scripts/publish_docker_image.py

build:
	docker run --tty --rm \
		--volume $(ROOT):$(ROOT) \
		--workdir $(ROOT) \
		$(DOCKER_IMAGE) build --trace

build-drafts:
	docker run --tty --rm \
		--volume $(ROOT):$(ROOT) \
		--workdir $(ROOT) \
		$(DOCKER_IMAGE) build --trace --drafts

lint:
	docker run --tty --rm \
		--volume $(ROOT):$(ROOT) \
		--workdir $(ROOT) \
		--volume $(ROOT)/src/_plugins/linter.rb:/usr/local/bundle/gems/jekyll-4.2.1/lib/jekyll/commands/linter.rb \
		$(DOCKER_IMAGE) lint
	docker run --rm \
		--volume $(ROOT):/mnt \
		koalaman/shellcheck:stable scripts/*.sh

serve:
	docker run --tty --rm \
		--volume $(ROOT):$(ROOT) \
		--workdir $(ROOT) \
		--publish 5757:5757 \
		$(DOCKER_IMAGE) \
		serve --drafts --incremental --host "0.0.0.0" --port 5757 --skip-initial-build --trace

publish-drafts:
	docker run --tty --rm \
		--volume $(ROOT):$(ROOT) \
		--workdir $(ROOT) \
		--volume $(ROOT)/src/_plugins/publish_drafts.rb:/usr/local/bundle/gems/jekyll-4.2.1/lib/jekyll/commands/publish_drafts.rb \
		--volume ~/.gitconfig:/root/.gitconfig \
		--volume ~/.ssh:/root/.ssh \
		$(DOCKER_IMAGE) publish_drafts

publish: publish-drafts build

deploy: publish lint
	docker run --tty --rm \
		--volume $(ROOT):$(ROOT) \
		--workdir $(ROOT) \
		ghcr.io/williamjacksn/netlify-cli \
		deploy --auth="$NETLIFY_AUTH_TOKEN"

deploy-prod: publish lint
	docker run --tty --rm \
		--volume $(ROOT):$(ROOT) \
		--workdir $(ROOT) \
		ghcr.io/williamjacksn/netlify-cli \
		deploy --prod --auth="$NETLIFY_AUTH_TOKEN"

Gemfile.lock: Gemfile
	docker run \
		--volume $(ROOT):$(ROOT) \
		--workdir $(ROOT) \
		--tty --rm $(shell cat Dockerfile | grep FROM | awk '{print $$2}') \
		bundle lock --update


.PHONY: publish-docker build stop serve publish-drafts publish rsync deploy

export DOCKER_IMAGE_NAME = ghcr.io/alexwlchan/alexwlchan.net
export DOCKER_IMAGE_VERSION = 42
DOCKER_IMAGE = $(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_VERSION)

ROOT = $(shell git rev-parse --show-toplevel)

JEKYLL_VERSION = 4.3.1
JEKYLL_COMMAND_DIR = /usr/local/bundle/gems/jekyll-$(JEKYLL_VERSION)/lib/jekyll/commands

publish-docker:
	ruby scripts/publish_docker_image.rb

html:
	find _site -name '*.avif' -delete
	docker run --tty --rm \
		--volume /var/run/docker.sock:/var/run/docker.sock \
		--volume $(ROOT):$(ROOT) \
		--workdir $(ROOT) \
		$(DOCKER_IMAGE) build --trace

html-drafts:
	find _site -name '*.avif' -delete
	docker run --tty --rm \
		--volume /var/run/docker.sock:/var/run/docker.sock \
		--volume $(ROOT):$(ROOT) \
		--workdir $(ROOT) \
		$(DOCKER_IMAGE) build --trace --drafts

lint:
	docker run --tty --rm \
		--volume $(ROOT):$(ROOT) \
		--workdir $(ROOT) \
		--volume $(ROOT)/src/_plugins/linter.rb:$(JEKYLL_COMMAND_DIR)/linter.rb \
		$(DOCKER_IMAGE) lint

script-lint:
	docker run --rm \
		--volume $(ROOT):/mnt \
		koalaman/shellcheck:stable scripts/*.sh

serve:
	docker run --tty --rm \
		--volume /var/run/docker.sock:/var/run/docker.sock \
		--volume $(ROOT):$(ROOT) \
		--workdir $(ROOT) \
		--publish 5757:5757 \
		$(DOCKER_IMAGE) serve \
			--drafts \
			--incremental \
			--host "0.0.0.0" \
			--port 5757 \
			--skip-initial-build \
			--trace

publish-drafts:
	docker run --tty --rm \
		--volume $(ROOT):$(ROOT) \
		--workdir $(ROOT) \
		--volume $(ROOT)/src/_plugins/publish_drafts.rb:$(JEKYLL_COMMAND_DIR)/publish_drafts.rb \
		--volume ~/.gitconfig:/root/.gitconfig \
		--volume ~/.ssh:/root/.ssh \
		$(DOCKER_IMAGE) publish_drafts

deploy:
	docker run --tty --rm \
		--volume $(ROOT):$(ROOT) \
		--workdir $(ROOT) \
		ghcr.io/williamjacksn/netlify-cli \
		deploy --auth "$(NETLIFY_AUTH_TOKEN)"

deploy-prod:
	docker run --tty --rm \
		--volume $(ROOT):$(ROOT) \
		--workdir $(ROOT) \
		ghcr.io/williamjacksn/netlify-cli \
		deploy --prod --auth "$(NETLIFY_AUTH_TOKEN)"

Gemfile.lock: Gemfile
	docker run \
		--volume $(ROOT):$(ROOT) \
		--workdir $(ROOT) \
		--tty --rm $(shell cat Dockerfile | grep FROM | awk '{print $$2}') \
		bundle lock --update

plugin-tests:
	docker run --tty --rm \
		--entrypoint ruby \
		--volume $(ROOT):$(ROOT) \
		--workdir $(ROOT) \
		$(DOCKER_IMAGE) src/_tests/tests.rb

.PHONY: publish-docker build stop serve publish-drafts publish rsync deploy

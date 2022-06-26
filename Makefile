export DOCKER_IMAGE_NAME = greengloves/alexwlchan.net
export DOCKER_IMAGE_VERSION = 24
DOCKER_IMAGE = $(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_VERSION)

SERVE_CONTAINER = server

ROOT = $(shell git rev-parse --show-toplevel)

# This looks for a line in Gemfile.lock like:
#
#			jekyll (1.2.3)
#
# then extracts the version number from the brackets.  This is
# used to mount custom Jekyll commands inside the container
# at the right location.
#
# It's a slightly roundabout call to grep to avoid using parentheses,
# so I don't have to work out how to escape them inside $(shell …).
JEKYLL_VERSION = $(shell grep 'jekyll ' Gemfile.lock | grep -v '~>' | grep -o '\d.\d.\d')
JEKYLL_COMMAND_DIR = "/usr/local/bundle/gems/jekyll-$(JEKYLL_VERSION)/lib/jekyll/commands"

publish-docker:
	ruby scripts/publish_docker_image.rb

html:
	docker run --tty --rm \
		--volume $(ROOT):$(ROOT) \
		--workdir $(ROOT) \
		$(DOCKER_IMAGE) build --trace

html-drafts:
	docker run --tty --rm \
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
		--volume $(ROOT):$(ROOT) \
		--workdir $(ROOT) \
		--publish 5757:5757 \
		$(DOCKER_IMAGE) \
		serve --drafts --incremental --host "0.0.0.0" --port 5757 --skip-initial-build --trace

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


.PHONY: publish-docker build stop serve publish-drafts publish rsync deploy

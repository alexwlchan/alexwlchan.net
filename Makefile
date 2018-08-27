BUILD_IMAGE = alexwlchan/alexwlchan.net
TESTS_IMAGE = alexwlchan/alexwlchan.net_tests
SERVE_CONTAINER = server

RSYNC_HOST = 139.162.244.147
RSYNC_USER = alexwlchan
RSYNC_DIR = /home/alexwlchan/sites/alexwlchan.net

ROOT = $(shell git rev-parse --show-toplevel)
SRC = $(ROOT)/src
DST = $(ROOT)/_site
TESTS = $(ROOT)/tests

$(ROOT)/.docker/build: Dockerfile install_jekyll.sh install_specktre.sh Gemfile.lock src/_plugins/publish_drafts.rb
	docker build --tag $(BUILD_IMAGE) --build-arg CI=$$CI .
	mkdir -p .docker
	touch .docker/build

$(ROOT)/.docker/tests: tests/Dockerfile tests/*.py tests/requirements.txt
	docker build --tag $(TESTS_IMAGE) --file $(TESTS)/Dockerfile $(TESTS)
	mkdir -p .docker
	touch .docker/tests

.docker/build: $(ROOT)/.docker/build

.docker/tests: $(ROOT)/.docker/tests


tests/requirements.txt: tests/requirements.in
	docker run --volume $(TESTS):/src --rm micktwomey/pip-tools
	touch $(TESTS)/requirements.txt


clean: .docker/build
	docker run --volume $(SRC):/site --rm $(BUILD_IMAGE) clean
	rm -rf .docker
	docker rm --force $(SERVE_CONTAINER)
	docker rmi --force $(BUILD_IMAGE)
	docker rmi --force $(TESTS_IMAGE)

build: .docker/build
	docker run --volume $(ROOT):/$(ROOT) --workdir $(ROOT) $(BUILD_IMAGE) build

stop:
	@# Clean up old running containers
	@docker stop $(SERVE_CONTAINER) >/dev/null 2>&1 || true
	@docker rm $(SERVE_CONTAINER) >/dev/null 2>&1 || true

serve: .docker/build stop
	docker run \
		--publish 5757:5757 \
		--volume $(ROOT):/$(ROOT) \
		--workdir $(ROOT) \
		--name $(SERVE_CONTAINER) \
		--hostname $(SERVE_CONTAINER) \
		--tty --rm --detach $(BUILD_IMAGE) \
		serve --host $(SERVE_CONTAINER) --port 5757 --watch --drafts --incremental

serve-debug: serve
	docker attach $(SERVE_CONTAINER)

publish-drafts: .docker/build
	docker run \
		--volume $(ROOT):/$(ROOT) \
		--workdir $(ROOT) \
		--volume ~/.gitconfig:/root/.gitconfig \
		--volume ~/.ssh:/root/.ssh \
		--tty --rm $(BUILD_IMAGE) \
		publish-drafts

publish: publish-drafts build

deploy: publish
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
		--rsh="ssh -o StrictHostKeyChecking=no -i ~/.ssh/id_rsa" \
		/data/ "$(RSYNC_USER)"@"$(RSYNC_HOST)":"$(RSYNC_DIR)"

test: .docker/tests
	docker run \
		--volume $(ROOT):/$(ROOT) \
		--workdir $(ROOT) \
		--env HOSTNAME=$(SERVE_CONTAINER) \
		--link $(SERVE_CONTAINER) \
		--link alexwlchan \
		--tty --rm $(TESTS_IMAGE)

Gemfile.lock: Gemfile
	docker run \
		--volume $(ROOT):$(ROOT) \
		--workdir $(ROOT) \
		--workdir /site \
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


.PHONY: clean build stop serve serve-debug publish-drafts publish deploy test renew-certbot

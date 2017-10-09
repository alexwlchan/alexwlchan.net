BUILD_IMAGE = alexwlchan/alexwlchan.net
TESTS_IMAGE = alexwlchan/alexwlchan.net_tests
SERVE_CONTAINER = server

RSYNC_HOST = 139.162.244.147
RSYNC_USER = alexwlchan
RSYNC_DIR = /home/alexwlchan/sites/alexwlchan.net

ROOT = $(shell git rev-parse --show-toplevel)
SRC = $(ROOT)/src
TESTS = $(ROOT)/tests

.docker/build: Dockerfile install_jekyll.sh install_specktre.sh Gemfile.lock src/_plugins/publish_drafts.rb
	docker build --tag $(BUILD_IMAGE) .
	mkdir -p .docker
	touch .docker/build

.docker/tests: tests/Dockerfile tests/*.py tests/requirements.txt tests/requirements_extra.txt tests/tox.ini
	docker build --tag $(TESTS_IMAGE) --file $(TESTS)/Dockerfile $(TESTS)
	mkdir -p .docker
	touch .docker/tests


tests/requirements.txt: tests/requirements.in
	docker run --volume $(TESTS):/src --rm micktwomey/pip-tools requirements.in
	touch $(TESTS)/requirements.txt

tests/requirements_extra.txt: tests/requirements_extra.in
	docker run --volume $(TESTS):/src --rm micktwomey/pip-tools requirements_extra.in
	touch $(TESTS)/requirements_extra.txt


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

publish-drafts: .docker/build
	docker run \
		--volume $(ROOT):/repo \
		--volume ~/.gitconfig:/root/.gitconfig \
		--volume ~/.ssh:/root/.ssh \
		--tty $(BUILD_IMAGE) \
		publish-drafts --source=/repo/src

publish: publish-drafts build

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

Gemfile.lock: Gemfile
	docker run \
		--volume $(ROOT):/site \
		--workdir /site \
		--tty $(shell cat Dockerfile | grep FROM | awk '{print $$2}') \
		bundle lock --update

renew-certbot:
	docker run \
		--volume ~/sites/alexwlchan.net:/site \
		--volume ~/.certbot/work:/var/lib/letsencrypt \
		--volume ~/.certbot/logs:/var/logs/letsencrypt \
		--volume ~/.certbot/config:/etc/letsencrypt \
		certbot/certbot certonly --webroot --webroot-path /site -d alexwlchan.net,www.alexwlchan.net

.PHONY: clean build serve serve-debug publish-drafts publish deploy test renew-certbot

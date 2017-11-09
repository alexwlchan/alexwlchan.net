BUILD_IMAGE = alexwlchan/alexwlchan.net
SERVE_CONTAINER = server

RSYNC_HOST = 139.162.244.147
RSYNC_USER = alexwlchan
RSYNC_DIR = /home/alexwlchan/sites/alexwlchan.net

ROOT = $(shell git rev-parse --show-toplevel)
SRC = $(ROOT)/src

$(ROOT)/.docker/build: Dockerfile install_jekyll.sh install_specktre.sh Gemfile.lock src/_plugins/publish_drafts.rb
	docker build --tag $(BUILD_IMAGE) .
	mkdir -p .docker
	touch .docker/build

.docker/build: $(ROOT)/.docker/build

.docker/tests: $(ROOT)/.docker/tests

.docker/flake8: $(ROOT)/.docker/flake8


clean: .docker/build
	docker run --volume $(SRC):/site --rm $(BUILD_IMAGE) clean
	rm -rf .docker
	docker rm --force $(SERVE_CONTAINER)
	docker rmi --force $(BUILD_IMAGE)
	docker rmi --force $(TESTS_IMAGE)

build: .docker/build
	docker run --volume $(SRC):/site $(BUILD_IMAGE) build

stop:
	@# Clean up old running containers
	@docker stop $(SERVE_CONTAINER) >/dev/null 2>&1 || true
	@docker rm $(SERVE_CONTAINER) >/dev/null 2>&1 || true

serve: .docker/build stop
	docker run \
		--publish 5757:5757 \
		--volume $(SRC):/site \
		--name $(SERVE_CONTAINER) \
		--hostname $(SERVE_CONTAINER) \
		--tty --rm --detach $(BUILD_IMAGE) \
		serve --host $(SERVE_CONTAINER) --port 5757 --watch --drafts

serve-debug: serve
	docker attach $(SERVE_CONTAINER)

publish-drafts: .docker/build
	docker run \
		--volume $(ROOT):/repo \
		--volume ~/.gitconfig:/root/.gitconfig \
		--volume ~/.ssh:/root/.ssh \
		--tty --rm $(BUILD_IMAGE) \
		publish-drafts --source=/repo/src

publish: publish-drafts build

deploy: publish
	docker run --rm --tty \
		--volume ~/.ssh/id_rsa:/root/.ssh/id_rsa \
		--volume $(ROOT)/src/_site:/data \
		instrumentisto/rsync-ssh \
		rsync \
		--archive \
		--verbose \
		--compress \
		--delete \
		--exclude=".DS_Store" \
		--rsh="ssh -o StrictHostKeyChecking=no -i ~/.ssh/id_rsa" \
		/data/ "$(RSYNC_USER)"@"$(RSYNC_HOST)":"$(RSYNC_DIR)"

Gemfile.lock: Gemfile
	docker run \
		--volume $(ROOT):/site \
		--workdir /site \
		--tty --rm $(shell cat Dockerfile | grep FROM | awk '{print $$2}') \
		bundle lock --update

renew-certbot:
	docker run --rm \
		--volume ~/sites/alexwlchan.net:/site \
		--volume ~/.certbot/work:/var/lib/letsencrypt \
		--volume ~/.certbot/logs:/var/logs/letsencrypt \
		--volume ~/.certbot/config:/etc/letsencrypt \
		certbot/certbot certonly --webroot --webroot-path /site -d alexwlchan.net,www.alexwlchan.net


include analytics/Makefile
include tests/Makefile


.PHONY: clean build stop serve serve-debug publish-drafts publish deploy test renew-certbot

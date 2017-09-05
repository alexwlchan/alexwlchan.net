DOCKER_IMAGE = alexwlchan/alexwlchan.net

.docker/build:
	docker build --tag $(DOCKER_IMAGE) .
	mkdir -p .docker
	touch .docker/build


clean:
	rm -rf .docker
	docker rmi --force $(DOCKER_IMAGE)

build: .docker/build
	docker run --volume $$(pwd):/site $(DOCKER_IMAGE) build

serve: .docker/build
	docker run \
		--publish 5757:5757 \
		--volume $$(pwd):/site \
		--name alexwlchan.net_serve \
		--tty $(DOCKER_IMAGE) \
		serve --host 0.0.0.0 --port 5757 --watch

publish: specktre-assets build


.PHONY: clean build watch serve publish

include _specktre/Makefile

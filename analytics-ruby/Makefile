ROOT = $(shell git rev-parse --show-toplevel)
ANALYTICS = $(ROOT)/analytics

$(ROOT)/.docker/analytics: $(ANALYTICS)/Dockerfile
	docker build --tag alexwlchan/analytics $(ANALYTICS)
	mkdir -p $(ROOT)/.docker
	touch $(ROOT)/.docker/analytics

analytics-report: $(ROOT)/.docker/analytics
	docker run --rm \
		--volume $(ANALYTICS):/analytics \
		--volume /var/run/docker.sock:/var/run/docker.sock alexwlchan/analytics

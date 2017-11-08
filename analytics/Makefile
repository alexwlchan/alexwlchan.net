ROOT = $(shell git rev-parse --show-toplevel)
ANALYTICS = $(ROOT)/analytics

$(ANALYTICS)/requirements.txt: $(ANALYTICS)/requirements.in
	docker run --volume $(ANALYTICS):/src --rm micktwomey/pip-tools
	touch $(ANALYTICS)/requirements.txt

$(ROOT)/.docker/analytics: $(ANALYTICS)/requirements.txt $(ANALYTICS)/Dockerfile $(ANALYTICS)/analytics.py
	docker build --tag alexwlchan/analytics --file $(ANALYTICS)/Dockerfile $(ANALYTICS)
	mkdir -p $(ROOT)/.docker
	touch $(ROOT)/.docker/analytics

analytics-build: $(ROOT)/.docker/analytics


.PHONY: analytics-build

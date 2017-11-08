ROOT = $(shell git rev-parse --show-toplevel)
ANALYTICS = $(ROOT)/analytics

$(ANALYTICS)/requirements.txt: $(ANALYTICS)/requirements.in
	docker run --volume $(ANALYTICS):/src --rm micktwomey/pip-tools
	touch $(ANALYTICS)/requirements.txt

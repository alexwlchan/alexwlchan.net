ROOT = $(shell git rev-parse --show-toplevel)
ANALYTICS = $(ROOT)/analytics

$(ANALYTICS)/requirements.txt: $(ANALYTICS)/requirements.in
	docker run --rm --volume $(ANALYTICS):/src micktwomey/pip-tools
	touch $(ANALYTICS)/requirements.txt

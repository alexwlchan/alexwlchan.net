ROOT = $(shell git rev-parse --show-toplevel)
CERTS = $(ROOT)/certs


$(CERTS)/requirements.txt: $(CERTS)/requirements.in
	docker run --volume $(CERTS):/src --rm micktwomey/pip-tools
	touch $(CERTS)/requirements.txt

ROOT = $(shell git rev-parse --show-toplevel)
CERTS = $(ROOT)/certs

CERTS_IMAGE = alexwlchan/certbot


$(ROOT)/.docker/certs: $(CERTS)/requirements.txt
	docker build --tag $(CERTS_IMAGE) --file $(CERTS)/Dockerfile $(CERTS)
	mkdir -p .docker
	touch .docker/certs

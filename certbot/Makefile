ROOT = $(shell git rev-parse --show-toplevel)
CERTBOT = $(ROOT)/certbot

$(CERTBOT)/requirements.txt: $(CERTBOT)/requirements.in
	docker run --rm --volume $(CERTBOT):/src micktwomey/pip-tools
	touch $(CERTBOT)/requirements.txt

ROOT = $(shell git rev-parse --show-toplevel)
CERTBOT = $(ROOT)/certbot

$(CERTBOT)/requirements.txt: $(CERTBOT)/requirements.in
	docker run --rm --volume $(CERTBOT):/src micktwomey/pip-tools
	touch $(CERTBOT)/requirements.txt

deps = $(CERTBOT)/requirements.txt $(CERTBOT)/Dockerfile $(CERTBOT)/renew_certs.py

$(ROOT)/.docker/certbot: $(deps)
	docker build --tag alexwlchan/certbot $(CERTBOT)
	mkdir -p $(ROOT)/.docker
	touch $(ROOT)/.docker/certbot

renew-certs: $(ROOT)/.docker/certbot
	docker run --rm --tty \
		--volume $(ROOT):/repo \
		--volume ~/sites:/site \
		--volume ~/.certbot/work:/var/lib/letsencrypt \
		--volume ~/.certbot/logs:/var/logs/letsencrypt \
		--volume ~/.certbot/config:/etc/letsencrypt \
		alexwlchan/certbot

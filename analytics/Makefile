ROOT = $(shell git rev-parse --show-toplevel)
ANALYTICS = $(ROOT)/analytics

$(ANALYTICS)/requirements.txt: $(ANALYTICS)/requirements.in
	docker run --rm --volume $(ANALYTICS):/src micktwomey/pip-tools
	touch $(ANALYTICS)/requirements.txt

deps = $(ANALYTICS)/requirements.txt $(ANALYTICS)/Dockerfile $(ANALYTICS)/reports.py

$(ROOT)/.docker/analytics: $(deps)
	docker build --tag alexwlchan/analytics $(ANALYTICS)
	mkdir -p $(ROOT)/.docker
	touch $(ROOT)/.docker/analytics

analytics-report: $(ROOT)/.docker/analytics
	docker run --rm --volume /var/run/docker.sock:/var/run/docker.sock alexwlchan/analytics --days=7 --limit=15

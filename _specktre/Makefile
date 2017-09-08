SPECKTRE_IMAGE = alexwlchan/specktre

ROOT = $$(git rev-parse --show-toplevel)
SPECKTRE = $$(git rev-parse --show-toplevel)/_specktre

.docker/specktre:
	docker build --tag $(SPECKTRE_IMAGE) $(SPECKTRE)
	mkdir -p .docker
	touch .docker/specktre

specktre-assets: .docker/specktre
	docker run --volume $(ROOT):/site $(SPECKTRE_IMAGE)

.PHONY: specktre-assets

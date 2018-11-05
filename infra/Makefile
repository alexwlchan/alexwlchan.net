ROOT = $(shell git rev-parse --show-toplevel)
INFRA = $(ROOT)/infra

TERRAFORM_IMAGE = hashicorp/terraform:0.11.10


terraform-plan:
	docker run --volume $(INFRA):/data --workdir /data --rm --tty \
		$(TERRAFORM_IMAGE) init
	docker run --volume $(INFRA):/data --workdir /data --rm --tty \
		$(TERRAFORM_IMAGE) plan -out terraform.plan

terraform-apply:
	docker run --volume $(INFRA):/data --workdir /data --rm --tty \
		$(TERRAFORM_IMAGE) apply terraform.plan

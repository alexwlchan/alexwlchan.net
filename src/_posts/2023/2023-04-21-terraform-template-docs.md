---
layout: post
date: 2023-04-21 15:40:25 +00:00
title: Using templates in Terraform to document a deployment
summary: Terraform can fill in placeholders with exact values from your deployment, for easy copy/paste instructions.
tags:
  - terraform
  - documentation
colors:
  index_light: "#7B42BC"
  index_dark:  "#af75fa"
card_attribution: pexels-pixabay-261763.jpg, noun-pencil-5667651-FFFFFF.png
---

I've been doing a bunch of new Terraform recently, and I've started using it to document the deployments it's creating.
In particular, I've started using Terraform to create README files which describe the exact infrastructure it's just created.

Here's my latest example: a README for an API deployment which tells you where to access the app and how to deploy new versions.
All of the instructions (except the initial `docker build`) can be copy/pasted exactly, with no need for the reader to fill in placeholder values.

{%
  picture
  filename="terraform-docs-screenshot.png"
  class="screenshot"
  width="599"
  alt="Screenshot of a README file for a 'semantic-search API'. It includes a URL where the API can be accessed, and then numbered step-by-step instructions for deploying a new version of the API. Each step includes a brief prose description and then a command for the developer to run."
%}

The alternative would be some sort of generic README with placeholder values that the reader has to fill in, which is how a lot of documentation works -- but having them pre-filled is quite nice.
It makes it a little bit quicker to start using whatever resources I've just spun up.

The sort of stuff I put in these READMEs include:

*   Instructions on deploying a new version of the app.
    In the example above, that includes `docker push` and `aws ecs update-service` commands with the exact parameters filled in.

*   How to find logs for the newly-created deployment.
    This is a clickable link to our logging setup, which takes you directly to the logs for this deployment.

*   Example commands to test the app you've just spun up.
    This is normally some snippets using cURL, and it includes steps for fetching any credentials you need from Secrets Manager.

To create this README, I have Terraform render a template file, and I pass in the variables:

```hcl
resource "local_file" "readme" {
  content = templatefile(
    "${path.module}/README.html.tpl",
    {
      name         = var.name
      ecr_repo_url = aws_ecr_repository.api.repository_url
      cluster_name = aws_ecs_cluster.cluster.name
      service_name = module.service.name
      domain_name  = local.domain_name
    }
  )

  filename = "README.html"
}
```

and then I tell the user about it with a Terraform output:

```hcl
output "next_steps" {
  value = <<EOT
Your new API has been created at ${module.api.domain_name}

For instructions on deploying new code, open ${local_file.readme.filename} in your browser
EOT
}
```

When somebody runs `terraform apply`, they see something like this:

```
Apply complete! Resources: 0 added, 0 changed, 0 destroyed.

Outputs:

next_steps = <<EOT
Your new API has been created at semantic-search-1718862681.eu-west-1.elb.amazonaws.com

For instructions on deploying new code, open README.html in your browser
EOT
```

I've found this especially useful for short-lived or experimental deployments, which aren't tied into a more automated or polished build system.
Having some quick instructions for getting them up and running are quite handy.

I'm not going to do this for all the Terraform I write, but I'm quite enjoying it in the places where I have.

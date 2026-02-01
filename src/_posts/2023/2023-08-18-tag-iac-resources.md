---
layout: post
date: 2023-08-18 08:04:30 +00:00
title: Tag your infrastructure-as-code resources with a link to their definitions
summary: Applying a default tag that points to the IaC definition makes it easy to go from the console to the code.
tags:
  - aws
  - terraform
colors:
  index_light: "#016d01"
  index_dark:  "#88a284"
  css_light: "#016d01"
  css_dark:  "#88a284"
card_attribution: https://www.pexels.com/photo/blank-white-tags-with-blue-ribbon-8058551/
---

The aspiration of [infrastructure-as-code tools][iac] is that you use them to manage *everything*.
You create all your resources by writing a file that defines them, and any time you change something, you update the definition in that file.
It's a nice idea, but easier said than done.

Creating the resources with infrastructure-as-code isn't too bad; the tricky part is updating them later.
If you have a large or thorny codebase, it may not be obvious where a particular resource is defined -- when you want to make changes, which file should you update?

If you're in a hurry, it's tempting to make a manual change now, and tell yourself you'll come back to update the code "later" -- when you have more time to find the file -- but "later" rarely comes.

To make this easier, I recommend tagging all your resources with a link to the file where the resource is defined.

[iac]: https://en.wikipedia.org/wiki/Infrastructure_as_code

---

At work, we're managing AWS resources defined in Terraform.
The Terraform AWS Provider supports setting [default tags] -- you write them once, and then they get applied to every resource that can be tagged.
This is what that looks like for us:

```hcl
provider "aws" {
  default_tags {
    tags = {
      TerraformConfigurationURL = "https://github.com/wellcomecollection/aws-account-infrastructure/tree/main/accounts/storage"
    }
  }
}
```

The `TerraformConfigurationURL` points to a specific subfolder of a GitHub repository, which is where this particular set of Terraform configuration files are stored.

If we're looking at a resource in the AWS console, we can look for the `TerraformConfigurationURL` tag.
If it's there, we can follow the URL to find the Terraform where the resource is defined.

This is particularly simple with Terraform and AWS, because of the support for default tags.
It might be more cumbersome if you're using a different tool or managing different types of resources, but I still think it's worth the benefits.

[default tags]: https://www.hashicorp.com/blog/default-tags-in-the-terraform-aws-provider

---

I originally created these tags to solve the "where is this thing defined" problem.
I've found something in the AWS console, I want to make a change to it, and I want to find the Terraform definition so I can manage the change using infrastructure-as-code.
It has been useful for that, but it's also been helpful in other, unexpected ways.
 
On one occasion, they highlighted some resources that were defined in multiple places.
We could see two Terraform configurations fighting over the value of the `TerraformConfigurationURL` tag -- one would set it to A, the other would set it to B, the first would set it back to A, and so on.
This conflict helped us find and delete the duplicate definition.

It's also been a good way to find resources that aren't managed with infrastructure-as-code.
Because this tag should be applied to everything that's managed with Terraform, anything without this tag was probably created some other way.

Some of our AWS infrastructure predates our use of Terraform, and we've been trying to bring it into Terraform -- looking for resources that don't have this tag is one way to do that.
I also check for this tag as part of our security audits, looking for untagged IAM users that might have been created quietly for malicious purposes.

As with any tagging strategy, it's not perfect.
Not every resource supports tagging, and we haven't always remembered to create these tags -- but it's good enough.
We have enough resources using this tag for it to be useful, and it's been handy on plenty of occasions.

---
category: Terraform
date: 2019-01-29 16:07:28 +0000
layout: post
summary: If a 'terraform plan' hangs, adding 'max_retries = 1' can sometimes expose
  the issue.
tags: terraform aws
theme:
  minipost: true
title: Debugging a stuck Terraform plan
---

While working on some Terraform today, I had a problem that it would hang in the `plan` stage.
Adding the following setting to my `provider` block exposed the issue:

```hcl
provider "aws" {
  # other settings
  max_retries = 1
}
```

Rather than retrying a flaky AWS API, it crashed immediately and told me which API had an issue.
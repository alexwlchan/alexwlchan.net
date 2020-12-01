---
layout: post
title: Creating short-lived, temporary roles for experimenting with AWS IAM policy
  documents
tags: aws aws-iam
link: https://github.com/alexwlchan/iam-policy-document-tester
summary: Create short-lived, temporary roles for experimenting with AWS IAM policy documents
---

As part of some recent work, I was experimenting with IAM roles in AWS, and I came up with a way to create short-lived, temporary IAM roles that use a particular IAM policy document.

It goes something like this:

```python
with temporary_iam_credentials(admin_role_arn, policy_document) as credentials:
    # do stuff with your credentials, which are precisely scoped to
    # the provided IAM policy document.
```

The function `temporary_iam_credentials()` gives you a set of temporary AWS credentials, which have the permissions defined by the IAM policy document. You can make API calls using those credentials, and check they behave correctly -- that API calls are allowed or denied as appropriate.

When you're done, it cleans up after itself, so there are no temporary resources left hanging around in your account.

I use it in two ways:

*   To dramatically speed up the flow for developing IAM policy documents. It gives me a fast write-test-debug loop for making changes; much faster than if I was using a more full-featured deployment tool like Terraform or CloudFormation.
*   To temporarily downgrade permissions when doing something potentially risky. If I have an admin role, I can create more tightly-scoped credentials to act as an extra guard rail.

It was a useful experience working with Python's context managers, with using [ExitStack to handle nested context managers](https://www.rath.org/on-the-beauty-of-pythons-exitstack.html), and seeing how quickly IAM can react to changes.

You can find the code [on GitHub](https://github.com/alexwlchan/iam-policy-document-tester), and I've also written a "what I learnt" section in the README.

The "what I learnt" is a new thing I'm trying.
The number of people who have the exact same problem as me -- and will try to use my code to solve it -- is pretty small.
The number of people who have *similar* problems -- and who might benefit from my ideas if not the actual code -- is probably larger.
I'm trying to make my repos more useful for the latter group.

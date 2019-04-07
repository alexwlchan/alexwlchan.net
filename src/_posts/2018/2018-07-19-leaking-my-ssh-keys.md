---
layout: post
date: 2018-07-19 07:38:10 +0000
title: A robot leaked my SSH keys
tags: github opsec security
summary: A cautionary tale of a daft incident where I leaked a set of SSH keys to GitHub.
category: Programming and code
best_of: true
---

A coworker was reviewing one of my pull requests yesterday, when she pointed at the screen and asked, *"Is that meant to be there?"*
Somehow, an SSH private key had appeared in the diff!

The key in question gave push access to our main repository (it was configured as a [deploy key][deploy_key] with write access).
It was only for that repository, and we'd be able to restore everything from local clones; it would just be a massive faff.

I rushed back to my desk to revoke the key and work out what had happened, and I was pleasantly surprised by an email from GitHub (emphasis mine):

> We noticed that a valid SSH private key of yours was committed to a public GitHub repository.
> This key is configured as a deploy key for the wellcometrust/platform repository.
> Publicly disclosing a valid SSH private key would allow other people to interact with this repository, potentially altering data.
>
> **As a precautionary measure, we have unverified the SSH key.**
> You should should generate a new SSH key and add it to the repository.

Comparing timestamps, this email was sent almost as soon as the commit landed.
Attempting to push to the repo using the leaked SSH key would fail.
Even if we'd missed the diff, we were still protected against malicious commits.

I've heard stories of Amazon scanning public GitHub repos for leaked AWS credentials, and proactively revoking them, but I never thought something like that would happen to me.

Thanks for protecting us, GitHub!


## How did this happen?

So how did an SSH private key end up in the commit history?

Nobody had checked it in, accidentally or on purpose.
None of us even had a local copy!

No, our SSH key was leaked by one of our build jobs in Travis CI.

To keep our code tidy, we run a number of autoformatters against our repository ([scalafmt][scalafmt], [terraform fmt][terraform] and [autoflake][autoflake]).
On pull requests, we have a Travis job that runs the autoformatting, puts the changes in a new commit, and pushes the changes to your PR.

To allow Travis to push changes, we give it an SSH private key in an [encrypted zip file][traviszip].
The corresponding public key is configured as a deploy key on our repository.
Travis unencrypts and unzips the file at runtime, and loads the private key into its Git config.

I'd been tweaking our GitHub deploy keys to manage them [with Terraform][tf_key].
Previously the encrypted zip was unpacked into a dedicated (and gitignored) directory; now the files are unpacked into the repo root.
Which is fine... until the autoformat script comes along, and tries to add every change to a new commit.
It saw the private key as a new, untracked file, and included it in the commit.

Oops.

## How do I stop this happening again?

Aside from rotating out the compromised key, I'll be making some changes to avoid a repeat of this exact scenario:

*   Add the private key file to `.gitignore`.
    I should have done this already, I was just lazy.

*   Use `git add --update` instead of `git add --all` in our autoformat script.
    That should stop the script adding random files it finds lying around the repo (which can also include AWS credentials).

*   The autoformat script gets a list of changed files before it decides whether to commit -- if the list is empty, nothing has changed and it can exit early.
    It knows what sort of files should have changed (e.g. only files ending in `.py` for the Python formatter), so I'll change it to error if it spots an unrecognised file.

This isn't [the first time][subprocess] I've made a daft security mistake, and it won't be the last -- and the next one will probably be something completely different.
Best I can hope is that I'll be similarly lucky, and whatever it is won't be an expensive mistake.

[deploy_key]: https://developer.github.com/v3/guides/managing-deploy-keys/#deploy-keys
[scalafmt]: https://scalameta.org/scalafmt/
[terraform]: https://www.terraform.io/docs/commands/fmt.html
[autoflake]: https://pypi.org/project/autoflake/
[traviszip]: https://docs.travis-ci.com/user/encrypting-files/
[tf_key]: https://www.terraform.io/docs/providers/github/r/repository_deploy_key.html
[subprocess]: /2018/05/beware-logged-errors/

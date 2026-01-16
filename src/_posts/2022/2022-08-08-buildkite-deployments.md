---
layout: post
date: 2022-08-08 07:49:39 +00:00
title: How to customise the title of Buildkite builds triggered from GitHub deployments
summary: Getting a more descriptive build label than 'Deployment'.
tags:
  - builds and ci
  - buildkite
---

At work, we use [Buildkite] for all our continuous testing and deployment, including the Wellcome Collection website.
I recently fixed a small annoyance in our setup, and I figured I'd write it up as I couldn't find any other answers to my problem.

When we want to deploy the website, we [create a GitHub Deployment][GHD].
This triggers a Buildkite pipeline that actually deploys the site to AWS.
We deploy in two steps: first to a staging site, then to a prod site -- so we can catch errors before they're in front of users.

The staging and prod deployments are two separate builds in Buildkite, and until recently they were just labelled "Deployment" in the Buildkite dashboard:

{%
  picture
  filename="buildkite_unhelpful.png"
  alt="Two builds for a single commit in the Buildkite dashboard, both labelled 'Deployment'."
  width="720"
%}

If you click through, you can tell if it's a prod or staging deployment -- but it'd be nice if it was obvious from the dashboard.

The key is to set the `description` field when you call the GitHub Deployments API.
Those descriptions appear in Buildkite: for example, we now label our deployments with the environment.

{%
  picture
  filename="buildkite_helpful.png"
  alt="Two builds for a single commit in the Buildkite dashboard, now labelled 'Deployment (prod)' and 'Deployment (staging)'."
  width="720"
%}

[Buildkite]: https://buildkite.com/
[GHD]: https://docs.github.com/en/rest/deployments/deployments#create-a-deployment

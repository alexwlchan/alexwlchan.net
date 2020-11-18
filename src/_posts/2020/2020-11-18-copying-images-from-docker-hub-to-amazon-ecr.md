---
layout: post
date: 2020-11-18 09:41:32 +0000
title: A script to copy images from Docker Hub to Amazon ECR
summary:
tags: docker amazon-ecr aws
link: https://github.com/wellcomecollection/platform-infrastructure/blob/4b16beef44efbe8faa9a62f5459ab6f706e07032/builds/copy_docker_images_to_ecr.py
---

In August, Docker announced they were going to start [rate limiting for Docker image pulls](https://www.docker.com/blog/scaling-docker-to-serve-millions-more-developers-network-egress/) from Docker Hub.
The new limits are being [introduced gradually](https://www.docker.com/blog/what-you-need-to-know-about-upcoming-docker-hub-rate-limiting/), and if you exceed the rate limits, you'll be unable to pull images.

This has caused problems at work -- we've started to hit the rate limits in our automated CI tests.
We use Docker extensively in our tests, and we pull way more images than the free rate limits allow.
We had to choose: pull less images, start paying Docker, or stop using Docker Hub.

Pulling a lot of images is a side-effect of how our CI works -- our CI tasks run on a bunch of short-lived VMs, and each new VM has to pull a fresh set of Docker images.
We could change this, but it'd be a big piece of work.
Pulling less images isn't practical in the short term.

Meanwhile, we're already paying for a Docker Hub alternative -- we pay for ECR, Amazon's managed container registry, part of AWS.
It's where we publish all of the Docker images for our apps.
When our apps run, they pull the images from ECR.
Why not stop using Docker Hub, and start using ECR to pull images in CI?

The images we use in CI are part of the public registry -- not ones we publish ourselves.
**I've written [a Python script](https://github.com/wellcomecollection/platform-infrastructure/blob/4b16beef44efbe8faa9a62f5459ab6f706e07032/builds/copy_docker_images_to_ecr.py) that copies public images from Docker Hub to ECR repositories in our AWS account.**
When our CI runs, it now pulls images from ECR.

Our CI runs inside our AWS account, so we can pull images from ECR without incurring any egress charges.
We also won't hit any rate limits -- although ECR [does have limits](https://docs.aws.amazon.com/AmazonECR/latest/userguide/service-quotas.html), they're much higher than we'll ever need.

I expect the financial cost to be trivial -- we have dozens of ECR repos, and it's still a tiny item on the bill each month.
Spending a few extra cents to mirror some images from Docker Hub will keep our CI running reliably and quickly, so it should be excellent value.

Amazon has talked about creating [a new public container registry](https://aws.amazon.com/blogs/containers/advice-for-customers-dealing-with-docker-hub-rate-limits-and-a-coming-soon-announcement/) based on ECR "within weeks".
That might work as a long-term solution, but our builds were breaking *today*.
Copying the images we use to ECR works as an immediate fix.

If you use AWS, and you're about to be affected by Docker Hub's new rate limits, you might want to consider copying some Docker Hub images into ECR.
My script is designed to be reusable, so hopefully you could use it as a starting point.

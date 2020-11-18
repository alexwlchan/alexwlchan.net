---
layout: post
title: A script to copy images from Docker Hub to Amazon ECR
summary:
tags: docker amazon-ecr aws
link: https://github.com/wellcomecollection/platform-infrastructure/blob/4b16beef44efbe8faa9a62f5459ab6f706e07032/builds/copy_docker_images_to_ecr.py
---

In August, Docker announced they were going to start [rate limiting for Docker container pulls](https://www.docker.com/blog/scaling-docker-to-serve-millions-more-developers-network-egress/) from Docker Hub.
The new limits are being [introduced gradually](https://www.docker.com/blog/what-you-need-to-know-about-upcoming-docker-hub-rate-limiting/), and if you exceed the rate limits, you'll be unable to pull images.

This has started to cause problems at work -- we've started to hit the rate limits in our CI suite.
We use Docker extensively in our tests, and we pull way more images than the free rate limits allow.
We had to choose: stop using Docker Hub, or start paying Docker.

We're already paying for a container registry -- ECR is Amazon's managed container registry, part of AWS, and it's where we publish all of our Docker images.
(Think Docker Hub, but private.)
When we run our apps inside AWS, we pull the images from ECR.
Why not reuse ECR for our CI?

**I've written [a Python script](https://github.com/wellcomecollection/platform-infrastructure/blob/4b16beef44efbe8faa9a62f5459ab6f706e07032/builds/copy_docker_images_to_ecr.py) that copies images from Docker Hub to ECR repositories in our AWS account.**
When our CI runs, it now pulls images from ECR, not Docker Hub.

Our CI runs on EC2 instances inside our AWS account, so we can pull images from ECR without incurring egress charges.
We also won't hit any rate limits for pulling images -- although ECR [does have limits](https://docs.aws.amazon.com/AmazonECR/latest/userguide/service-quotas.html), they're much higher than we'll ever need.

I expect the financial cost to be trivial -- we have dozens of ECR repos, and it's still a tiny item on the bill each month.
Spending a few cents to mirror some images from Docker Hub will keep our CI running reliably and quickly, so it should be excellent value.

Amazon has talked about creating [a new public container registry](https://aws.amazon.com/blogs/containers/advice-for-customers-dealing-with-docker-hub-rate-limits-and-a-coming-soon-announcement/) based on ECR "within weeks".
That might be a better long-term solution, but our builds were breaking *today*.
Copying the images we use to ECR works as an immediate fix.

If you use AWS, and you're about to be affected by Docker Hub's new rate limits, you might want to consider copying some Docker Hub images into ECR repositories.
My script is designed to be reusable, so hopefully you could use it as a starting point.

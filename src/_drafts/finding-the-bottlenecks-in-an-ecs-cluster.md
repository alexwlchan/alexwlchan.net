---
layout: post
title: Finding the bottlenecks in an ECS cluster
summary:
category: Amazon Web Services
---

At Wellcome, we use Amazon's EC2 Container Service (ECS) to run some of our applications.
ECS is a service for orchestrating Docker containers -- you describe a collection of containers you want to run, and then ECS finds somewhere to run them.

If you look in the ECS console, you can see graphs of the CPU and memory utilisation for your containers:

<img src="/images/2020/ecs_metric_graphs.png" style="width: 616px;">

At a glance, this gives a clue about whether any apps are bottlenecked by CPU or memory.
In this case, we can see there were periods when the app was using 100% of its provisioned CPU and memory -- so we might be able to make it run faster by increasing its available resources.
But we have a lot of apps in ECS, and clicking around in the console is slow and boring.
These stats are all available through AWS APIs -- so could we get this data programatically?

I've written a script that gives me a quick snapshot of CPU and memory usages across an ECS cluster, and highlights possible bottlenecks:

<img src="/images/2020/ecs_terminal_graph.png" style="width: 644px; border: 1px solid #ccc;">

Let's walk through how I wrote this script.



## ECS terminology

In ECS, a [*task definition*][task] describes a collection of containers you want to run together, and any of the parameters you need to start them.
For example, "run three app containers and one nginx container".
It might include the Docker image you want to run, the CPU and memory to provision, or the environment variables to pass to the containers.

A [*service*][service] tells ECS how many instances of a task definition to run.
The ECS scheduler will start or stop containers to give you the desired number of tasks in a service.
This includes restarting containers if a task unexpectedly stops running.

An ECS [*cluster*][cluster] is a collection of tasks and services that run together.
For example, all the tasks in a cluster might run on the same container hosts.

[task]: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definitions.html
[service]: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_services.html
[cluster]: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/clusters.html



## Looking up a single CPU/memory utilization metric

The graph in the ECS console is created from CloudWatch Metrics.
If you click the title of the graph, you're taken to the CloudWatch console, where you can see a bigger, interactive version of the graph:

<img src="/images/2020/ecs_cloudwatch_metrics.png">

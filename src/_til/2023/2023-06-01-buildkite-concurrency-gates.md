---
layout: til
title: Use concurrency gates to prevent concurrent deployments
date: 2023-06-01 20:37:05 +00:00
tags:
  - buildkite
---
Concurrency gates are a Buildkite feature you can use to "lock" certain tasks, e.g. ensure that you're only deploying one copy of an app at a time.
The pattern is described [in a Buildkite blog post](https://buildkite.com/blog/concurrency-gates), but it took actually implementing it [in Wellcome's front-end builds](https://github.com/wellcomecollection/wellcomecollection.org/pull/9884) to wrap my head around it.

Here's a simplified version of the Buildkite YAML from that PR, with my comments intact -- which are what helped me understand it.

```yaml
steps:
  - label: "Deploy to prod environment"
    command: "deploy_to_prod_environment.sh"

    # These three lines create a "lock" around this pipeline.
    #
    # This means that once a deployment starts to an environment,
    # no other builds will deploy to that environment until this
    # deployment is complete and has run the end-to-end tests.
    #
    # == How it works ==
    #
    # This uses the "concurrency gate" pattern described in the Buildkite blog
    # here: https://buildkite.com/blog/concurrency-gates
    #
    # Once this job starts running, this build has to either:
    #
    #   1)  fail, or
    #   2)  complete all the other tasks in this concurrency group -- which is
    #       just the "Complete!" task at the end of the pipeline
    #
    # before any other build is allowed to run tasks in this concurrency group.
    # This means no other build can start a new deployment until this deployment
    # is complete.
    concurrency_group: "front-end-deployment-gate"
    concurrency: 1

  - wait

  - label: "Run end-to-end tests on the new deployment"
    command: "run_e2e_tests.sh"

  - wait

  - label: "Complete the deployment"
    command: echo "Deployment complete!"

    # This is the second half of the concurrency gate described above.
    #
    # Buildkite won't let any other pipelines run in this concurrency group until
    # this step has run (or the entire deployment has failed).
    #
    # When this step completes, it "unlocks" the deployment and allows other
    # deployments to begin.
    concurrency_group: "front-end-deployment-${BUILDKITE_GITHUB_DEPLOYMENT_ENVIRONMENT}-gate"
    concurrency: 1
```
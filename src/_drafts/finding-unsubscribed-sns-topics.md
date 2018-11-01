---
layout: post
title: Finding SNS topics without any subscriptions
tags: golang aws
summary: I'm trying out Go, and I wrote a tool to help me find SNS topics that don't have any subscriptions.
---

I make regular use of [Amazon SNS][sns] when working with message queues in AWS.

SNS is a notification service.
A user can send a notification to a *topic*.
Each topic can have multiple *subscribers*, which receive a copy of every message sent to the topic -- something like an HTTP endpoint, an email address, or an Amazon SQS queue.
Sending a single notification can go to multiple places.

<img src="/images/2018/sns-notifications.png" style="max-width: 600px;">

We use SNS as an intermediary for SQS at work.
Rather than sending a message directly to a queue, we send messages to an SNS topic, and the queue subscribes to the topic.
Usually there's a 1-to-1 relationship between topics and queues, but SNS is useful if we ever want to do some debugging or monitoring.
We can create a second subscription to the topic, get a copy of the messages, and inspect them without breaking the original queue.

A more common use case is something like push notifications on your phone.
For example, when a game sends you a notification to tell you about new content -- that could be powered by SNS.

We've had a few bugs recently where the subscription between the SNS topic and SQS queue gets broken.
When nothing subscribes to a topic, any notifications it receives are silently discarded -- because there's nowhere for them to be sent.

I wanted a way to detect if this had happened – do we have any topics without any subscribers?

You can see this information in the console, but it's a little cumbersome.
Anything more than a handful of topics becomes unwieldy, so I wrote a script.
Normally I'd reach for Python, but I'm trying to learn some new languages, so I decided to write it in Go.
I've only dabbled in Go, so this was a chance to write a useful program and test my Go skills.

In this post, I'll explain how I wrote the script.
Even if the Go isn't very idiomatic, I hope it's a useful insight into how I write this sort of thing.
And it's helpful for me to write it, because it forces me to understand exactly how this code works.

[sns]: https://en.wikipedia.org/wiki/Amazon_Simple_Notification_Service

<!-- summary -->


## Brief interlude: installing Go

I think most people install Go directly on their computer, using the [official installer][installer] for their platform of choice.
I didn't do that.

I'm almost obsessive about running everything in Docker, so I set up some Docker images to build and run my Go program.
They're still a work-in-progress, so I won't explain them for now -- but if my process doesn't exactly match yours, that might be why.

[installer]: https://golang.org/doc/install


## Back to the script

The first thing to do is to get the [AWS SDK for Go][sdk].
If you have Git installed, you can install it with the built-in package manager:

```console
$ go get github.com/aws/aws-sdk-go
```

First we need a client for interacting with the SNS API.
I found the [docs for the SNS service][sns_service] a little unclear -- it says "use the New function to create a new service client", but I'd have preferred example code.
I found a more instructive example in the [session package docs][session_docs], but it wasn't immediately clear that I should be looking there:

```go
import (
    "github.com/aws/aws-sdk-go/aws/session"
    "github.com/aws/aws-sdk-go/service/sns"
)

func main() {
    sess := session.Must(session.NewSession())
    snsClient := sns.New(sess)
    ...
}
```

I was a bit surprised that it only reads from ~/.aws/credentials by default -- you have to set the region by environment variable, specify it explicitly, or tell the SDK to look in ~/.aws/config.
I worked it out, but the Python SDK reads from both files by default, and it took me a moment to spot the difference.

I'm sharing ~/.aws/credentials into my Docker container, and setting the region by environment variable.

Next, let's get all the topics in this AWS region.
Because I want to find the topics with zero subscriptions, I really want to track how many subscriptions each topic has.
Let's store the topics in a map from their ARN to subscription count:

```go
subscriptionCountsByTopicArn := make(map[string]int)
```

And this is the code for populating the map:

```go
import os

func main {
    ...
    listTopicsParams := sns.ListTopicsInput{}
    listTopicsErr := snsClient.ListTopicsPages(
        &listTopicsParams,
        func(page *sns.ListTopicsOutput, lastPage bool) bool {
            for _, topic := range page.Topics {
                subscriptionCountsByTopicArn[*topic.TopicArn] = 0
            }
            return true
        })

    if listTopicsErr != nil {
        fmt.Println("Error describing topics: %v", listTopicsErr)
        os.Exit(1)
    }
    ...
}
```

Let's break this down.

The key method here is [sns.ListTopicPages][ListTopicPages], which provides a wrapper around the ListTopics API.
It takes two parameters -- a pointer to an instance of ListTopicsInput, and a function that handles each page of the response.
Within the function, you do any processing you want to on that page, and then the ListTopicPages fetches the next page for you.
It's a useful wrapper around the pagination APIs.

For the parameters, I'm using the defaults -- the ListTopicsInput struct doesn't have any interesting options.
The ampersand gives me the *address* of the object, so I'm passing a *pointer* into the function.
This looks similar to [pass by reference][pass_by_ref] in C, but I'm sure there are subtleties in Go that I haven't learnt yet.

The handler function gets a *pointer* to an instance of ListTopicsOutput, and a boolean.
In the example in the docs, this is called `LastPage`, so I'm guessing this tells you whether you're on the last page of the response?
The docs aren't clear on this point.
I don't use that parameter, so I tried using an underscore for the name.
I'm pleased to learn that works fine in Go!

Within the handler, I'm iterating over the list of topics, and initialising the subscription count map to 0 for each topic ARN.
(An ARN is the [Amazon Resource Name][arn], a unique ID for anything created in AWS.)

Finally, I have to check if ListTopicsPages returned an error.
Like C, Go doesn't have exceptions, it has error returns -- you have to explicitly check for errors yourself.
This is different from what I'm used to; it'll take a while to adjust.
If I do find an error, I exit immediately -- this script is too short to merit more sophisticated error handling.

At the end of this code, I have a map with all of the topic ARNs as keys, and the value of each is 0:

```
map[
  arn:aws:sns:eu-west-1:760097843905:load_test_failure_alarm:0
  arn:aws:sns:eu-west-1:760097843905:shared_alb_client_error_alarm:0
  ... ]
```

[session_docs]: https://docs.aws.amazon.com/sdk-for-go/api/aws/session/#hdr-Creating_Sessions

[sdk]: https://aws.amazon.com/sdk-for-go/
[sns_service]: https://docs.aws.amazon.com/sdk-for-go/api/service/sns/#hdr-Using_the_Client
[session_package]: https://docs.aws.amazon.com/sdk-for-go/api/aws/session/
[ListTopicPages]: https://docs.aws.amazon.com/sdk-for-go/api/service/sns/#SNS.ListTopicsPages
[pass_by_ref]: https://en.wikipedia.org/wiki/Evaluation_strategy#Call_by_reference
[arn]: https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html


## Putting it all together

This is the final code:

```go
package main

import (
    "fmt"
    "github.com/aws/aws-sdk-go/aws/session"
    "github.com/aws/aws-sdk-go/service/sns"
    "os"
)

func main() {
    sess := session.Must(session.NewSession())
    snsClient := sns.New(sess)

    subscriptionCountsByTopicArn := make(map[string]int)

    listTopicsParams := sns.ListTopicsInput{}
    listTopicsErr := snsClient.ListTopicsPages(
        &listTopicsParams,
        func(page *sns.ListTopicsOutput, lastPage bool) bool {
            for _, topic := range page.Topics {
                subscriptionCountsByTopicArn[*topic.TopicArn] = 0
            }
            return true
        })

    if listTopicsErr != nil {
        fmt.Println("Error describing topics: %v", listTopicsErr)
        os.Exit(1)
    }

    listSubscriptionParams := &sns.ListSubscriptionsInput{}
    listSubscriptionsErr := snsClient.ListSubscriptionsPages(
        listSubscriptionParams,
        func(page *sns.ListSubscriptionsOutput, lastPage bool) bool {
            for _, subscription := range page.Subscriptions {
                subscriptionCountsByTopicArn[*subscription.TopicArn] += 1
            }
            return true
        })

    if listSubscriptionsErr != nil {
        fmt.Println("Error describing subscriptions: %v", listSubscriptionsErr)
        os.Exit(1)
    }

    for topicArn, subscriptionCount := range subscriptionCountsByTopicArn {
        if subscriptionCount == 0 {
            fmt.Println(topicArn)
        }
    }
}
```

I might cringe at it in six months, but for now it does the job, and I know how it works.
For an early attempt at the language, I'll take it.

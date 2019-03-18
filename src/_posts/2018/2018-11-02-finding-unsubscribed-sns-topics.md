---
layout: post
date: 2018-11-02 10:42:04 +0000
title: Finding SNS topics without any subscriptions
tags: golang aws
summary: I'm trying out Go, and I wrote a tool to help me find SNS topics that don't have any subscriptions.
category: Working with AWS
---

I make regular use of [Amazon SNS][sns] when working with message queues in AWS.

SNS is a notification service.
A user can send a notification to a *topic*.
Each topic can have multiple *subscribers*, which receive a copy of every message sent to the topic -- something like an HTTP endpoint, an email address, or an Amazon SQS queue.
Sending a single notification can go to multiple places.

<figure style="max-width: 600px;">
  {%
    image :filename => "sns-notifications.png",
    :alt => "A flow diagram showing how SNS works."
  %}
</figure>

A common use case is something like push notifications on your phone.
For example, when a game sends you a notification to tell you about new content -- that could be powered by SNS.

We use SNS as an intermediary for SQS at work.
Rather than sending a message directly to a queue, we send messages to an SNS topic, and the queue subscribes to the topic.
Usually there's a 1-to-1 relationship between topics and queues, but SNS is useful if we ever want to do some debugging or monitoring.
We can create a second subscription to the topic, get a copy of the messages, and inspect them without breaking the original queue.

We've had a few bugs recently where the subscription between the SNS topic and SQS queue gets broken.
When nothing subscribes to a topic, any notifications it receives are silently discarded -- because there's nowhere for them to be sent.

I wanted a way to detect if this had happened – do we have any topics without any subscribers?

You can see this information in the console, but it's a little cumbersome.
Anything more than a handful of topics becomes unwieldy, so I wrote a script.
Normally I'd reach for Python, but I'm trying to learn some new languages, so I decided to write it in Go.
I've only dabbled in Go, and this was a chance to write a useful program and test my Go skills.

In this post, I'll explain how I wrote the script.
Even if the Go isn't very idiomatic, I hope it's a useful insight into how I write this sort of thing, and what I'm learning as a Go novice.

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
I worked it out, but the Python SDK reads from both files by default, and it took me a moment to realise the difference.

I'm sharing ~/.aws/credentials into my Docker container, and setting the region by environment variable.

Next, let's get all the topics in this AWS region.
Because I want to find the topics with zero subscriptions, I really want to track how many subscriptions each topic has.
Let's store the topics in a map from their ARN to subscription count.
(An ARN is the [Amazon Resource Name][arn], a unique ID for anything created in AWS.)

```go
subscriptionCountsByTopicArn := make(map[string]int)
```

And this is the code for populating the map:

```go
import "os"

func main {
    ...
    listTopicsParams := sns.ListTopicsInput{}
    listTopicsErr := snsClient.ListTopicsPages(
        &listTopicsParams,
        func(page *sns.ListTopicsOutput, _lastPage_ bool) bool {
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

For ListTopicsInput, I'm using the defaults -- there aren't any interesting options.
The ampersand gives me the *address* of the object, so I'm passing a *pointer* into the function.
This looks similar to [pass by reference][pass_by_ref] in C, but I'm sure there are subtleties in Go that I haven't learnt yet.

The handler function gets a *pointer* to an instance of ListTopicsOutput, and a boolean.
In the example in the docs, this is called `lastPage`, so I'm guessing this tells you whether you're on the last page of the response?
The docs aren't clear on this point.
I don't use that parameter, so I tried using an underscore for the name.
I'm pleased to learn that works fine in Go!

Within the handler, I'm iterating over the list of topics, and initialising the subscription count map to 0 for each topic ARN.

Finally, I have to check if ListTopicsPages returned an error.
Like C, Go doesn't throw exceptions, it has error returns -- you have to explicitly check for errors yourself.
This is different from what I'm used to; it'll take a while to adjust.
If I do find an error, I exit immediately -- this script is too short to need more sophisticated error handling.

At the end of this code, I have a map with all of the topic ARNs as keys, and the value of each is 0:

```
map[
  arn:aws:sns:eu-west-1:760097843905:load_test_failure_alarm:0
  arn:aws:sns:eu-west-1:760097843905:shared_alb_client_error_alarm:0
  ... ]
```

Next, let's iterate over all the subscriptions, and tally the subscriptions associated with each topic:

```go
listSubscriptionParams := sns.ListSubscriptionsInput{}
listSubscriptionsErr := snsClient.ListSubscriptionsPages(
    &listSubscriptionParams,
    func(page *sns.ListSubscriptionsOutput, _ bool) bool {
        for _, subscription := range page.Subscriptions {
            subscriptionCountsByTopicArn[*subscription.TopicArn] += 1
        }
        return true
    })

if listSubscriptionsErr != nil {
    fmt.Println("Error describing subscriptions: %v", listSubscriptionsErr)
    os.Exit(1)
}
```

This is quite similar to the first loop -- here the key method is ListSubscriptionsPages, which is a wrapper for the ListSubscriptions API.

As before I'm passing a pointer to some options that use all the defaults, then a handler that processes each page of the response.
This time, I'm incrementing the value in the map rather than setting it to 0.

You'll notice I don't check if the topic ARN is already in the map before I try to increment it.
Occasionally a subscription doesn't get deleted when the topic is deleted, and you have subscriptions pointing at a non-existent topic.
In most languages, accessing a key in a map that doesn't exist is an error -- but not so in Go.

If you try to look up a key in a map that doesn't exist, Go returns the nil value (which is 0 for an int).
And because `+= 1` is really syntactic sugar for:

```go
existingValue := subscriptionCountsByTopicArn[*subscription.TopicArn]
subscriptionCountsByTopicArn[*subscription.TopicArn] = existingValue + 1
```

When the program looks up the key for a topic that wasn't found by ListTopics, it gets the nil value (0), then it adds 1 and stores that back in the map.
In this case that's fine, because I'm only interested in topics with zero subscriptions, so an extra non-zero entry in this map is irrelevant.
In other cases, I'll need to remember that Go handles maps in an unusual way.

The error handling is then very similar to when I listed the topics, just with a different error message.

Finally, let's iterate over the map and print any of the topics with no subscriptions.
My first attempt was to write a standard Go `range` loop:

```go
def main {
    ...
    for topicArn, subscriptionCount := range subscriptionCountsByTopicArn {
        if subscriptionCount == 0 {
            fmt.Println(topicArn)
        }
    }
}
```

What I discovered is that iterating over a map gives a random iteration order -- [deliberately so][maps_in_action].
This is slightly annoying, because it's difficult to see if the output has changed over different calls of the script.
To get around this, we build a list of the keys, sort it ourselves, then iterate over that:

```go
import "sort"

def main {
    ...

    var allTopicArns []string
    for topicArn := range subscriptionCountsByTopicArn {
        allTopicArns = append(allTopicArns, topicArn)
    }

    sort.Strings(allTopicArns)

    for _, topicArn := range allTopicArns {
        if subscriptionCountsByTopicArn[topicArn] == 0 {
            fmt.Println(topicArn)
        }
    }
}
```

I could have built this list while I was paging through ListTopics, but I prefer having it all in one place.
It makes it clearer why I'm building a list of topic ARNs as well as the map.

And that completes the script.
To recap, we've:

1.  Listed all the topics in SNS
2.  Listed all the subscriptions that SNS knows about
3.  Created a map that tallies the number of subscriptions associated with each topic
4.  Printed the ARN of every topic that has no subscriptions

When I ran this script, I did indeed find several topics that didn't have any subscriptions, and I fixed them before we lost any more notifications.
Success!

[session_docs]: https://docs.aws.amazon.com/sdk-for-go/api/aws/session/#hdr-Creating_Sessions
[sdk]: https://aws.amazon.com/sdk-for-go/
[sns_service]: https://docs.aws.amazon.com/sdk-for-go/api/service/sns/#hdr-Using_the_Client
[session_package]: https://docs.aws.amazon.com/sdk-for-go/api/aws/session/
[ListTopicPages]: https://docs.aws.amazon.com/sdk-for-go/api/service/sns/#SNS.ListTopicsPages
[pass_by_ref]: https://en.wikipedia.org/wiki/Evaluation_strategy#Call_by_reference
[arn]: https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html
[maps_in_action]: https://blog.golang.org/go-maps-in-action#TOC_7.


## Putting it all together

This is the final code:

```go
package main

import (
    "fmt"
    "github.com/aws/aws-sdk-go/aws/session"
    "github.com/aws/aws-sdk-go/service/sns"
    "os"
    "sort"
)

func main() {
    sess := session.Must(session.NewSession())
    snsClient := sns.New(sess)

    subscriptionCountsByTopicArn := make(map[string]int)

    listTopicsParams := sns.ListTopicsInput{}
    listTopicsErr := snsClient.ListTopicsPages(
        &listTopicsParams,
        func(page *sns.ListTopicsOutput, _ bool) bool {
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
        func(page *sns.ListSubscriptionsOutput, _ bool) bool {
            for _, subscription := range page.Subscriptions {
                subscriptionCountsByTopicArn[*subscription.TopicArn] += 1
            }
            return true
        })

    if listSubscriptionsErr != nil {
        fmt.Println("Error describing subscriptions: %v", listSubscriptionsErr)
        os.Exit(1)
    }

    // Print the topic ARNs and subscriptions.  Note that Go randomises map iteration
    // order by default, so we have to sort the keys ourselves:
    // https://blog.golang.org/go-maps-in-action#TOC_7.
    var allTopicArns []string
    for topicArn := range subscriptionCountsByTopicArn {
        allTopicArns = append(allTopicArns, topicArn)
    }

    sort.Strings(allTopicArns)

    for _, topicArn := range allTopicArns {
        if subscriptionCountsByTopicArn[topicArn] == 0 {
            fmt.Println(topicArn)
        }
    }
}
```

Writing this post was a useful exercise for me.
It forced me to really understand what I was doing, and not just handwave an example I'd copied from somewhere else.
Plus, I made several improvements to the original code while writing the post.

I tried using an underscore for an unused variable in the handler functions (previously it was still called `lastPage`, because that's what the example in the docs used), and that's something I'll use again.

I learnt about the iteration order of maps, which is something I take for granted elsewhere.

And I had to think about the way Go handles map keys that don't exist (when iterating over the subscriptions).
In this case, you could ignore it and it's fine, but that won't always be the case.
Learning about that now is bound to save me a headache later.

(It occurred to me that if all you care about is whether a topic has any subscriptions, you could simplify the map further and just record a boolean "does this topic have any subscriptions".
But then I'd lose the lesson about non-existent keys, so I decided to leave it as-is.)

Overall, I'm pretty pleased with this code.
It does the job I wanted, fixed a few bugs in our AWS estate, and I've learnt a lot about Go by writing it.
Not bad for a Thursday evening.

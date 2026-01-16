---
layout: post
date: 2023-04-11 21:04:12 +00:00
title: Filtering AWS CLI output by tags using jq
summary: Using `from_entries` is a nicer way to deal with the list of Name/Value pairs returned by the AWS CLI.
tags:
  - jq
colors:
  index_dark:  "#d4d1c0"
  index_light: "#46362e"
---

{% comment %}
  Card image from https://www.pexels.com/photo/brown-paper-tag-lot-1111315/
{% endcomment %}

Recently I was writing a shell script to deal with the AWS CLI, and I wanted to filter the list of results [using jq][jq].
Specifically, I wanted to filter using some of the AWS tags, which are a bit unwieldy -- although the tags form a set of key/value pairs, they're returned as a list of objects with `Key`/`Value` keys.

For example, given this list of two instances, how do I get the JSON object for the bastion host?

```
[
  {
    "InstanceId": "i-123456789",
    "Tags": [
      {
        "Key": "Environment",
        "Value": "Production"
      },
      {
        "Key": "Name",
        "Value": "container-host_a88676"
      }
    ]
  },
  {
    "InstanceId": "i-987654321",
    "Tags": [
      {
        "Key": "Environment",
        "Value": "Production"
      },
      {
        "Key": "Name",
        "Value": "bastion-host_517e67"
      }
    ]
  }
]
```

I found a few snippets around the Internet, but they all did a complicated combination of `map` and `select`.
I cobbled this together, which seemed to work, but I had to really stare at it to understand what it was doing:

```shell
jq 'map(select(.Tags[] | select(.Key=="Name") | .Value | startswith("bastion-")))'
```

I started reading the jq documentation to understand exactly how this worked, when I stumbled upon [a much better way to do this][from_entries]:

{%
  picture
  filename="jq_from_entries.png"
  width="531"
  alt="A screenshot of the jq documentation, explaining the from_entries, to_entries and with_entries filters, including a couple of examples."
  class="screenshot"
%}

I can use the `from_entries` filter as an intermediate transformation step to turn the tags into an object.
This simplifies the structure of `Tags`, for example:

```shell
jq 'map(.Tags |= from_entries)'
```

[transforms the JSON into][example1]:

```
[
  {
    "InstanceId": "i-123456789",
    "Tags": {
      "Environment": "Production",
      "Name": "container-host_a88676"
    }
  },
  {
    "InstanceId": "i-987654321",
    "Tags": {
      "Environment": "Production",
      "Name": "bastion-host_517e67"
    }
  }
]
```

I can then work with the tags as an object, and [add my filter by name][example2]:

```shell
jq 'map(.Tags |= from_entries) | map(select(.Tags.Name | startswith("bastion-")))'
```

or I can combine it into a single step, [like so](https://jqplay.org/s/TGhRjo7Riuz):

```shell
jq 'map(select(.Tags | from_entries | .Name | startswith("bastion-")))'
```

I find both of those easier to understand than the doubly-nested `select()` I had in my first snippet.

[jq]: https://stedolan.github.io/jq/manual/
[from_entries]: https://stedolan.github.io/jq/manual/#to_entries,from_entries,with_entries
[example1]: https://jqplay.org/s/omejYgBUWcw
[example2]: https://jqplay.org/s/f9KqBJ9mbR2
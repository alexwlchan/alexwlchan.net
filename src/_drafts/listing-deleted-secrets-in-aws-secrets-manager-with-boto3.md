---
layout: post
title: Listing deleted secrets in AWS Secrets Manager with boto3 and the AWS CLI
summary: Using botocore extras
tags: python aws aws-secrets-manager
---

If you delete a secret from AWS Secrets Manager, it isn't deleted immediately -- instead, it gets scheduled for deletion.
This gives you a recovery window, so you can retrieve the secret if it was deleted accidentally -- but it also prevents you creating a new secret with the same name.

If you want to delete a secret immediately, you can [call the DeleteSecret API with the ForceDeleteWithoutRecovery parameter][DeleteSecret].
To use this API, you need to know the ID of the secret -- but what if it's already been deleted?
What if you wanted to delete secrets that are still in their recovery window?

You can see deleted secrets in the AWS Console (notice the "Deleted on" column):

<figure  style="width: 515px;">
  <img src="/images/2021/secrets_manager.png">
  <figcaption>
    To see deleted secrets, select the gear icon in the top right-hand corner for settings, then make sure you have "Show disabled secrets" selected.
  </figcaption>
</figure>

But if you call the ListSecrets API, they don't appear.
How can we retrieve deleted secrets programatically?

In this post, I'll explain how I get a list of deleted secrets using boto3.
It takes us on a surprisingly twisty journey through browser dev tools, AWS API definitions, and botocore loaders.

If you just want the answer, [skip to the end](#putting-it-all-together).

[DeleteSecret]: https://aws.amazon.com/premiumsupport/knowledge-center/delete-secrets-manager-secret/



{% separator "secrets_manager.svg" %}



## Motivation

I can see the secrets in the console, so why not delete them there?
It's only a few clicks, and it'd be much faster than writing a script.

I wrote a script because I want to list and delete secrets repeatedly, which makes the reliability and speed of a script is more useful.

For a current project, I'm trying to write a Terraform module that somebody can use to spin up a large collection of services in a new AWS account.
I'm repeatedly creating my resources, then tearing them down so I can try again.
This includes include some secrets in Secrets Manager.

Because the secrets aren't getting deleted immediately, Terraform can't create the secret on the next attempt.
I want a way to clear out Secrets Manager quickly, so I can get back to an empty account.

(I discovered Terraform will delete secrets immediately [if you set `recovery_window_in_days = 0`][tf_var], but I don't want to use it because it's not a setting I'd otherwise use.
I don't love the idea of putting a workaround for my development process in the Terraform module.)

[tf_var]: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/secretsmanager_secret#recovery_window_in_days



{% separator "secrets_manager.svg" %}



## My initial attempt

I started by looking at [the boto3 documentation for `list_secrets()`][list_secrets].
The response schema includes a `DeletedDate` field which is only present on secrets that are scheduled for deletion, so I thought something like this would work:

{% inline_code python _files/2021/list_deleted_secrets.py %}

But when I ran it, I didn't see anything, even though I knew I had deleted secrets -- the `list_secrets()` method was only finding active secrets.
Hmm.

[list_secrets]: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html?highlight=list_secrets#SecretsManager.Client.list_secrets



{% separator "secrets_manager.svg" %}



## A secret parameter

I figured I couldn't be the only person who wanted to do this, and maybe somebody else had made more progress.
Searching around, I found [someone with the same problem on Stack Overflow][stack_overflow].
Although they didn't have an answer, Max Allan had found a useful clue:

> In the AWS console I can see deleted secrets.
> A quick look at the dev tools and I can see my request payload on the Secrets Manager endpoint looks like:
>
> ```
> {
>   "method": "POST",
>   "path": "/",
>   "headers": {
>     "Content-Type": "application/x-amz-json-1.1",
>     "X-Amz-Target": "secretsmanager.ListSecrets",
>     "X-Amz-Date": "Fri, 27 Nov 2020 13:19:06 GMT"
>   },
>   "operation": "ListSecrets",
>   "content": {
>     "MaxResults": 100,
>     "IncludeDeleted": true,
>     "SortOrder": "asc"
>   },
>   "region": "eu-west-2"
> }
> ```
>
> Is there any way to pass `"IncludeDeleted": true` to the CLI?

The other two parameters -- MaxResults and SortOrder -- are both documented parameters for ListSecrets.
What if we pass that undocumented parameter into `list_secrets()`?

```python
client.list_secrets(IncludeDeleted=True)
```

Unfortunately, that returns an error:

```
botocore.exceptions.ParamValidationError: Parameter validation failed:
Unknown parameter in input: "IncludeDeleted", must be one of: MaxResults, NextToken, Filters, SortOrder
```

Even though that parameter would probably do the right thing if we could get it into the HTTP request, boto3 rejects it.
So what if we don't go through boto3?

[stack_overflow]: https://stackoverflow.com/q/65038240/1558022



{% separator "secrets_manager.svg" %}



## Bypassing boto3, briefly

Under the hood, boto3 and the other language-specific AWS SDKs are all making HTTP requests against the same APIs.
If you look at [AWS API docs][apidocs], the first examples are always an HTTP request/response pair.
The SDKs provide a convenient wrapper that build, sign, and send the requests, and in turn interpret the responses -- but you don't have to use them.
What if you sent the HTTP request directly?

To me, the hard part is [signing the requests][signing].
I've never done it before, and it seems like the sort of fiddly process that would take a few attempts to get right.

I tried to find a way to get boto3 to do the request signing for me, on an arbitrary request -- a function that would take some a URL, some headers and a body, and do the signing process -- but if one exists, I couldn't find it.
There's nothing to suggest that's possible in the documentation, I couldn't find examples in Google, and the code itself is pretty complicated.

I couldn't even find [a method called `list_secrets()` in boto3][search] -- so where does that come from?

[apidocs]: https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_ListSecrets.html#API_ListSecrets_Examples
[signing]: https://docs.aws.amazon.com/general/latest/gr/sigv4_signing.html
[search]: https://github.com/boto/boto3/search?q=list_secrets



{% separator "secrets_manager.svg" %}



## How the language-specific AWS SDKs work

At time of writing, AWS has [nine language-specific SDKs][sdks] which have to support over 200 different services.
Each SDK contains a client for each service, and the methods on those clients mirror the underlying HTTP APIs.
It would be impractical to maintain those clients by hand -- so they don't.

Instead, AWS publish "service models" that describe each service.
These models are JSON files that contain a complete description of the endpoints, the models, the documentation text, and so on.
These models are used to autogenerate the service-specific clients in the SDKs, reducing the effort required to keep everything up-to-date.
This approach has also allowed other people to write SDKs in languages that AWS don't support, like [Haskell][haskell_sdk] and [Clojure][clojure_sdk].

These models are a bit like Swagger, although they use an AWS-specific syntax.
Here's part of the Secrets Manager service model:

```
{
  "operations": {
    "ListSecrets": {
      "name": "ListSecrets",
      "http": {"method": "POST", "requestUri": "/"},
      "input": {"shape": "ListSecretsRequest"},
      "output": {"shape": "ListSecretsResponse"},
      "errors":[
        {"shape": "InvalidParameterException"},
        {"shape": "InvalidNextTokenException"},
        {"shape": "InternalServiceError"}
      ],
      "documentation": "Lists all of the secrets that are stored by Secrets Manager in the AWS account. …"
    },
    …
  },
  "shapes": {
    "ListSecretsRequest": {
      "type": "structure",
      "members": {
        "MaxResults": { … },
        "NextToken": { … },
        "Filters": { … },
        "SortOrder": { … }
      }
    },
    …
  },
  "documentation": "<fullname>AWS Secrets Manager API Reference</fullname> …",
  …
}
```

Looking at the `operations` object, we can see that the ListSecrets API requires a POST request to /, and it takes an instance of the ListSecretsRequest model (here called a "shape").
It returns an instance of ListSecretsResponse, or one of three different error types.

In turn, the `shapes` object tells us that the ListSecretsRequest model takes four different parameters (and in turn their types, and a description of how to use them).

You'll find a copy of these service models in every SDK -- for the Python SDK, they're in the ["data" directory of the botocore library][botocore_data].
The methods are generated at runtime, which is why I couldn't find a `list_secrets()` method in the codebase.
For compiled languages like Java or C++, these definitions are used to generate source code.

I couldn't find much publicly available documentation that describes how these service models work.
The most detail I found was a comment from Norm Johanson, an AWS employee, on [the .NET AWS SDK repo][dotnet_comment]:

> AWS services use a few different internal tools and technologies to model their APIs. None of them are swagger. You have to remember many AWS services predate swagger. The json files are created using some tools we have to translate the models service teams write into a common format that all of the AWS SDKs can use.
>
> Long term wise is to have services use our new open source protocol-agnostic interface definition language called [Smithy].

Scant documentation aside, the existence of service models suggests a way forward: what if we modified this file to add the IncludeDeleted parameter?

<!--
1. Go: https://github.com/aws/aws-sdk-go/tree/main/models/apis
2. .NET: https://github.com/aws/aws-sdk-net/tree/abc04d363f65c94a5c8d2fa30b9f5ed799bebdf6/generator/ServiceModels
3. Java: https://github.com/aws/aws-sdk-java-v2/tree/master/services/amplifybackend/src/main/resources/codegen-resources
4. C++: https://github.com/aws/aws-sdk-cpp/tree/bb1fdce01cc7e8ae2fe7162f24c8836e9d3ab0a2/code-generation/api-descriptions
5. Node.js/JS: https://github.com/aws/aws-sdk-js/tree/34d637e6faed4c5fbe332bff2c5cbc1bc5ddf810/apis
6. PHP: https://github.com/aws/aws-sdk-php/tree/ce99fa71b917428ae790063c41e9cc4b85592299/src/data
7. Python: https://github.com/boto/botocore/tree/develop/botocore/data
8. Ruby: https://github.com/aws/aws-sdk-ruby/tree/b091f79fa28fde265693f3e01690526ef2446fde/apis
 -->

[dotnet_comment]: https://github.com/aws/aws-sdk-net/issues/1619
[sdks]: https://aws.amazon.com/getting-started/tools-sdks/
[botocore_data]: https://github.com/boto/botocore/tree/develop/botocore/data
[haskell_sdk]: http://brendanhay.nz/amazonka-comprehensive-haskell-aws-client
[clojure_sdk]: https://github.com/cognitect-labs/aws-api#rationale
[Smithy]: https://github.com/awslabs/smithy



{% separator "secrets_manager.svg" %}



## Modifying the API definition with loaders

I started by modifying the service model in my installed copy of botocore.
I added a new member to the ListSecretsRequest shape:

```diff
       "members": {
+        "IncludeDeleted": {
+          "shape": "BooleanType",
+          "documentation": "<p>(Optional) If set, includes secrets that are disabled.</p>"
+        },
         "MaxResults": {
```

Once I'd done that, I could call `client.list_secrets(IncludeDeleted=True)`, the function would work, and the response included deleted secrets -- but this is pretty brittle.
Next time I update botocore, this change will likely be reverted.

After digging through the botocore code some more, I discovered the idea of "loaders", which have [their own documentation][loaders].
The loaders are classes that look for files with service models, and [make them available to the boto3 clients][client_call]:

```python
def _load_service_model(self, service_name, api_version=None):
    json_model = self._loader.load_service_model(service_name, 'service-2',
                                                 api_version=api_version)
    service_model = ServiceModel(json_model, service_name=service_name)
    return service_model
```

So when you call, say, `boto3.client("s3")`, at some point a loader is called with `load_service_model("s3", "service-2")`.
The `service-2` tells the loader to look for a v2 service model.

The loader documentation explains that there are two default paths where it searches for these data definitions:

-   `~/.aws/models`
-   `<botocore root>/data`

The first path is for users to drop in new models that override the models that ship with botocore.

I reverted my change to botocore proper, and instead copied my modified copy of the Secrets Manager service model to `~/.aws/model`.
Now my changes will survive an update to botocore, but I'm still duplicating the entire service model, even though I only want a small change.
If the service model changes, I'll need to update my patched copy.

Reading the rest of the loader documentation, there's an intriguing notion of "extras" as a way to add additional parameters:

> The sdk-extras and similar files represent extra data that needs to be applied to the model after it is loaded.
> Data in these files might represent information that doesn't quite fit in the original models, but is still needed for the sdk.
> For instance, additional operation parameters might be added here which don't represent the actual service api.

Like everything else around AWS service models, the documentation is pretty sparse, but it was the final clue I needed.
By looking at examples of extras for other service models, I was able to write an extra that describes the undocumented parameter:

```
{
  "version": 1.0,
  "merge": {
    "shapes": {
      "ListSecretsRequest": {
        "members": {
          "IncludeDeleted": {
            "shape": "BooleanType",
            "documentation": "<p>If set, includes secrets that are disabled.</p>"
          }
        }
      }
    }
  }
}
```

Because this extra is only describing the change, rather than reproducing the entire service model, it should be more robust to changes in botocore or the underlying service model.

As a nice side benefit, because the AWS CLI is written in Python and uses boto3, this change also affects the CLI.
It gets a new `--include-deleted/--no-include-deleted` flag, which is even added to the CLI help text.

This turned out to be way, way more complicated than I thought it would be.
I thought I'd write a quick script, a short blog post, and be done.
Instead, I find myself knee-deep in rabbit holes -- but I learnt a lot, and I got something that works!

[loaders]: https://botocore.amazonaws.com/v1/documentation/api/latest/reference/loaders.html
[client_call]: https://github.com/boto/botocore/blob/23ee17f5446c78167ff442302471f9928c3b4b7c/botocore/client.py#L119-L123



{% separator "secrets_manager.svg" %}



## Putting it all together

First, save [the following file](/files/2021/service-2.sdk-extras.json) to `~/.aws/models/secretsmanager/2017-10-17/service-2.sdk-extras.json`:

{% inline_code text _files/2021/service-2.sdk-extras.json %}

Then use the following script:

{% inline_code python _files/2021/list_deleted_secrets.py %}

Or run the following CLI command:

```
aws secretsmanager list-secrets --include-deleted
```

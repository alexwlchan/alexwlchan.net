---
layout: post
date: 2022-06-09 06:40:48 +0000
title: Experimenting with jq as a tool for filtering JSON
summary: I wanted to learn jq's more powerful features, so I tried to filter some JSON from the AWS Secrets Manager CLI.
tags:
  - aws
  - jq
  - aws:aws-secrets-manager
colors:
  index_light: "#c5121f"
  index_dark:  "#ef5258"
---

Recently I wanted to clean up our secrets in AWS Secrets Manager.

We had a lot of secrets with old credentials you couldn't use any more -- for example, passwords for databases we'd deleted.
This made it harder to find current secrets, and more than once I'd tried to use an old secret which didn't work.
Switching to infrastructure-as-code and [Terraform] has made it easier to delete secrets when they become stale, but we had lots of pre-Terraform secrets.

I wanted to find and delete these old secrets.
We have hundreds of secrets in our account, so I didn't want to go through every secret individually.

To help me out, Secrets Manager records the last time a secret was retrieved:

{%
  picture
  filename="secrets_screenshot.png"
  alt="A table with three columns and five rows. The rows are titled 'Secret name', 'Description', and 'Last retrieved (UTC)', and the rows of the 'Last retrieved' column are filled with MM/DD/YYYY dates."
  width="532"
  class="screenshot"
%}

I could use this as a clue for which secrets are current -- they'd have been retrieved recently.
If I filtered for secrets last retrieved before a particular date, I'd get a much shorter list.
I could work through that list and work out what could be safely deleted.

Unfortunately the console doesn't support sorting, so I turned to other means.
The AWS CLI will give you a complete list of secrets, including the last accessed date, in a convenient JSON format:

```console
$ aws secretsmanager list-secrets
{
    "SecretList": [
        {
            "ARN": "arn:aws:secretsmanager:eu-west-1:1234567890:secret:github_api_key-ngKsKU",
            "Name": "github_api_key",
            "LastChangedDate": 1654714184.587,
            "LastAccessedDate": 1654646400.0,
            "Tags": [],
            "SecretVersionsToStages": {
                "f51d4cf9-488b-496a-8d9d-bfad42ec0ef2": [
                    "AWSCURRENT"
                ]
            },
            "CreatedDate": 1654714184.546
        },
        ...
    ]
}
```

There are dozens of ways to filter a blob of JSON; because this was a one-off task, I used it as an opportunity to try using [jq].
It's a command-line tool for slicing and filtering JSON.
I'd used it for simple tasks, but nothing more powerful -- this was a chance to learn.

This is the command I came up with:

```bash
aws secretsmanager list-secrets \
    | jq .SecretList \
    | jq 'map(.LastAccessedDate |= if type == "number" then strftime("%Y-%m-%d") else "<never>" end)' \
    | jq 'map(select(.LastAccessedDate <= "2021-12-31" or .LastAccessedDate == "<never>"))' \
    | jq -r 'map([.LastAccessedDate, .Name] | @tsv) | join("\n")'
```

Let's break it down.

[Terraform]: https://www.terraform.io
[jq]: https://stedolan.github.io/jq/



## Step 1: Extracting the list of secrets

The CLI returns a JSON object with a single key: `SecretList`.
This key contains a list of all the secrets, and I wanted to get at that list so I could filter it.

This was one of the few things I already knew how to do in jq: you can look up [a key in an object with `.key`][key_filter].
For example:

```console
$ echo '{"colour": "green", "sides": 4}' | jq .colour
"green"
```

so I could get the raw list with `jq .SecretList`, like so:

<pre class="language-console"><code><span class="gp">$</span><span class="w"> </span>aws secretsmanager list-secrets <span class="se">\</span>
    | jq .SecretList
<span class="go">[
  {
    "ARN": "arn:aws:secretsmanager:eu-west-1:1234567890:secret:github_api_key-ngKsKU",
    "LastAccessedDate": 1654646400.0,
    ...
  },
  ...
]</span></code></pre>

[key_filter]: https://stedolan.github.io/jq/manual/#ObjectIdentifier-Index:.foo,.foo.bar



## Step 2: Getting a human-readable date in the `LastAccessedDate` field

The `LastAccessedDate` field contains [a Unix timestamp][unix_time], recording seconds since the epoch.
That's not especially useful to me, because I don't speak Unix.
But googling around, I discovered jq [can process dates][date_filter], and in particular it can reformat them.
For example, it can turn that Unix timestamp into a human-readable date:

```console
$ echo '1654646400.0' | jq 'strftime("%Y-%m-%d")'
"2022-06-08"
```

You can update an object with the [update-assignment operator `|=`][update_assignment]:

```console
$ echo '{"Time": 1654646400.0}' | jq '.Time |= strftime("%Y-%m-%d")'
{"Time": "2022-06-08"}
```

And you can map over the elements of a JSON list with [the `map()` filter][map_filter]:

```console
$ echo '[{"Time": 1654646400.0}, {"Time": 1638316800.0}]' | jq 'map(.Time |= strftime("%Y-%m-%d"))'
[
  {"Time": "2022-06-08"},
  {"Time": "2021-12-01"}
]
```

Putting these pieces together, we can replace the `LastAccessedDate` values with human-readable timestamps:

<pre class="language-console"><code><span class="gp">$</span><span class="w"> </span>aws secretsmanager list-secrets <span class="se">\</span>
    | jq .SecretList <span class="se">\</span>
    | jq <span class="s1">'map(.LastAccessedDate |= strftime("%Y-%m-%d"))'</span>
<span class="go">jq: error (at &lt;stdin&gt;:68): strftime/1 requires parsed datetime inputs</span></code></pre>

Oh.

Digging in a bit, I discovered that we had some secrets which had never been accessed, in which case the CLI omits the `LastAccessedDate` key.
If the key is missing, it looks like the update assignment gets passed `null` (in jq, the `.` is the identity function):

```console
$ echo '{"Name": "github_api_key"}' | jq '.LastAccessedDate |= .'
{
  "Name": "github_api_key",
  "LastAccessedDate": null
}
```

We can get round this with jq's [conditional expressions].
In particular, we can inspect the type of the value, and either call `strftime()` or drop in a hard-coded string:

<pre class="language-console"><code><span class="gp">$</span><span class="w"> </span>aws secretsmanager list-secrets <span class="se">\</span>
    | jq .SecretList <span class="se">\</span>
    | jq <span class="s1">'map(.LastAccessedDate |= if type == "number" then strftime("%Y-%m-%d") else "&lt;never&gt;" end)'</span>
<span class="go">[
  {
    "ARN": "arn:aws:secretsmanager:eu-west-1:241906670800:secret:github_api_key-ngKsKU",
    "LastAccessedDate": "2022-06-08",
    ...
  },
  {
    "ARN": "arn:aws:secretsmanager:eu-west-1:241906670800:secret:user_db_credentials-gAdCG1",
    "LastAccessedDate": "&lt;never&gt;"
  },
  ...
]</span></code></pre>

[unix_time]: https://en.wikipedia.org/wiki/Unix_time
[date_filter]: https://stedolan.github.io/jq/manual/#Dates
[update_assignment]: https://stedolan.github.io/jq/manual/#Update-assignment:|=
[map_filter]: https://stedolan.github.io/jq/manual/#map(x),map_values(x)
[conditional expressions]: https://stedolan.github.io/jq/manual/#ConditionalsandComparisons



## Step 3: Filter for values before a particular date

Now I've got the dates into a format I can read, I can pick out the secrets with values I care about.
In jq, there are lots of things called "filters", so what might be called `filter()` in another language is called [`select()`][select] in jq.

```console
$ echo '[1, 2, 3, 4, 5]' | jq 'map(select(. >= 3))'
[3, 4, 5]
```

Because I've already converted the dates into human-readable form, this let me write a human-readable filter.
For example, if I want to find secrets that we haven't looked at this year:

<pre class="language-console"><code><span class="gp">$</span><span class="w"> </span>aws secretsmanager list-secrets <span class="se">\</span>
    | jq .SecretList <span class="se">\</span>
    | jq <span class="s1">'map(.LastAccessedDate |= if type == "number" then strftime("%Y-%m-%d") else "&lt;never&gt;" end)'</span> <span class="se">\</span>
    | jq <span class="s1">'map(select(.LastAccessedDate <= "2021-12-31"))'</span></code></pre>

This isn't quite enough -- remember some of the secrets have never been retrieved, and I want to include them too.
We can include them using jq's [boolean operators]:

<pre class="language-console"><code><span class="gp">$</span><span class="w"> </span>aws secretsmanager list-secrets <span class="se">\</span>
    | jq .SecretList <span class="se">\</span>
    | jq <span class="s1">'map(.LastAccessedDate |= if type == "number" then strftime("%Y-%m-%d") else "&lt;never&gt;" end)'</span> <span class="se">\</span>
    | jq <span class="s1">'map(select(.LastAccessedDate <= "2021-12-31" or .LastAccessedDate == "&lt;never&gt;"))'</span>
<span class="go">[
  {
    "ARN": "arn:aws:secretsmanager:eu-west-1:241906670800:secret:twitter_oauth_token-aIWQcj",
    "LastAccessedDate": "2021-04-01",
    ...
  },
  {
    "ARN": "arn:aws:secretsmanager:eu-west-1:241906670800:secret:user_db_credentials-gAdCG1",
    "LastAccessedDate": "&lt;never&gt;"
  },
  ...
]</span></code></pre>

The alternative would have been writing this filter using Unix timestamps -- possible, but more cumbersome.

[select]: https://stedolan.github.io/jq/manual/#select(boolean_expression)
[boolean operators]: https://stedolan.github.io/jq/manual/#and/or/not



## Step 4: Make the output more readable

This JSON output is great for computers, but not so good for humans.
There's a lot of information there I don't care about; I only want the secret and last retrieved date.
Fortunately, jq also has some [formatting filters], one of which lets you print as TSV (tab-separated values):

<pre class="language-console"><code><span class="gp">$</span><span class="w"> </span>aws secretsmanager list-secrets <span class="se">\</span>
    | jq .SecretList <span class="se">\</span>
    | jq <span class="s1">'map(.LastAccessedDate |= if type == "number" then strftime("%Y-%m-%d") else "&lt;never&gt;" end)'</span> <span class="se">\</span>
    | jq <span class="s1">'map(select(.LastAccessedDate <= "2021-12-31" or .LastAccessedDate == "&lt;never&gt;"))'</span> <span class="se">\</span>
    | jq -r <span class="s1">'map([.LastAccessedDate, .Name] | @tsv) | join("\n")'</span>
<span class="go">2021-04-01	twitter_oauth_token
&lt;never&gt;		email_cert
2021-04-02	git_private_key</span></code></pre>

The `-r` flag to jq tells it to print the raw value; not a JSON-formatted string.
This give me a simple list I can work through and start to pick off secrets.

I didn't want to delete every secret that hadn't been accessed recently, because some secrets are rarely accessed for good reason -- for example, if they're part of a disaster recovery process.
But this list did let me delete several dozen secrets we weren't using, and I had to check a much shorter list than every secret in the account.

[formatting filters]: https://stedolan.github.io/jq/manual/#Formatstringsandescaping



## Would I do this again?

This is the final command:

```bash
aws secretsmanager list-secrets \
    | jq .SecretList \
    | jq 'map(.LastAccessedDate |= if type == "number" then strftime("%Y-%m-%d") else "<never>" end)' \
    | jq 'map(select(.LastAccessedDate <= "2021-12-31" or .LastAccessedDate == "<never>"))' \
    | jq -r 'map([.LastAccessedDate, .Name] | @tsv) | join("\n")'
```

There are lots of ways to filter a list of JSON objects; I picked jq because this was a one-off task, and I wanted to try its more powerful features.
Normally I'm quite conservative about using new tools, but I knew I'd be throwing this code away so that was less of a concern.

I got this working, but I'm not super happy with the code.
It took a lot of trial-and-error; in particular, the order of some of the `map()` filters was quite fiddly and tricky to get right.
If I put this in a production codebase, I'd worry about whether I could understand or modify it in future.

Nonetheless, this was a good experiment.
Even if I'm unlikely to use jq for this sort of task in future, I'm glad to have a flavour of its power.

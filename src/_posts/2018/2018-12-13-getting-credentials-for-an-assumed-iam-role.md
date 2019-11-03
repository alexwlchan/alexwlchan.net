---
category: Amazon Web Services
date: 2018-12-13 08:57:16 +0000
layout: post
summary: A script that creates temporary credentials for an assumed IAM role, and
  stores them in ~/.aws/credentials.
tags: python aws
title: Getting credentials for an assumed IAM Role
---

In AWS, everybody has a user account, and you can give each user very granular permissions.
For example, you might allow some users complete access to your S3 buckets, databases and EC2 instances, while other users just have read-only permissions.
Maybe you have another user who can only see billing information.
These permissions are all managed by [AWS IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html).

Sometimes you want to give somebody temporary permissions that aren't part of their usual IAM profile -- maybe for an unusual operation, or to let them access resources in a different AWS account.
The mechanism for managing this is an [*IAM role*](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html).
An IAM role is an identity with certain permissions and privileges that can be *assumed* by a user.
When you assume a role, you get the associated permissions.

For example, at work, the DNS entries for wellcomecollection.org are managed in a different AWS account to the one I usually work in -- but I can assume a role that lets me edit the DNS config.

If you're using the AWS console, you can assume a role in the GUI -- there's a dropdown menu with a button for it:

{%
  image :filename => "iam_role_gui.png",
  :alt => "A screenshot from the IAM console, showing a dropdown menu with a green arrow pointing at “Switch Role”."
%}

If you're using the SDK or the CLI, it can be a little trickier -- so I wrote a script to help me.

## The "proper" approach

According to [the AWS docs](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-role.html), you can define an IAM role as a profile in `~/.aws/config`.

This example shows a role profile called `dns_editor_profile`.

```
[profile dns_editor_profile]
role_arn = arn:aws:iam::123456789012:role/dns_editor
source_profile = user1
```

When I use this profile, the CLI automatically creates temporary credentials for the `dns_editor` role, and uses those during my session.
When the credentials expire, it renews them.
Seamless!

This config is also supported in [the Python SDK](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#assume-role-provider), and I'd guess it works with SDKs in other languages as well -- but when I tried it with Terraform, it was struggling to find credentials.
I don't know if this is a gap in the Go SDK, or in Terraform's use of it -- either way, I needed an alternative.
So rather than configuring credentials implicitly, I wrote a script to create them explicitly.

## Creating temporary AWS credentials for a role

There are a couple of ways to pass AWS credentials to the SDK: as environment variables, with SDK-specific arguments, or with the shared credentials profile file in `~/.aws/credentials`.
I store the credentials in the shared profile file because all the SDKs can use it, so my script has two steps:

1.  Create a set of temporary credentials
2.  Store them in `~/.aws/credentials`

By keeping those as separate steps, it's easier to change the storage later if, for example, I want to use environment variables.

### Create a set of temporary credentials

AWS credentials are managed by AWS Security Token Service (STS).
You get a set of temporary credentials by calling [the `assume_role()` API](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html?highlight=sts#STS.Client.assume_role).

Let's suppose we already have the account ID (the 13-digit number in the role ARN above) and the role name.
We can get some temporary credentials like so:

```python
import boto3


def get_credentials(*, account_id, role_name):
    sts_client = boto3.client("sts")

    role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"
    role_session_name = "..."

    resp = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName=role_session_name
    )

    return resp["Credentials"]
```

Here `RoleArn` is the ARN (AWS identifier) of the IAM role we want to assume, and `RoleSessionName` is an identifier for the session.
If multiple people assume a role at the same time, we want to distinguish the different sessions.

You can put any alphanumeric string there (no spaces, but a few punctuation characters).
I use my IAM username and the details of the role I'm assuming, so it's easy to understand in audit logs:

```python
    iam_client = boto3.client("iam")
    username = iam_client.get_user()["User"]["UserName"]
    role_session_name = f"{username}@{role_name}.{account_id}"
```

We could also set the `DurationSeconds` parameter, which configures how long the credentials are valid for.
It defaults to an hour, which is fine for my purposes -- but you might want to change it if you have longer sessions, and don't want to keep re-issuing credentials.

Note that I'm using two Python 3 features here: [f-strings for interpolation](https://www.python.org/dev/peps/pep-0498/), which I find much cleaner, and the `*` in the argument list creates [keyword-only arguments](https://www.python.org/dev/peps/pep-3102/), to enforce clarity when this function is called.

### Store the credentials in ~/.aws/credentials

The format of the credentials file is something like this:

```
[profile_name]
aws_access_key_id=ABCDEFGHIJKLM1234567890
aws_secret_access_key=ABCDEFGHIJKLM1234567890

[another_profile]
aws_access_key_id=ABCDEFGHIJKLM1234567890
aws_secret_access_key=ABCDEFGHIJKLM1234567890
aws_session_token=ABCDEFGHIJKLM1234567890
```

Each section is a new AWS profile, and contains an access key, a secret key, and optionally a session token.
That session token is tied to the `RoleSessionName` we gave when assuming the role.

We could try to edit this file by hand -- or easier, we could use the [configparser module](https://docs.python.org/3/library/configparser.html) in the Python standard library, which is meant for working with this type of file.

First we have to load the existing credentials, then look for a profile with this name.
If it's present, we replace it; if not, we create it.
Then we store the new credentials, and rewrite the file.
Like so:

```python
import configparser
import os


def update_credentials_file(*, profile_name, credentials):
    aws_dir = os.path.join(os.environ["HOME"], ".aws")

    credentials_path = os.path.join(aws_dir, "credentials")
    config = configparser.ConfigParser()
    config.read(credentials_path)

    if profile_name not in config.sections():
        config.add_section(profile_name)

    assert profile_name in config.sections()

    config[profile_name]["aws_access_key_id"] = credentials["AccessKeyId"]
    config[profile_name]["aws_secret_access_key"] = credentials["SecretAccessKey"]
    config[profile_name]["aws_session_token"] = credentials["SessionToken"]

    config.write(open(credentials_path, "w"), space_around_delimiters=False)
```

Most of this is fairly standard use of the configparser library.
The one item of note: I remove the spaces around delimiters, because when I tried leaving them in, boto3 got upset -- I think it read the extra space as part of the credentials.

### Read command-line parameters

Finally, we need to get some command-line parameters to tell us what the account ID and role name are, and optionally a profile name to store in `~/.aws/credentials`.
Recently I've been trying [click](https://palletsprojects.com/p/click/) for command-line parameters, and I quite like it.
Here's the code:

```python
import click


@click.command()
@click.option("--account_id", required=True)
@click.option("--role_name", required=True)
@click.option("--profile_name")
def save_assumed_role_credentials(account_id, role_name, profile_name):
    if profile_name is None:
        profile_name = account_id

    credentials = get_credentials(
        account_id=account_id,
        role_name=role_name
    )

    update_credentials_file(profile_name=profile_name, credentials=credentials)


if __name__ == "__main__":
    save_assumed_role_credentials()
```

This defines a command-line interface with `@click.command()`, then sets up two required command-line parameters -- account ID and role name.
The profile name is a third, optional parameter, and defaults to the account ID if you don't supply one.
These parameters are passed into the `save_assumed_role_credentials()` method, which calls the two helpers methods.

Now I can call the script like so:

```console
$ python issue_temporary_credentials.py --account_id=123456789012 --role_name=dns_editor --profile_name=dns_editor_profile
```

and it creates a set of credentials and writes them to `~/.aws/credentials`.

To use this profile, I set the `AWS_PROFILE` variable:

```console
$ AWS_PROFILE=dns_editor_profile aws s3 ls
```

and this command now runs with the credentials for that profile.

## tl;dr

If you just want the code, here's the final copy of the script:

```python
# issue_temporary_credentials.py

import configparser
import os
import sys

import boto3
import click


def get_credentials(*, account_id, role_name):
    iam_client = boto3.client("iam")
    sts_client = boto3.client("sts")

    username = iam_client.get_user()["User"]["UserName"]

    role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"
    role_session_name = f"{username}@{role_name}.{account_id}"

    resp = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName=role_session_name
    )

    return resp["Credentials"]


def update_credentials_file(*, profile_name, credentials):
    aws_dir = os.path.join(os.environ["HOME"], ".aws")

    credentials_path = os.path.join(aws_dir, "credentials")
    config = configparser.ConfigParser()
    config.read(credentials_path)

    if profile_name not in config.sections():
        config.add_section(profile_name)

    assert profile_name in config.sections()

    config[profile_name]["aws_access_key_id"] = credentials["AccessKeyId"]
    config[profile_name]["aws_secret_access_key"] = credentials["SecretAccessKey"]
    config[profile_name]["aws_session_token"] = credentials["SessionToken"]

    config.write(open(credentials_path, "w"), space_around_delimiters=False)


@click.command()
@click.option("--account_id", required=True)
@click.option("--role_name", required=True)
@click.option("--profile_name")
def save_assumed_role_credentials(account_id, role_name, profile_name):
    if profile_name is None:
        profile_name = account_id

    credentials = get_credentials(
        account_id=account_id,
        role_name=role_name
    )

    update_credentials_file(profile_name=profile_name, credentials=credentials)


if __name__ == "__main__":
    save_assumed_role_credentials()
```
#!/usr/bin/env python3
"""
This is a tool for finding information about an IAM access key:

    $ python3 describe_iam_access_key.py AKIAVOSFODNN7EXAMPLE
    access key:       AKIAIOSFODNN7EXAMPLE
    account:          acme_corp (1234567890)
    username:         example_user
    key created:      19 May 2020

    IAM permissions:  archivists_s3_upload.iam_permissions.txt

    console:          https://us-east-1.console.aws.amazon.com/iamv2/home#/users/details/example_user?section=permissions
    terraform:        https://github.com/wellcomecollection/archivematica-infrastructure/tree/master/terraform/users

== Motivation ==

We mostly use IAM access keys with S3 clients like FileZilla Pro.

When somebody has an issue, they may know their access key ID but
nothing else.  It's often useful to know the IAM permissions associated
with the key (and where it's defined, in case we need to change them).

This script goes through every IAM user in every account until it finds
a matching access key, then prints some useful information about it.

== How it works ==

1.  Use the sts:GetAccessKeyInfo API to find the AWS account ID.
2.  Use the iam:GetAccessKeyLastUsed API to find the IAM user name.
3.  Use a couple of other IAM APIs to get info about the user before
    pretty-printing it.

See https://alexwlchan.net/2023/iam-keys/

"""

import json
import sys

import boto3
from botocore.exceptions import ClientError
import termcolor

from config import WELLCOME_ACCOUNT_NAMES


def get_aws_session(*, role_arn):
    sts_client = boto3.client("sts")
    assumed_role_object = sts_client.assume_role(
        RoleArn=role_arn, RoleSessionName="AssumeRoleSession1"
    )
    credentials = assumed_role_object["Credentials"]

    return boto3.Session(
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"],
    )


def find_account_id(*, access_key_id):
    """
    Given an IAM access key ID, return the account identifier.

    See https://docs.aws.amazon.com/STS/latest/APIReference/API_GetAccessKeyInfo.html
    """
    sess = get_aws_session(role_arn="arn:aws:iam::760097843905:role/platform-read_only")
    sts_client = sess.client("sts")

    return sts_client.get_access_key_info(AccessKeyId=access_key_id)["Account"]


def get_iam_user_name(sess, *, access_key_id):
    """
    Given an IAM access key ID and an authenticated session, return the
    user_name of the associated IAM user.
    """
    iam_client = sess.client("iam")

    return iam_client.get_access_key_last_used(AccessKeyId=access_key_id)["UserName"]


def pprint_info(*, key, value, color="blue"):
    print(f"{key}:".ljust(17), end=" ")
    print(termcolor.colored(value, color))


def pprint_user_info(sess, *, account_id, account_name, user_name, access_key_id):
    """
    Print a bunch of information about this user and their access key.
    """
    iam_client = sess.client("iam")

    user_tags = {
        t["Key"]: t["Value"]
        for t in iam_client.list_user_tags(UserName=user_name)["Tags"]
    }
    user_policy_names = iam_client.list_user_policies(UserName=user_name)
    user_policies = {
        policy_name: iam_client.get_user_policy(
            UserName=user_name, PolicyName=policy_name
        )
        for policy_name in user_policy_names["PolicyNames"]
    }
    user_access_keys = iam_client.list_access_keys(UserName=user_name)
    this_access_key_info = next(
        m
        for m in user_access_keys["AccessKeyMetadata"]
        if m["AccessKeyId"] == access_key_id
    )

    pprint_info(key="access key", value=access_key_id)
    pprint_info(key="account", value=f"{account_name} ({account_id})")
    pprint_info(key="username", value=user_name)
    pprint_info(
        key="key created",
        value=this_access_key_info["CreateDate"].strftime("%-d %B %Y"),
    )
    pprint_info(
        key="status",
        value=this_access_key_info["Status"],
        color="red" if this_access_key_info["Status"] == "Inactive" else "blue",
    )

    print("")

    policy_document_file = f"{user_name}.iam_permissions.txt"
    with open(policy_document_file, "w") as outfile:
        for policy_name, policy_description in user_policies.items():
            outfile.write(policy_name + "\n")
            outfile.write(
                json.dumps(
                    policy_description["PolicyDocument"], indent=2, sort_keys=True
                )
                + "\n\n"
            )

    pprint_info(key="IAM permissions", value=policy_document_file)

    print("")

    pprint_info(
        key="console",
        value=f"https://us-east-1.console.aws.amazon.com/iamv2/home#/users/details/{user_name}",
    )
    pprint_info(
        key="terraform", value=user_tags.get("TerraformConfigurationURL", "<unknown>")
    )


if __name__ == "__main__":
    try:
        access_key_id = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {__file__} <ACCESS_KEY_ID>")

    account_id = find_account_id(access_key_id=access_key_id)

    # Go from the AWS account ID to:
    #
    #   -   a friendly name for this AWS account
    #   -   an authenticated boto3 Session in this account which has the
    #       iam:GetAccessKeyLastUsed permission
    #
    # If you want to use this script with non-Wellcome AWS accounts,
    # you'll need to customise this part.
    try:
        account_name = WELLCOME_ACCOUNT_NAMES[account_id]
    except KeyError:
        pprint_info(key="access key", value=access_key_id)
        pprint_info(key="account", value=f"{account_id} (unknown)")
        sys.exit(0)
    else:
        sess = get_aws_session(
            role_arn=f"arn:aws:iam::{account_id}:role/{account_name}-read_only"
        )

    user_name = get_iam_user_name(sess, access_key_id=access_key_id)

    pprint_user_info(
        sess,
        account_id=account_id,
        account_name=account_name,
        user_name=user_name,
        access_key_id=access_key_id,
    )

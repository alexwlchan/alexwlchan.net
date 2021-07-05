import boto3


def list_secrets(session):
    client = session.client("secretsmanager")

    for page in client.get_paginator("list_secrets").paginate():
        yield from page["SecretList"]


if __name__ == "__main__":
    session = boto3.Session()

    for secret in list_secrets(session):
        if "DeletedDate" in secret:
            print(secret)

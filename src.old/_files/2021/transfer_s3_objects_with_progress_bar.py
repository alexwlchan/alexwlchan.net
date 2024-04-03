import os

import boto3
import tqdm


def download_object_from_s3(session, *, bucket, key, version_id=None, filename):
    """
    Download an object from S3 with a progress bar.

    From https://alexwlchan.net/2021/04/s3-progress-bars/
    """
    s3 = session.client("s3")

    # First get the size, so we know what tqdm is counting up to.
    # Theoretically the size could change between this HeadObject and starting
    # to download the file, but this would only affect the progress bar.
    kwargs = {"Bucket": bucket, "Key": key}

    if version_id is not None:
        kwargs["VersionId"] = version_id

    object_size = s3.head_object(**kwargs)["ContentLength"]

    # Now actually download the object, with a progress bar to match.
    # How this works:
    #
    #   -   We take manual control of tqdm() using a ``with`` statement,
    #       see https://pypi.org/project/tqdm/#manual
    #
    #   -   We set ``unit_scale=True`` so tqdm uses SI unit prefixes, and
    #       ``unit="B"`` means it adds a "B" as a suffix.  This means we get
    #       progress info like "14.5kB/s".
    #
    #       (Note: the "B" is just a string; tqdm doesn't know these are
    #       bytes and doesn't care.)
    #
    #   -   The Callback method on a boto3 S3 function is called
    #       periodically during the download with the number of bytes
    #       transferred.  We can use it to update the progress bar.
    #
    if version_id is not None:
        ExtraArgs = {"VersionId": version_id}
    else:
        ExtraArgs = None

    with tqdm.tqdm(total=object_size, unit="B", unit_scale=True, desc=filename) as pbar:
        s3.download_file(
            Bucket=bucket,
            Key=key,
            ExtraArgs=ExtraArgs,
            Filename=filename,
            Callback=lambda bytes_transferred: pbar.update(bytes_transferred),
        )


def upload_file_to_s3(session, *, bucket, key, filename):
    """
    Upload a file to S3 with a progress bar.

    From https://alexwlchan.net/2021/04/s3-progress-bars/
    """
    file_size = os.stat(filename).st_size

    s3 = session.client("s3")

    with tqdm.tqdm(total=file_size, unit="B", unit_scale=True, desc=filename) as pbar:
        s3.upload_file(
            Filename=filename,
            Bucket=bucket,
            Key=key,
            Callback=lambda bytes_transferred: pbar.update(bytes_transferred),
        )


if __name__ == "__main__":
    # Customise the session if you want to use, e.g., a particular role ARN
    # See https://ben11kehoe.medium.com/boto3-sessions-and-why-you-should-use-them-9b094eb5ca8e
    session = boto3.Session()

    download_object_from_s3(
        session,
        bucket="example-bucket",
        key="cat.jpg",
        filename="cat_v1.jpg",
        version_id="lzhtwp8Tgq7lRRy_7.Qz9eIB5b68le_h",
    )

    download_object_from_s3(
        session,
        bucket="example-bucket",
        key="cat.jpg",
        filename="cat_latest.jpg"
    )

    with open("greeting.txt", "wb") as outfile:
        outfile.write(b"Hello world! Guten tag! Bonjour!")

    upload_file_to_s3(
        session,
        bucket="example-bucket",
        key="greeting.txt",
        filename="greeting.txt",
    )

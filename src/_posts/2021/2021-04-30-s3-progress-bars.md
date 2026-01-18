---
layout: post
date: 2021-04-30 18:28:27 +00:00
title: Downloading objects from/uploading files to S3 with progress bars in Python
summary: Making it easier to see how long a file transfer will take, in the terminal.
tags:
  - aws:amazon s3
  - aws
  - python
  - terminal tricks
---

I write a lot of scripts to move files in and out of S3, and when I'm dealing with larger files, I find it useful to get an idea of how long the transfer will take.
Will it be done in a tick, or should I find something else to do while I wait?

The AWS CLI gives you half of this -- it shows the size of the object it's transferring, and the current transfer rate -- but you still need to work out the time for yourself.
Can we do better?

Both the [`download_file()`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.download_file) and [`upload_file()`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.download_file) methods in the boto3 SDK support progress callbacks.
If you pass a function in the Callback parameter, it gets periodically called with the number of bytes that have been transferred so far.

If we also look up the size of the object, and pass all this information to the amazing [tqdm library](https://pypi.org/project/tqdm/), we get progress bars for our S3 transfers.
Here's what they look like:

<pre><code id="progressBarDemo">photo.jpg:&nbsp;&nbsp;&nbsp;0%|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;0.00/13.0M&nbsp;[00:00&lt;?,&nbsp;?B/s]</code>
<code style="padding-top: 5px; display: block;"><a onclick="runDemo()" style="cursor: pointer; text-decoration: underline">run demo</a><noscript>(Sorry, this demo requires JavaScript!)</noscript></code></pre>

<script>
var lines = ['photo.jpg:&nbsp;&nbsp;&nbsp;0%|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;0.00/13.0M&nbsp;[00:00&lt;?,&nbsp;?B/s]',
 'photo.jpg:&nbsp;&nbsp;&nbsp;2%|▏&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;262k/13.0M&nbsp;[00:00&lt;00:41,&nbsp;306kB/s]',
 'photo.jpg:&nbsp;&nbsp;&nbsp;4%|▍&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;524k/13.0M&nbsp;[00:01&lt;00:36,&nbsp;345kB/s]',
 'photo.jpg:&nbsp;&nbsp;&nbsp;6%|▌&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;786k/13.0M&nbsp;[00:01&lt;00:26,&nbsp;455kB/s]',
 'photo.jpg:&nbsp;&nbsp;&nbsp;8%|▊&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;1.05M/13.0M&nbsp;[00:01&lt;00:21,&nbsp;565kB/s]',
 'photo.jpg:&nbsp;&nbsp;12%|█▏&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;1.57M/13.0M&nbsp;[00:01&lt;00:15,&nbsp;745kB/s]',
 'photo.jpg:&nbsp;&nbsp;14%|█▍&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;1.84M/13.0M&nbsp;[00:02&lt;00:12,&nbsp;913kB/s]',
 'photo.jpg:&nbsp;&nbsp;18%|█▊&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;2.36M/13.0M&nbsp;[00:02&lt;00:09,&nbsp;1.14MB/s]',
 'photo.jpg:&nbsp;&nbsp;22%|██▏&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;2.88M/13.0M&nbsp;[00:02&lt;00:06,&nbsp;1.45MB/s]',
 'photo.jpg:&nbsp;&nbsp;26%|██▌&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;3.41M/13.0M&nbsp;[00:02&lt;00:05,&nbsp;1.79MB/s]',
 'photo.jpg:&nbsp;&nbsp;30%|███&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;3.93M/13.0M&nbsp;[00:02&lt;00:04,&nbsp;2.18MB/s]',
 'photo.jpg:&nbsp;&nbsp;34%|███▍&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;4.46M/13.0M&nbsp;[00:02&lt;00:03,&nbsp;2.61MB/s]',
 'photo.jpg:&nbsp;&nbsp;38%|███▊&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;4.98M/13.0M&nbsp;[00:02&lt;00:03,&nbsp;2.51MB/s]',
 'photo.jpg:&nbsp;&nbsp;44%|████▍&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;5.77M/13.0M&nbsp;[00:03&lt;00:02,&nbsp;2.90MB/s]',
 'photo.jpg:&nbsp;&nbsp;48%|████▊&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;6.29M/13.0M&nbsp;[00:03&lt;00:02,&nbsp;2.71MB/s]',
 'photo.jpg:&nbsp;&nbsp;52%|█████▏&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;6.82M/13.0M&nbsp;[00:03&lt;00:03,&nbsp;1.99MB/s]',
 'photo.jpg:&nbsp;&nbsp;56%|█████▋&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;7.34M/13.0M&nbsp;[00:04&lt;00:02,&nbsp;2.05MB/s]',
 'photo.jpg:&nbsp;&nbsp;61%|██████&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;7.86M/13.0M&nbsp;[00:04&lt;00:02,&nbsp;2.36MB/s]',
 'photo.jpg:&nbsp;&nbsp;65%|██████▍&nbsp;&nbsp;&nbsp;|&nbsp;8.39M/13.0M&nbsp;[00:04&lt;00:02,&nbsp;2.19MB/s]',
 'photo.jpg:&nbsp;&nbsp;69%|██████▊&nbsp;&nbsp;&nbsp;|&nbsp;8.91M/13.0M&nbsp;[00:04&lt;00:01,&nbsp;2.24MB/s]',
 'photo.jpg:&nbsp;&nbsp;73%|███████▎&nbsp;&nbsp;|&nbsp;9.44M/13.0M&nbsp;[00:04&lt;00:01,&nbsp;2.30MB/s]',
 'photo.jpg:&nbsp;&nbsp;75%|███████▍&nbsp;&nbsp;|&nbsp;9.70M/13.0M&nbsp;[00:04&lt;00:01,&nbsp;2.34MB/s]',
 'photo.jpg:&nbsp;&nbsp;77%|███████▋&nbsp;&nbsp;|&nbsp;9.96M/13.0M&nbsp;[00:05&lt;00:01,&nbsp;2.41MB/s]',
 'photo.jpg:&nbsp;&nbsp;80%|███████▉&nbsp;&nbsp;|&nbsp;10.4M/13.0M&nbsp;[00:05&lt;00:01,&nbsp;2.40MB/s]',
 'photo.jpg:&nbsp;&nbsp;84%|████████▍&nbsp;|&nbsp;10.9M/13.0M&nbsp;[00:05&lt;00:00,&nbsp;2.65MB/s]',
 'photo.jpg:&nbsp;&nbsp;88%|████████▊&nbsp;|&nbsp;11.4M/13.0M&nbsp;[00:05&lt;00:00,&nbsp;2.29MB/s]',
 'photo.jpg:&nbsp;&nbsp;90%|████████▉&nbsp;|&nbsp;11.7M/13.0M&nbsp;[00:05&lt;00:00,&nbsp;2.29MB/s]',
 'photo.jpg:&nbsp;&nbsp;92%|█████████▏|&nbsp;11.9M/13.0M&nbsp;[00:05&lt;00:00,&nbsp;2.23MB/s]',
 'photo.jpg:&nbsp;&nbsp;94%|█████████▍|&nbsp;12.2M/13.0M&nbsp;[00:06&lt;00:00,&nbsp;2.20MB/s]',
 'photo.jpg:&nbsp;&nbsp;96%|█████████▌|&nbsp;12.5M/13.0M&nbsp;[00:06&lt;00:00,&nbsp;2.26MB/s]',
 'photo.jpg:&nbsp;&nbsp;98%|█████████▊|&nbsp;12.7M/13.0M&nbsp;[00:06&lt;00:00,&nbsp;2.16MB/s]',
 'photo.jpg:&nbsp;100%|██████████|&nbsp;13.0M/13.0M&nbsp;[00:06&lt;00:00,&nbsp;2.23MB/s]',
 'photo.jpg:&nbsp;100%|██████████|&nbsp;13.0M/13.0M&nbsp;[00:06&lt;00:00,&nbsp;2.02MB/s]'];

function setLine(code, lineNo) {
  console.log("Calling setLine(" + code + ", " + lineNo + ")");
  code.innerHTML = lines[lineNo];
  if (lineNo + 1 < lines.length) {
    setTimeout(function() { setLine(code, lineNo + 1) }, 150);
  }
};

function runDemo() {
  console.log("Calling runDemo() 1");
  var code = document.getElementById("progressBarDemo");
  console.log("Calling runDemo() 2");
  setLine(code, 0);
};

</script>

I've got two functions: one that can download objects, another that can upload them.
I've included the code for both below, and some examples of how to use them.
I'm not going to walk through the code – hopefully the comments are sufficient to understand how it works.

If this seems like something you'd find useful, copy it into your own scripts.
Enjoy!

```python
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
```

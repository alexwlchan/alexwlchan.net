---
layout: post
date: 2021-04-30 18:28:27 +0000
title: Downloading objects from/uploading files to S3 with progress bars in Python
summary: Making it easier to see how long a file transfer will take, in the terminal.
tags: amazon-s3 aws python terminal-tricks
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
(If not, [get in touch](/#contact).)

If this seems like something you'd find useful, copy it into your own scripts.
Enjoy!

{% inline_code python _files/2021/transfer_s3_objects_with_progress_bar.py %}

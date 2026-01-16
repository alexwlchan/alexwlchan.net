---
layout: til
title: How to simulate shell pipes with the subprocess module
date: 2024-01-13 10:57:17 +00:00
tags:
  - python
---
I had a shell command featuring a pipe that I wanted to replicate with subprocess:

```bash
youtube-dl --get-id "$PLAYLIST_URL" \
  | xargs -I '{}' -P 5 youtube-dl 'https://youtube.com/watch?v={}'
```

I could try to create this command as a string, pass it to `subprocess.call(…, shell=True)`, and I hope I've used `shlex.quote()` correctly – but that's dangerous and error-prone.

I found a better approach in [a Stack Overflow answer][so] by Taymon: use `subprocess.PIPE` to pass stdout/stdin between processes.

<pre><code>
get_ids_proc = subprocess.Popen(
    ["youtube-dl", "--get-id", youtube_url],
    <strong>stdout=subprocess.PIPE</strong>
)

subprocess.check_call(
    ["xargs", "-I", "{}", "-P", "5", "youtube-dl", "https://youtube.com/watch?v={}"],
    <strong>stdin=get_ids_proc.stdout,</strong>
)

get_ids_proc.wait()
</code></pre>

[so]: https://stackoverflow.com/q/13332268/1558022

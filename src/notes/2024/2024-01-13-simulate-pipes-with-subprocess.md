---
layout: note
title: How to simulate shell pipes with the subprocess module
date: 2024-01-13 10:57:17 +00:00
topic: Python
---
I had a shell command featuring a pipe that I wanted to replicate with subprocess:

```bash
youtube-dl --get-id "$PLAYLIST_URL" \
  | xargs -I '{}' -P 5 youtube-dl 'https://youtube.com/watch?v={}'
```

I could try to create this command as a string, pass it to `subprocess.call(…, shell=True)`, and I hope I've used `shlex.quote()` correctly – but that's dangerous and error-prone.

I found a better approach in [a Stack Overflow answer][so] by Taymon: use `subprocess.PIPE` to pass stdout/stdin between processes.

<pre class="lng-python"><code><span class="n">get_ids_proc</span> = subprocess.Popen<span class="p">(</span>
    <span class="p">[</span><span class="s">"youtube-dl"</span><span class="p">,</span> <span class="s">"--get-id"</span><span class="p">,</span> youtube_url<span class="p">]</span><span class="p">,</span>
    <mark>stdout=subprocess.PIPE</mark>
<span class="p">)</span>

subprocess.check_call<span class="p">(</span>
    <span class="p">[</span><span class="s">"xargs"</span><span class="p">,</span> <span class="s">"-I"</span><span class="p">,</span> <span class="s">"{}"</span><span class="p">,</span> <span class="s">"-P"</span><span class="p">,</span> <span class="s">"5"</span><span class="p">,</span> <span class="s">"youtube-dl"</span><span class="p">,</span> <span class="s">"https://youtube.com/watch?v={}"</span><span class="p">]</span><span class="p">,</span>
    <mark>stdin=get_ids_proc.stdout<span class="p">,</span></mark>
<span class="p">)</span>

get_ids_proc.wait<span class="p">(</span><span class="p">)</span>
</code></pre>

[so]: https://stackoverflow.com/q/13332268/1558022

---
layout: article
date: 2015-07-27 20:36:00 +00:00
link: http://redsymbol.net/articles/bash-exit-traps/
title: 'Useful Bash features: exit traps'
topic: Shell scripting
---

I recently discovered exit traps, and I think they're a really neat feature of Bash.

Exit traps are a resilient way to handle cleanup code in Bash scripts. You "trap" a function on a special exit code, and then when the script exits, that function gets called – even if the script died unexpectedly. That means the cleanup work is always finished.

The linked article is a good introduction to traps. It explains how they works, and has several examples of how traps might be used. Here's another example from my recent work:

As part of my day job, I've been doing some tests to monitor the performance impact of our code. As the test runs, I have a shell script running alongside which records the load on the system.

At the end of the test, I want to save a copy of the logs, so that I can correlate events with the load on the system. I was doing it by hand, but I would often forget. Then I found exit traps, and the solution was simple. I added a few lines to my monitoring script:

<pre class="lng-bash"><code>function <span class="n">save_logs</span> <span class="p">{</span>
    if [[ -f /var/log/calico/felix.log ]]<span class="p">;</span> then
        mv /var/log/calico/felix.log <span class="s">"$TESTID"_felix.log</span>
    fi
<span class="p">}</span>

trap save_logs exit</code></pre>

and now I get a set of saved logs after every test.
It's reliable, robust, and one less thing for me to think about.

If you write any shell scripts yourself, I suggest you look at exit traps – I think you'll find them very useful.
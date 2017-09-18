---
date: 2015-07-27 20:36:00 +0000
layout: post
link: http://redsymbol.net/articles/bash-exit-traps/
slug: exit-traps-in-bash
summary: null
tags: bash shell-scripting
title: 'Useful Bash features: exit traps'
---

I recently discovered exit traps, and I think they're a really neat feature of Bash.

Exit traps are a resilient way to handle cleanup code in Bash scripts. You "trap" a function on a special exit code, and then when the script exits, that function gets called – even if the script died unexpectedly. That means the cleanup work is always finished.

The linked article is a good introduction to traps. It explains how they works, and has several examples of how traps might be used. Here's another example from my recent work:

As part of my day job, I've been doing some tests to monitor the performance impact of our code. As the test runs, I have a shell script running alongside which records the load on the system.

At the end of the test, I want to save a copy of the logs, so that I can correlate events with the load on the system. I was doing it by hand, but I would often forget. Then I found exit traps, and the solution was simple. I added a few lines to my monitoring script:

```bash
function save_logs {
    if [[ -f /var/log/calico/felix.log ]]; then
        mv /var/log/calico/felix.log "$TESTID"_felix.log
    fi
}

trap save_logs exit
```

and now I get a set of saved logs after every test.
It's reliable, robust, and one less thing for me to think about.

If you write any shell scripts yourself, I suggest you look at exit traps – I think you'll find them very useful.

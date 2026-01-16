---
layout: til
title: How to run a task on a schedule on macOS
summary: Create a `LaunchAgent` with a `StartCalendarInterval` or `StartInterval` that defines how often you want the task to run.
date: 2025-06-13 16:59:56 +01:00
tags:
  - macos
---
I've been doing a bunch of work recently where I use macOS LaunchAgents to run task on a schedule, as a fairly basic polling mechanism that's built into my system.

What's nice is that running LaunchAgent tasks is managed by the OS, so I don't need to worry about keeping a session running or fiddling with `nohup`.
I find them a bit finnicky to set up, but one they're running they're solid.

These are some quick notes and examples so I don't forget the general pattern.

## Running at a fixed time of day

If I want to run a LaunchAgent at the same time every day, I create a file like this in `~/Library/LaunchAgents`.

The example below runs at 1:30 and 7:30 (I'm not sure if that's UTC or the computer's timezone), and I'd save it as `net.alexwlchan.run_at_fixed_time.plist`.

It includes settings for writing logs from the program invoked by `ProgramArguments`.
Note that you have to create the output directory for the logs, or they won't be saved.

To start this running on its schedule, I need to run

```console
$ launchctl load net.alexwlchan.run_at_fixed_time.plist
```

I can similar run `launchctl unload` if I want to temporarily pause it.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>net.alexwlchan.run_at_fixed_time</string>
    <key>ProgramArguments</key>
    <array>
      <string>bash</string>
      <string>-c</string>
      <string>cd ~/repos/example-repo; source .venv/bin/activate; python3 run_script.py</string>
    </array>
    <key>StandardOutPath</key>
    <string>/Users/alexwlchan/logs/run_at_fixed_time.stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/alexwlchan/logs/run_at_fixed_time.stderr.log</string>
    <key>StartCalendarInterval</key>
    <array>
      <dict>
        <key>Hour</key>
        <integer>1</integer>
        <key>Minute</key>
        <integer>30</integer>
      </dict>
      <dict>
        <key>Hour</key>
        <integer>7</integer>
        <key>Minute</key>
        <integer>30</integer>
      </dict>
    </array>
  </dict>
</plist>
```

## Polling repeatedly

Here's another example of a LaunchAgent file, which will run roughly once a second.
I'm sure you can adjust the polling frequency, but I haven't had to yet.

I've used this to run basic queues, where the queue worker wakes up every second and looks for new work.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>net.alexwlchan.poll_every_second</string>
    <key>ProgramArguments</key>
    <array>
      <string>bash</string>
      <string>/Users/alexwlchan/poll_every_second.sh</string>
    </array>
    <key>StandardOutPath</key>
    <string>/Users/alexwlchan/logs/poll_every_second.stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/alexwlchan/logs/poll_every_second.stderr.log</string>
    <key>StartInterval</key>
    <integer>1</integer>
    <key>KeepAlive</key>
    <true/>
  </dict>
</plist>
```

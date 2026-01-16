---
layout: til
title: Run a script on macOS on a schedule using a LaunchAgent
date: 2024-01-22 11:54:52 +00:00
tags:
  - macos
---
I was setting up a script to run on a nightly schedule.
Based on a combination of bits I found on Google, I created the following plist file which I saved in `~/Library/LaunchAgents/net.alexwlchan.run_scheduled_task.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
 <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
 <plist version="1.0">
   <dict>
     <key>Label</key>
     <string>net.alexwlchan.run_scheduled_task</string>

     <key>ProgramArguments</key>
     <array>
       <string>/path/to/script.sh</string>
     </array>

     <key>StandardOutPath</key>
     <string>/path/to/script_logs.log</string>

     <key>StandardErrorPath</key>
     <string>/path/to/script_logs.err.log</string>

     <key>StartCalendarInterval</key>
     <dict>
       <key>Hour</key>
       <integer>1</integer>
       <key>Minute</key>
       <integer>45</integer>
     </dict>
   </dict>
 </plist>
```

To register the task so it runs in the background:

```console
$ launchctl load net.alexwlchan.run_scheduled_task
```

You can also unregister the task with `unload`:

```console
$ launchctl unload net.alexwlchan.run_scheduled_task
```

When I was working out the XML syntax, I ended up with a few cases where I had a broken task that was "loaded", and running `launchctl load` would throw an error.
I had to `unload; load` to get the new task working.

Or run it as a one-off task to check you've configured it correctly:

```console
$ launchctl start net.alexwlchan.run_scheduled_task
```

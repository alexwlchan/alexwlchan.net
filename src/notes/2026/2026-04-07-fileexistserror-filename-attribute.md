---
layout: note
date: 2026-04-07 21:50:30 +01:00
title: The `FileExistsError` exception exposes a `filename` attribute
summary: The `filename` attribute returns the name of the already-existent file as a string.
topic: Python
---
Here's a simple snippet that shows it returning a string attribute:

```python {"names":{"2":"out_file","6":"err"}}
try:
    with open("greeting.txt", "x") as out_file:
        out_file.write("hello world!")
except FileExistsError as err:
    print(repr(err.filename))  # 'greeting.txt'
```

It's not especially useful in this example because you already know the name of the file you're writing -- but I've found it useful with the `download_image()` function I wrote for [`chives.fetch`][chives-fetch].

The `download_image()` function takes a URL and an out prefix, looks at the `Content-Type` header of the response to decide the file extension, and returns the downloaded path.
I don't know what path it will use until I've got the server response.

The function won't overwrite existing images, so it throws a `FileExistsError` exception if the image already exists.
If I want to carry on anyway with the already-downloaded image, I can get the filename from the exception rather than re-calculating the filename or changing the API.

Here's another example:

```python {"names":{"1":"chives","2":"fetch","3":"download_image","4":"pathlib","5":"Path","6":"out_path","14":"err"}}
from chives.fetch import download_image
from pathlib import Path

try:
    out_path = download_image(
        url="https://alexwlchan.net/images/2026/470906.png",
        out_prefix=Path("example")
    )
    print(out_path)  # Path("example.png")
except FileExistsError as err:
    print(repr(err.filename))  # 'example.png'
```

The `filename` attribute comes from [`OSError`][pydoc-oserror-filename], of which `FileExistsError` is a subclass.

[chives-fetch]: https://github.com/alexwlchan/chives/blob/main/src/chives/fetch.py
[pydoc-oserror-filename]: https://docs.python.org/3/library/exceptions.html#OSError.filename

---
layout: til
title: You can set/update the `total` of a progress bar `tqdm` after it starts
summary: Update the `.total` attribute, then call `.refresh()`.
date: 2025-05-17 16:00:18 +0100
tags:
  - python
---
I use the [`tqdm` library][tqdm] to create progress bars in my terminal.

If you know the number of items upfront, you can pass a `total` to `tqdm.tqdm()`, for example:

```python
import time
import tqdm

with tqdm.tqdm(total=100) as pbar:
    for _ in tange(100):
        time.sleep(1)
```

But what if you don't know the size upfront?

It turns out you can set the `total` later, and then `tqdm` will use it when it redraws the progress bar.
Here's a simple example:

```python
import time
import tqdm

with tqdm.tqdm() as pbar:
    for _ in range(5):
        time.sleep(1)
        pbar.update(1)

        pbar.total = 5
        pbar.refresh()
```

I found this useful in a script where the generator was quite slow (fetching a list of video IDs from a YouTube playlist) and I wanted to start acting on the generator immediately (downloading the videos), but I also wanted a nice progress bar.

[tqdm]: https://pypi.org/project/tqdm/
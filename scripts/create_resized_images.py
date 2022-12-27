#!/usr/bin/env python3

import concurrent.futures
import itertools
import json
import os
import sys

from PIL import Image
import pillow_avif
import tqdm


def get_inputs():
    try:
        for line in open(".missing_images.json"):
            yield json.loads(line)
    except FileNotFoundError:
        return []


def process(line):
    try:
        im = Image.open(line["source_path"])
        im = im.resize((line["width"], int(im.height * line["width"] / im.width)))
        os.makedirs(os.path.dirname(line["out_path"]), exist_ok=True)
        im.save(line["out_path"])
    except Exception:
        print(line)
        raise


def concurrently(fn, inputs, *, max_concurrency=1):
    """
    Calls the function ``fn`` on the values ``inputs``.

    ``fn`` should be a function that takes a single input, which is the
    individual values in the iterable ``inputs``.

    Generates (input, output) tuples as the calls to ``fn`` complete.

    See https://alexwlchan.net/2019/10/adventures-with-concurrent-futures/ for an explanation
    of how this function works.

    """
    # Make sure we get a consistent iterator throughout, rather than
    # getting the first element repeatedly.
    fn_inputs = iter(inputs)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(fn, input): input
            for input in itertools.islice(fn_inputs, max_concurrency)
        }

        while futures:
            done, _ = concurrent.futures.wait(
                futures, return_when=concurrent.futures.FIRST_COMPLETED
            )

            for fut in done:
                original_input = futures.pop(fut)
                yield original_input, fut.result()

            for input in itertools.islice(fn_inputs, len(done)):
                fut = executor.submit(fn, input)
                futures[fut] = input


if __name__ == "__main__":
    total = len(list(get_inputs()))
    
    if total == 0:
        sys.exit(0)
    
    for i, o in tqdm.tqdm(concurrently(process, get_inputs()), total=total):
        pass

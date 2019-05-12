---
layout: post
date: 2019-05-01 20:59:07 +0000
title: Finding unused variables in a Terraform module
summary:
tags:
category: Programming and code
---

At work, we use [Terraform] to manage our infrastructure in AWS.
We use [modules] to reduce repetition in our Terraform definitions, and we publish them in a [public GitHub repo].
A while back, I wrote a script that scans our modules and looks for unused variables, so that I could clean them all up.

In this post, I'm going to walk through the script and explain how it works.
If you just want the script, you can [skip to the end](#putting-it-all-together).

[Terraform]: https://www.terraform.io/
[modules]: https://www.terraform.io/docs/configuration/modules.html
[public GitHub repo]: https://github.com/wellcometrust/terraform-modules



## What variables are defined by a single Terraform file?

There's a Python module [for parsing HCL][pyhcl] (the Terraform markup language), so let's use that -- much easier and more accurate than trying to detect variables manually.
Here's what that looks like:

```python
import hcl


def get_variables_in_file(path):
    try:
        with open(path) as tf:
            tf_definitions = hcl.load(tf)
    except ValueError as err:
        raise ValueError(f"Error loading Terraform from {path}: {err}") from None

    try:
        return set(tf_definitions["variable"].keys())
    except KeyError:
        return set()
```

The `hcl.load` method does the heavy lifting.
It returns a dictionary, where the keys are the different elements of the Terraform language -- `resource`, `variable`, `provider`, and so on.
Within the dictionary for each element, you get every instance of that element in the file.

For example, the following Terraform definition:

```hcl
variable "queue_name" {
  description = "Name of the SQS queue to create"
}

resource "aws_sqs_queue" "q" {
  name            = "${var.queue_name}"
  redrive_policy = "{\"deadLetterTargetArn\":\"${aws_sqs_queue.dlq.arn}\",\"maxReceiveCount\":${var.max_receive_count}}"
}

resource "aws_sqs_queue" "dlq" {
  name = "${var.queue_name}_dlq"
}
```

gets a dictionary a bit like this:

```python
{
  "resource": {
    "aws_sqs_queue": {
      "dlq": ...,
      "q": ...
    }
  },
  "variable": {
    "queue_name": ...
  }
}
```

Getting the list of keys in the `variable` block (if it's present) tells us the variables defined in this file.

Sometimes you'll discover the Terraform inside a file is just malformed (or the file is empty!) -- so we wrap the exception we receive to include the file path.
The `from None` disables exception chaining in Python 3, and makes the traceback a little cleaner.

[pyhcl]: https://pypi.org/project/pyhcl/



## What variables are defined by a Terraform module?

Once we can get the variables defined by a single file, we can get all the variables defined in a module.

A module is a collection of Terraform files in the same directory, so we can find them by using `os.listdir`, like so:

```python
import os


def tf_files_in_module(dirname):
    for f in os.listdir(dirname):
        if f.endswith(".tf"):
            yield f


def get_variables_in_module(dirname):
    all_variables = {}

    for f in tf_files_in_module(dirname):
        for varname in get_variables_in_file(os.path.join(dirname, f)):
            all_variables[varname] = f

    return all_variables
```

This returns a map from (variable name) to (file where the variable was defined).
If a variable turns out to be redundant, knowing which file it was defined in will be helpful when we go back to delete it.


## Does a module have any unused variables?

Once we have a list of variables defined in a module, we need to go back to see which of them are in use.
I haven't found such a good way to do this -- right now the best I've come up with is to look for the string `var.VARIABLE_NAME` in all the files.
It's a bit crude, but seems to work.

Here's the code:

```python
def find_unused_variables_in_module(dirname):
    unused_variables = get_variables_in_module(dirname)

    for f in tf_files_in_module(dirname):
        if not unused_variables:
            return {}

        tf_src = open(os.path.join(dirname, f)).read()
        for varname in list(unused_variables):
            if f"var.{varname}" in tf_src:
                del unused_variables[varname]

    return unused_variables
```

We start by getting a list of all the variables defined in the module.

Then we go through the files in the module, one-by-one.
If we don't have any unused variables left, we can exit early -- checking the rest of the files won't tell us anything new.
Otherwise, we open the file, read the Terraform source, and look for instances of the variables we haven't seen used yet.
If we see a variable in use, we delete it from the dict.

We have to iterate over `list(unused_variables)` rather than `unused_variables` itself, because we're deleting elements from that dict as we go along.
If you don't make it a list first, you'll get an error when you delete the first element: *"dictionary changed size during iteration"*.

If the module uses all of its variables, we get back an empty dict.
If there are unused variables, we get a dict that tells us which variables aren't being used, and which file they're defined in.


## Looking at all the modules in a repo

Our [terraform-modules repo][tfmods] defines dozens of modules, and I wouldn't want to check them all by hand.
Instead, it's easier (and faster!) to use [os.walk] to look through every directory in the repo.
For a quick speedup, we can look for filenames ending with `.tf` to decide if a particular directory is a module.

Here's some code:

```python
def find_unused_variables_in_tree(root):
    for mod_root, _, filenames in os.walk(root):
        if not any(f.endswith(".tf") for f in filenames):
            continue

        unused_variables = find_unused_variables_in_module(mod_root)

        if unused_variables:
            print(f"Unused variables in {mod_root}:")
            for varname, filename in unused_variables.items():
                print(f"* {varname} ~> {os.path.join(mod_root, filename)}")
            print("")
```

And I wrap that in a little main block:

```python
import sys


if __name__ == "__main__":
    try:
        root = sys.argv[1]
    except IndexError:
        root = "."

    find_unused_variables_in_tree(root)
```

This means I can pass a directory to the script, and it looks for unused modules under that directory -- or if I don't pass an argument, it looks in the current directory.

[tfmods]: https://github.com/wellcometrust/terraform-modules
[os.walk]: https://docs.python.org/3/library/os.html#os.walk


## Putting it all together

Here's the final version of the code:

```python
import os
import sys

import hcl


def get_variables_in_file(path):
    try:
        with open(path) as tf:
            tf_definitions = hcl.load(tf)
    except ValueError as err:
        raise ValueError(f"Error loading Terraform from {path}: {err}")

    try:
        return set(tf_definitions["variable"].keys())
    except KeyError:
        return set()


def tf_files_in_module(dirname):
    for f in os.listdir(dirname):
        if f.endswith(".tf"):
            yield f


def get_variables_in_module(dirname):
    all_variables = {}

    for f in tf_files_in_module(dirname):
        for varname in get_variables_in_file(os.path.join(dirname, f)):
            all_variables[varname] = f

    return all_variables


def find_unused_variables_in_module(dirname):
    unused_variables = get_variables_in_module(dirname)

    for f in tf_files_in_module(dirname):
        if not unused_variables:
            return {}

        tf_src = open(os.path.join(dirname, f)).read()
        for varname in list(unused_variables):
            if f"var.{varname}" in tf_src:
                del unused_variables[varname]

    return unused_variables


def find_unused_variables_in_tree(root):
    for mod_root, _, filenames in os.walk(root):
        if not any(f.endswith(".tf") for f in filenames):
            continue

        unused_variables = find_unused_variables_in_module(mod_root)

        if unused_variables:
            print(f"Unused variables in {mod_root}:")
            for varname, filename in unused_variables.items():
                print(f"* {varname} ~> {os.path.join(mod_root, filename)}")
            print("")


if __name__ == "__main__":
    try:
        root = sys.argv[1]
    except IndexError:
        root = "."

    find_unused_variables_in_tree(root)
```

When I originally ran this script, it turned up a lot of unused variables, and I cleaned up the entire repo in one go.
I don't use it very often, because the modules don't change as much as they used to, but it's useful to have it.
I run it once in a blue moon, and clean up anything it tells me about.

It even exposed a few bugs!
It flagged a variable as being unused, even though it was one we expected the module to be using.
When I went to look, I found a configuration error or a typo.
Fix that, the variable is now in use, and the script is happy.

I've also used this code to look for unused `local`s -- but I'll leave that as an exercise for the reader.

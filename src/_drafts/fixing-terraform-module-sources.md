---
layout: post
title: "Preparing for Terraform 0.12: fixing module sources"
summary: I wanted a quick way to find Terraform modules that had values that would break in 0.12. I used a Python script to do it.
category: Terraform
---

I've mentioned before that we use [Terraform][tf] to manage our infrastructure at Wellcome.
Terraform is a tool for doing [infrastructure as code][infra_code] -- everything that defines our AWS resources is kept as text files in a Git repo, alongside our application source code.

[tf]: https://en.wikipedia.org/wiki/Terraform_(software)
[infra_code]: https://en.wikipedia.org/wiki/Infrastructure_as_code

In Terraform, you can use [modules] to define a reusable collection of resources.
This is useful if you've got some resources that should all be created together, or you want to make sure that every instance of a resource has the same settings.

For example, maybe you're creating some S3 buckets, and you want every bucket to have the same access policy.
You could define a module that creates an S3 bucket with the right policy, which takes the name of the bucket as a variable.
Then you'd use the module to create all your buckets:

```hcl
module "important_bukkit" {
  source = "./s3_bucket"

  name = "my_important_bukkit"
}
```

[modules]: https://www.terraform.io/docs/configuration/modules.html

When you use a `module`, the `source` input tells Terraform where the module is defined -- that is, the files that tell it which resources the module should create.
Maybe it's in the Terraform Registry, or a GitHub repo, or a local path.

We're starting to upgrade our Terraform setup to [Terraform 0.12][tf_012].
The new version has some breaking changes, including a new version of HCL, the markup language used to write Terraform code.
(Although breaking changes are always annoying, I don't mind this one so much -- I'm getting to delete a lot of ugly workarounds I'd written for limitations in the old HCL.)

[tf_012]: https://www.hashicorp.com/blog/announcing-terraform-0-12/

One of the changes in Terraform 0.12 is that it's stricter about how you declare module sources.
Previously, if you put a raw string as the source, it would treat it as a local path.
So this example would be fine, and use the module defined in the `s3_bucket` directory:

```hcl
module "important_bukkit" {
  source = "s3_bucket"

  name = "my_important_bukkit"
}
```

If you try to run the snippet above in 0.12, you get an error:

> The module address "s3_bucket" could not be resolved.
>
> If you intended this as a path relative to the current module, use
> "./s3_bucket" instead. The "./" prefix indicates that the address is a
> relative filesystem path.

(One of the things I like in 0.12 is the improved error handling.)

We have a lot of modules that use local paths, and after I'd fixed this a few times, I decided to find all the places where we had these ambiguous sources, and fix them all at once.
It's a tiny change, and backwards-compatible with 0.11, so it won't break anything.
This is a perfect case for a throwaway Python script.

I doubt many people want this exact script, but I hope you'll learn something useful from the write-up anyway.



## Step 1: where are my Terraform files?

We need to start by finding all our Terraform files.
This is where the [os.walk() function][walk] in the Python standard library comes in handy.
It walks a directory tree, and generates tuples `(dirpath, dirnames, filenames)` -- for each directory `dirpath` in the tree, what directories and files does it contain?

Here's how to use it, printing a path to every Terraform file under the current directory:

```python
import os


for dirpath, _, filenames in os.walk("."):
    for f in filenames:
        if f.endswith(".tf"):
            path = os.path.join(dirpath, f)
            print(path)
```

[walk]: https://docs.python.org/3/library/os.html#os.walk

If you run this, you might see lots of entries in a `.terraform` directory.
This is a local cache of all the modules you're using, created by `terraform get`.
It's not important for this task, so let's skip it.

```python
import os


for dirpath, _, filenames in os.walk("."):

    # Skip the .terraform directory, which is a local cache of
    # downloaded modules that we don't care about.
    if ".terraform" in dirpath:
        continue

    for f in filenames:
        if f.endswith(".tf"):
            path = os.path.join(dirpath, f)
            print(path)
```

At this point, it's tempting to start doing work inside the body of the inner loop, but I prefer to pull it into its own function, which is a standalone generator of paths to Terraform files:

```python
def get_all_tf_paths():
    """
    Generates paths to all the .tf files under the current directory.
    """
    for dirpath, _, filenames in os.walk("."):

        # Skip the .terraform directory, which is a local cache of
        # downloaded modules that we don't care about.
        if ".terraform" in dirpath:
            continue

        for f in filenames:
            if f.endswith(".tf"):
                yield os.path.join(dirpath, f)


for path in get_all_tf_paths():
    print(path)
```

This means that rather than working inside a nested for loop, there's only one for loop at the top level.
That makes the code a bit simpler, gives us a reusable generator, and makes it easier to use control flow statements like `break` and `continue`.

I use os.walk() a lot, and I always create little generator functions like this.
As I'm writing a new script, I like to test on one file to start with, before I run the whole set.
Because there's only one loop, I can process one file and then `break`.



## Step 2: what modules is this Terraform file using?

Now we've got paths that point to Terraform files.
Let's open those files and see what they contain.

There's a PyPI module for parsing Terraform syntax ([pyhcl]), so let's use that:

```python
import hcl


for path in get_all_tf_paths():
    tf = hcl.load(open(path))
    print(path)
    print(tf)
    break
```

[pyhcl]: https://pypi.org/project/pyhcl/

You get an output that looks something like this:

```
./reindexer/terraform/outputs.tf
{'output': {'topic_arn': {'value': '${module.reindex_worker.topic_arn}'}}}
```

The first key is the type of Terraform object you're creating (`output`, `resource`, `module`, and so on), the second key is the name of the object, the third key is the inputs being passed to that object.
This example comes from the following Terraform source:

```hcl
output "topic_arn" {
  value = "${module.reindex_worker.topic_arn}"
}
```

We can look up the modules in a file like so:

```python
for path in get_all_tf_paths():
    tf = hcl.load(open(path))

    try:
        modules = tf["module"]
    except KeyError:
        continue

    print(f"{path} has modules: {modules}")
```

If the file doesn't use any modules, we can skip doing anything else.

I originally wrote `modules = tf.get("module", {})`, then replaced it with `try … except KeyError`.
Although it's more verbose, it doesn't rely on knowing what an "empty" value looks like in this context, so it's more future-proof against changes to the output of `hcl.load`.
That's not important in a one-off script, but it's a useful habit to get into.

If you run this over the whole repo, you might get a ValueError on the `hcl.load()` line.
This means the file has invalid Terraform syntax, so pyhcl can't parse it.
This could be a malformed file, or it could be one that's already been upgraded to 0.12 -- either way, we can't do anything useful, so let's skip it:

```python
import sys


for path in get_all_tf_paths():
    try:
        tf = hcl.load(open(path))
    except ValueError as err:
        # Invalid HCL, possibly Terraform 0.12?
        print(f"Could not parse {path}: {err}", file=sys.stderr)
        continue

    ...
```

[Errors should never pass silently][zen], so I don't want to ignore those files completely, but sending the message to stderr means it's separate from other output from `print()`.
If I was running in a big codebase, I could split the messages about invalid HCL and ambiguous module sources, and inspect them separately.

[zen]: https://www.python.org/dev/peps/pep-0020/



## Step 3: Is any module using an ambiguous source?

Now we have the modules, we can loop over them and check the `source` field.
Something like:

```python
for path in get_all_tf_paths():
    ...

    for mod_name, mod_inputs in modules.items():
        mod_source = mod_inputs["source"]
        print(f"{path}: module {mod_name} has source {mod_source}")
```

(Notice that this is a double-nested loop, like we had in step 1.
I'm not going to pull it out as a generator right now, but I've done it below.)

We could inspect the output from this manually, but it gets quite long -- I ran this in one of our repos, and there are 138 lines of output.
Let's filter out module sources that we know are fine.

To do this, I glanced at the output, and started writing checks to filter out common patterns:

```python
for path in get_all_tf_paths():
    ...

    for mod_name, mod_inputs in modules.items():
        mod_source = mod_inputs["source"]

        if mod_source.startswith(("git::", "github.com", "./", "../")):
            continue

        print(f"{path}: module {mod_name} has source {mod_source}")
```

This gave me a list of a dozen modules where the source was an unadorned local path.
I went in and fixed them by hand, then ran the script a second time to confirm I'd fixed them all.
And voila!
I've fixed all the ambiguous module sources, in a script that only took me a few minutes to write.


## Putting it all together

Below is the final version of the script.
It's a bit neater than what I actually ran, because I've tidied it up for the blog post, but it's the same basic structure.

```python
#!/usr/bin/env python
# -*- encoding: utf-8

import os
import sys

import hcl


def get_all_tf_paths():
    """
    Generates paths to all the .tf files under the current directory.
    """
    for dirpath, _, filenames in os.walk("."):

        # Skip the .terraform directory, which is a local cache of
        # downloaded modules that we don't care about.
        if ".terraform" in dirpath:
            continue

        for f in filenames:
            if f.endswith(".tf"):
                yield os.path.join(dirpath, f)


def get_all_modules():
    """
    Generates tuples of (path, module_name, module_inputs) for all the modules
    defined in .tf files under the current directory.
    """
    for path in get_all_tf_paths():
        try:
            tf = hcl.load(open(path))
        except ValueError as err:
            # Invalid HCL, possibly Terraform 0.12?
            print(f"Could not parse {path}: {err}", file=sys.stderr)
            continue

        try:
            modules = tf["module"]
        except KeyError:
            continue

        for mod_name, mod_inputs in modules.items():
            yield (path, mod_name, mod_inputs)


if __name__ == "__main__":
    for (path, mod_name, mod_inputs) in get_all_modules():
        mod_source = mod_inputs["source"]

        if mod_source.startswith(("git::", "github.com", "./", "../")):
            continue

        print(f"{path}: module {mod_name} has source {mod_source}")
```

If you're running Terraform 0.11 and haven't upgraded to 0.12 yet, you might want to run this script so you can fix your own module references.
Adding `./` or `../` works fine in 0.11, so you can do this even if you have no immediate plans to upgrade.

If not, I hope you found the post interesting, and picked up a tip or two to use the next time you're writing your own scripts.

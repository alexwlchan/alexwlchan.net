---
title: Two shortcuts for using S3 in the shell
summary: Two shell functions for editing and inspecting S3 objects as if they were local files.
tags: aws
---

I often find myself needing to edit or inspect the contents of a text file stored in S3.

For example, at work we have a [Terraform variables file][tfvars] kept in a private S3 bucket.
This contains configuration that we don’t want to put in a public repository – passwords, API credentials, usernames, and so on.
If I want to add a new secret to this file, I need to download the existing file, make an edit, then re-upload the file under the same key.
It isn’t hard, but it’s moderately tedious to do these steps manually.
 
[tfvars]: https://www.terraform.io/docs/configuration/variables.html#variable-files

Any time you have a repetitive and tedious task, it’s worth trying to find a way to automate it.
To that end, I have a function in my shell config that simplifies the process of editing an text file in S3.
The function is written for fish, but the concept could be adapted for any shell.
It opens the file in my preferred text editor, which is TextMate (invoked with `mate`).

```shell
function s3mate
  set s3key $argv[1]
  set localname (basename $argv[1])

  pushd (mktemp -d)
    # Download the object from S3.  Although we're in a temporary
    # directory, give it a nice name for the sake of the editor.
    aws s3 cp "$s3key" "$localname"
    cp "$localname" "$localname.copy"
    
    # Open the file in an editor.  The '-w' flag to 'mate' means
    # "wait until the file has closed before continuing".
    mate -w "$localname"

    # Is the file different to the original version?  If so, save
    # a new copy to S3.
    cmp "$localname" "$localname.copy" >/dev/null
    if [ "$status" != "0" ]
      aws s3 cp "$localname" "$s3key"
    end
  popd
end
```

I call it from a shell by passing it an s3:// URI.
For example:

```console
$ s3mate s3://private-bucket/terraform.tfvars
```

This download the object *terraform.tfvars* from *private-bucket* into a temporary directory, and opens it in TextMate.
I can edit the file as much as I like, then I save and close it.
Once the file is closed, it checks to see if I’ve changed anything with [cmp(1)][cmp].
If I’ve made changes, it uploads a new copy of the file to the original key.

[cmp]: https://linux.die.net/man/1/cmp

If lots of people were editing this file at once, this approach wouldn’t be safe – I could download and start editing, and somebody else could change the file at the same time.
When I uploaded my new version, I’d delete their changes.
There’s no safe way to protect against this in S3 – it has no support for transactional updates.
Even if you checked the object in S3 hadn’t changed before uploading, it could still change between the check and the upload.

In practice, it’s rare for me to work on a file that has multiple editors, so this isn’t an issue for me – but it is worth noting.

Once I had this function, it was only a small tweak to get a version that inspects files, but doesn’t edit them.
Viz:

```shell
function s3cat
  set s3key $argv[1]
  set localname (basename $argv[1])

  pushd (mktemp -d)
    aws s3 cp "$s3key" "$localname"
    cat "$localname"
  popd
end
```

The name is to match [cat(1)][cat].

[cat]: https://linux.die.net/man/1/cat

I’ve had both of these in my shell config for a while now, and they’ve been quite useful.
Neither is a massive time saver, but they save me a few seconds each time I use them.

S3 isn't actually a local filesystem, and it's risky to treat it as such.
But for quick file edits, these functions help paper over the difference.

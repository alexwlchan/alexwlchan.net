---
layout: post
date: 2018-05-04 08:28:01 +0000
title: Beware of logged errors from subprocess
tags: python security
summary: If you use Python's subprocess module, be careful you don't leak sensitive information in your error logs.
category: Programming and code

index:
  best_of: true
---

Yesterday, Twitter [wrote a blog post][twitter] about a recent security bug:

> When you set a password for your Twitter account, we use technology that masks it so no one at the company can see it. We recently identified a bug that stored passwords unmasked in an internal log. We have fixed the bug, and our investigation shows no indication of breach or misuse by anyone.

Quite by chance, I spent yesterday fixing a similar bug.
I was a bit careless when using the [subprocess module][subprocess], and leaked some AWS credentials into a public CI log.

<!-- summary -->

## The faulty code

Here's a snippet from one of our CI scripts:

```python
import shlex
import subprocess


def ecr_login():
    """Authenticates for pushing to ECR."""
    command = subprocess.check_output([
        'aws', 'ecr', 'get-login', '--no-include-email'
    ]).decode('ascii')
    subprocess.check_call(shlex.split(command))
```

This is part of a script that builds a Docker image, then pushes that image to ECR, a container registry in AWS.
Using [*aws ecr get-login*][get-login] gives us a *docker login* command we can use to authenticate with ECR.
We run that command, and then we can push images to ECR.

The *docker login* command we're about to run includes a password, so we don't want to log that anywhere -- but we aren't logging it, right?

Right?

But I'd forgotten that when the command run by *check_call* or *check_output* fails, you get a CalledProcessError -- **and tracebacks for CalledProcessError include the command you were trying to run**.
This is helpful if you're trying to debug something, but risky if your command contains something sensitive.

So when the *docker login* call flaked out, we got the following traceback in our [public CI logs][cilog]:

```
*** Authenticating for `docker push` with ECR
WARNING! Using --password via the CLI is insecure. Use --password-stdin.
Error response from daemon: Get https://760097843905.dkr.ecr.eu-west-1.amazonaws.com/v2/: dial tcp: lookup 760097843905.dkr.ecr.eu-west-1.amazonaws.com on 169.254.169.254:53: no such host
Traceback (most recent call last):
  File "/builds/publish_service_to_aws.py", line 96, in <module>
    ecr_login()
  File "/builds/publish_service_to_aws.py", line 62, in ecr_login
    subprocess.check_call(shlex.split(command))
  File "/usr/lib/python3.6/subprocess.py", line 291, in check_call
    raise CalledProcessError(retcode, cmd)
subprocess.CalledProcessError: Command '['docker', 'login', '-u', 'AWS', '-p', 'eyJwYXlsb2FkIjoiMTZIQUkycWh1UU9pNldJeFRFUS9qQzJ3U1NCbEZ0bis0NUVZajZsWHRtb2FEa2tLWWNYZ0ZWdlRITzJpZy9VcjZ4amZhZVRBRi9xRXJidkFpa0JYV1BnY2c2SnVraVlDbmxKUUJPZHNhSmQ4RVlyeGhmQ1pWYzBIdGx0V1dVYll6ZlpudnVRVktxWGJ3TnR3TWcwVlJ1aUo2Z0ExS0Zka2FIa3RwcURhWmNOOStVSGsyNWc5TGttSEVLMlhHUmQ1dFBqa2VGWDY2c2NSajhtOExpdlVqY3ZlWkZBdElxaGcyRkcyc1o1WFlEa2dZK1pFUmVWTHIvNGJsY2FGQkNReGYyajh0dWR2NXFwUnA1dndHNjBxQXg1bThyVEg2Z1FPVm9CdG1QLzl6L1dTcms1UVhnYzkvcXJJZHNDNUFMODdJd0FxZkw1MFhZK3ZrUDVLQ3pDYm5MOUl6MUxORU5naGdLRU5VRHViZ2IvZU5MUXR0eDFnUTJ6RE4vVDNVVlRmeE9ua3E1TEN5cy91OEZ6eC9ubmpsR2ZrUFpvdXBhWFRZMTZJaDJ4SkZqK3NzdUpuaFNYN1RTTGZKVzFtVVBHODd2Yk1PZ0YwOGJiUVNFUVU1SE9rVDkvbm91dEZ5TEt3U1h0Vm5oNDBEVVJBSzBwQUNubkIxajNvQjhDSmFDT0dFN2xubFZ4Q1VWck9Keko4ZGF3SnpERG1lL0ZvUFNNSDFKQVM2cFhtREo2bDRrdVB6MncvZXI2UmUzaGtvdXVBK2hHNnVFdmpBUnorcDVYYk9kZmpSd3BxY2kybUw0RDBxL0M1dk1MSGNhcVpmRE9qQWgwakdBZWxRdHdMb0s0ejBmVG9SNzNYYXlNZ3dLWVd2WXNweTQ5eS9wTUJmYjh2aGRFRThDaUlHNWJVSzl4NTJzL2kvSXdVYnppZmw1NndQYW94WW45VjUrTldaaVU5TncxOU9XOUo4dlJNV2Q5UjNvbVFSR0JLend6bk5DRHpLN2FUdU1CK2NhcmF0MjNDWXV1dXByY2N5Ykc0MDh1aFBoU0VTVDBxS2lRL1ZZMEo0cUtlQ0V5MDlGakhpWGE3VFh2QU9jTEt1dzRtTzMxK0hpZlVyNXRRRHpwb0RKbTRld05Hck1zS3JUdVNRdkYxQVc5RnBOT1RHdXBhY28wVjNqWDlZY242SEdRTVBnaE81VTV3ZjZHMkNhc3VHMUNOTk1TTzBmQ1pPK3prVTJsYkp0bnd4MklLYzJLcDlqdmNNR08wSmd4cXRNZExhNDFZRi9JcGlGcWttODRpckpadEFYVVdNN0FveW9zQXVGVDR0OEVqOHVXSW9JOVczZEt2UURBdXdodVYzNUFJVXhZWWo1elNYcVp0OG9yL0lBVVBmTlJQNVJvR2xha25MNDNHZTc0cVhZdXBNSzJwTlRPdzNjbFJXTUZuU0VsK21Uc1c0cEU4bkVCaHBPNDhOSUxoTkxzcWdaVUoiLCJkYXRha2V5IjoiQVFFQkFIaCtkUytCbE51ME54blh3b3diSUxzMTE1eWpkK0xOQVpoQkxac3VuT3hrM0FBQUFINHdmQVlKS29aSWh2Y05BUWNHb0c4d2JRSUJBREJvQmdrcWhraUc5dzBCQndFd0hnWUpZSVpJQVdVREJBRXVNQkVFREhqWlJRenJ4SFlJVG9nYmh3SUJFSUE3Mk1xbnp1a0ZMNjZZK2lWZVNRMVZLcEhnbld3OFBnY2Qzd2FPU0taRHFMMEFNWkovaDdOaDF2eDZ3bE5QbzIzNTQ5YlVtNzI2cWFmN1NLVT0iLCJ2ZXJzaW9uIjoiMiIsInR5cGUiOiJEQVRBX0tFWSIsImV4cGlyYXRpb24iOjE1MjUzODE0MTN9', 'https://760097843905.dkr.ecr.eu-west-1.amazonaws.com']' returned non-zero exit status 1.
```

And suddenly anybody has a password that can push images to our ECR repositories.

We were lucky -- the build failure sent us an email, and we were able to delete the compromised credentials pretty quickly.
We followed up with a complete rebuild, so if somebody *did* push a malicious image to ECR, it was quickly replaced.

There are two approaches you could use to prevent making the same mistake.

[get-login]: https://docs.aws.amazon.com/cli/latest/reference/ecr/get-login.html
[cilog]: https://travis-ci.org/wellcometrust/platform/jobs/374305606

## Use low-level subprocess APIs

One approach is to eschew the *check_call* and *check_output* APIs, use lower-level subprocess features, and do the error checking yourself.

For example, for *check_call*:

```python
rc = subprocess.call(sensitive_command)
if rc != 0:
    raise RuntimeError('The sensitive command failed!')
```

And to replicate *check_output*:

```python
proc = subprocess.Popen(sensitive_command, stdout=subprocess.PIPE)
stdout, _ = proc.communicate()

if proc.returncode != 0:
    raise RuntimeError("The sensitive command failed!")
```

## Catch the CalledProcessError

You could use `try … except` to catch the CalledProcessError, and raise a different exception:

```python
# Python 2 only
try:
    subprocess.check_call(sensitive_command)
except subprocess.CalledProcessError:
    raise RuntimeError("The sensitive command failed!")
```

If you run this code in Python 3, you'll get a nasty surprise.
Because of the new [exception chaining][chaining], the traceback for the RuntimeError includes both exceptions -- including the CalledProcessError we're trying to hide:

```
Traceback (most recent call last):
  File "foo.py", line 4, in <module>
    subprocess.check_call(['less', '/dev/null'])
  File "/usr/local/Cellar/python/3.6.4_4/Frameworks/Python.framework/Versions/3.6/lib/python3.6/subprocess.py", line 291, in check_call
    raise CalledProcessError(retcode, cmd)
subprocess.CalledProcessError: Command '['less', '/dev/null']' returned non-zero exit status 1.

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "foo.py", line 6, in <module>
    raise RuntimeError("The sensitive command failed!")
RuntimeError: The sensitive command failed!
```

If we want to suppress the original error, we need to [add `from None` to our `raise` statement][suppress]:

```python
# Python 3 only
try:
    subprocess.check_call(sensitive_command)
except subprocess.CalledProcessError:
    raise RuntimeError("The sensitive command failed!") from None
```

And now only the RuntimeError will be printed.

[suppress]: https://stackoverflow.com/a/33822606/1558022
[chaining]: https://www.python.org/dev/peps/pep-3134/
[twitter]: https://blog.twitter.com/official/en_us/topics/company/2018/keeping-your-account-secure.html
[subprocess]: https://docs.python.org/3/library/subprocess.html
[chain]: https://www.python.org/dev/peps/pep-3134/

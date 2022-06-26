---
layout: post
date: 2020-05-10 09:11:55 +0000
title: Make it safe to admit mistakes
summary: You can't stop people making mistakes, but you can make it more likely that they'll admit their next mistake to you.
---

Most software developers have stories about how they broke their production environment.
Here's one of mine, from last week.

At Wellcome, we store our digital archive in S3 buckets.
When we upload new files, their checksums are verified against an external manifest.
Once a file has been uploaded, we don't want it to be modified or deleted.

We already block users from modifying objects in the bucket with per-user permissions (IAM), but this doesn't prevent somebody creating a new user that did have those permissions (whether accidentally or maliciously).
I thought it would be a good idea to apply a bucket-level policy that blocked unwanted modifications from *everybody*, and only allowed access to a small list of pre-approved applications.
Brimming with confidence, I tried to write and apply such a policy.

Unfortunately, what I actually did was switch the entire bucket into read-only mode, so *nobody* could write to the bucket, and we couldn't store new files.
Not only that, the bucket policy itself also became read-only, so I couldn't revert my mistake.

When I realised I'd done this, I felt terrible.
It's blocked new ingests for at least a fortnight.

There are ways to fix this.
You can contact AWS support, or you can use your root account to change the bucket policy.
The root account can [always modify bucket policies](https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketPolicy.html).
(Amazon say this is "as a security precaution", which is their polite way of saying "if you do something daft".)
But the specific fix isn't the point of this post; what's important is how my coworkers reacted.

I was very apologetic and conciliatory and I felt like I screwed up.
My coworkers reassured me that it wasn't my fault -- we all make mistakes, and I was just the unlucky one today.
**They didn't try to blame me or make me feel worse for my mistake.**

Part of this is because they recognise that [complex systems have complex failures](/2020/04/complex-failures/), and it's never a single person at fault.
Although I was the one who pushed the button, it would have been better if there hadn't been a button for me to press.
(And indeed, we're changing how we handle bucket policies so at least two people review every future change, making this sort of mistake less likely.)

But there's another reason why this was a good thing for them to do.

We all make mistakes.
However many guardrails or safety checks we use, we'll still make mistakes.
Nothing will change this.
**What we can change is what somebody does when they make a mistake.**

**If you get angry, aggressive or judgemental when somebody makes a mistake, you're training them not to tell you about their next mistake.**
If admitting a mistake is unpleasant experience, people will try to avoid it -- either by covering it up, or trying to fix it themselves.
Neither outcome is desirable.

When something goes wrong, the safest thing to do is to pause, take stock, and think carefully before changing anything else.
A rushed fix can often make things worse, and it's how a problem goes from bad to catastrophic.

**If you're reassuring and gentle when somebody makes a mistake, they're more likely to tell you about their next mistake.**
That means you can work together to fix the problem, and they'll be less stressed as they're doing it.
Once it's resolved, you can add new safety checks to avoid the exact same problem happening in future.

This is an example of a more general thene: if you want people to trust you, you need to [make yourself safe to tell things to](https://notebook.drmaciver.com/posts/2020-04-06-15:20.html).
I already felt terrible when I realised I'd broken production, and nothing my co-workers could have said would have make me feel worse.
Instead, they made me feel better, we came up with a sensible fix for the issue, and it's more likely I'll admit the next mistake I inevitably make.

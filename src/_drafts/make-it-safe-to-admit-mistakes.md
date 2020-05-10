---
layout: post
title: Make it safe to admit mistakes
summary: Making mistakes is part of being human, and you can't change that. What you can change is how people react when they make one.
---

Most software developers have at least one story about how they broke their production environment.
I have one from just a week ago.

At Wellcome, we store digital archive in a couple of S3 buckets.
When we upload new files, their checksums are verified against an external manifest.
Once a file has been uploaded, we don't want it to be modified or deleted.
We already block users from changing the bucket in the per-user permissions (IAM), but this doesn't prevent somebody creating a new user that did have those permissions (whether accidentally or maliciously).
I thought it would be a good idea to apply a bucket-level policy that blocked unwanted modifications, and only allowed access to a small list of pre-approved applications.

Unfortunately, what I actually did was switch the entire bucket into a read-only mode, so *nothing* could write to the bucket, and we couldn't store new files.
Not only that, the bucket policy also became read-only, so I couldn't easily revert my mistake.

There are ways to fix this.
You can contact AWS support, or you can use your root account to change the bucket policy.
The root account is [always able to modify bucket policies](https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketPolicy.html).
(Amazon say this is "as a security precaution", which is their polite way of saying "if you do something daft".)

When I realised I'd done this, I felt terrible.
It took a week for us to notice, and it's blocked new ingests for another week.
What's important is what happened next.

I was very apologetic and conciliatory and I felt like I screwed up.
My coworkers reassured me that it wasn't my fault -- we all make mistakes, and I was just the unlucky one today.
They didn't try to blame me or make me feel worse for my mistake.

Part of this is because they recognise that complex systems have complex failures, and it's never a single person at fault.
Although I was the one who pushed the button, it would have been better if there hadn't been a button for me to press.
(And indeed, we are going to be changing how we handle bucket policies so at least two people review every change, making this sort of mistake less likely.)

But there's another reason why this was a good thing for them to do.

When something goes wrong, the safest thing to do is to pause, take stock, and think carefully before trying to fix it.
A rushed fix can often make things worse.

We all make mistakes.
However many guardrails or safety checks we use, we'll still make mistakes.
Nothing will change this.
What we can change is what somebody does when they make a mistake.

If you're reassuring and gentle when somebody makes mistake, they're more likely to tell you about their next mistake.
That means they can get help your help as they're trying to fix it, and you can both make plans to avoid similar mistake happening in future.

If you get angry or aggressive or judgemental when somebody makes a mistake, you're training them not to tell you about their next mistake.
If admitting a mistake isn't unpleasant experience, people will try to avoid admitting mistakes.
One way they might do this is to to try to fix it themselves, when they're already stressed and under pressure, and this is when a problem can go from bad to catastrophic.

This is an example of a more general thene: if you want people to trust you, you need to make yourself safe to be around.
I already felt terrible when I realised I'd broken our pockets, and nothing my co-workers could have said wouldn't make me feel worse.
But what they did say make me feel better, and means it's more likely I'll admit the next mistake I make.

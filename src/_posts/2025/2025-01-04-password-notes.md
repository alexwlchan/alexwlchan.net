---
layout: post
date: 2025-01-04 11:02:13 +00:00
title: How I use the notes field in my password manager
summary: |
  I use notes as a mini-changelog to track the context and history of my online accounts.
  I write down why I created accounts, made changes, or chose particular settings.
tags:
  - infosec
  - taking notes
---
I use 1Password to store the passwords for my online accounts, and I've been reviewing it as a [new year cleanup task](/2015/1password/).
I've been deleting unused accounts, changing old passwords which were weak, and making sure I've enabled multi-factor authentication for key accounts.

Each 1Password item has a notes field, and I use it to record extra information about each account.
I've never seen anybody else talk about these notes, or how they use them, but I find it invaluable, so I thought it'd be worth explaining what I do.
(This is different from the [Secure Notes] feature -- I'm talking about the notes attached to other 1Password items, not standalone notes.)

Lots of password managers have a notes field, so you can keep notes even if you don't use 1Password.

I use the notes field as a mini-changelog, where I write dated entries to track the history of each account.
Here's some of the stuff I write down:

[Secure Notes]: https://1password.com/features/secure-notes/

## Why did I create this account?

If the purpose of an account isn't obvious, I write a note that explains why I created it.

This happens more often than you might think.
For example, there are lots of ticketing websites that don't allow a guest checkout -- you have to make an account.
If I'm only booking a single event, I'll save the account in 1Password, and without a note it would be easy to forget why the account exists.

## Why did I make significant changes?

I write down the date and details of anything important I change in an account, like:

* Updating the email address
* Changing the password
* Adding or removing authentication methods like passkeys
* Enabling multi-factor authentication

If it's useful, I include an explanation of *why* I made a change, not just what it was.

For example, when I change a password: was it because the old password was weak, because the site forced a reset, or because I thought a password might be compromised?
Somebody recently tried to hack into my broadband account, so I reset the password as a precaution.
I wrote a note about it, so if I see signs of another hacking attempt, I'll remember what happened the first time.

## Why is it set up in an unusual way?

There are a small number of accounts that I set up in a different way to the rest of my accounts.
I write down the reason, so my future self knows why and doesn't try to "fix" the account later.

For example, most of my accounts are linked to my `@alexwlchan.net` email address -- but a small number of them are tied to other email addresses.
When I do this, I wrote a note explaining why I deliberately linked that account to another email.
The most common reason I do this is because the account is particularly important, and if I lost access to my `@alexwlchan.net` email, I wouldn't want to lose access to that account at the same time.

## What are the password rules?

I write down any frustrating password rules I discover.
This is particularly valuable if those rules aren't explicitly documented, and you can only discover them by trial and error.
I include a date with each of these rules, in case they change later.

These notes reduce confusion and annoyance if I ever have to change the password.
It also means that when I'm reviewing my passwords later, I know that there's a reason I picked a fairly weak password -- I'd done the best I could given the site's requirements.

Here's a real example: *"the password reset UI won't tell you this, but passwords longer than 16 characters are silently truncated, and must be alphanumeric only"*.

## Do I have multi-factor authentication?

I enable multi-factor authentication (MFA) for important accounts, but I don't put the MFA codes in 1Password.
Keeping the password and MFA code in the same app is collapsing multiple authentication factors back into one.

If I do enable MFA, I write a note in 1Password that says when I enabled it, where to find my MFA codes, and where to find my account recovery codes.

For example, when I used hardware security keys at work, I wrote notes about where the keys were stored (*"in the fire safe, ask Jane Smith in IT to unlock"*) and how to identify different keys (*"pink ribbon = workflow account"*).
These details weren't sensitive security information, but they were easy to forget.

Sometimes I choose not to enable MFA even though it's available, and I write a note about that as well.
For example, Wikipedia supports MFA but it's described as ["experimental and optional"](https://meta.wikimedia.org/wiki/Help:Two-factor_authentication), so I've decided not to enable it on my account yet.


## Why doesn’t this account exist any more?

When I deactivate an account, I don't delete it from 1Password.
Instead, I write a final note explaining why and how I deactivated it, and then I move it to [the Archive](https://blog.1password.com/introducing-archive/).

I prefer this to deleting the entry -- it means I still have some record that the account existed, and I can see how long it existed for.
I've only had to retrieve something from the archive a handful of times, but I was glad I could do so, and I don't see any downside to having a large archive.

I also use the archive for accounts that I can't delete, but are probably gone.
For example, I have old accounts with utility companies that have been acquired or gone bust, and their website no longer exists.
My account is probably gone, but I have no way of verifying that.
Moving it to the archive gets it out of the way, and I still have the password if it ever comes back.

## What am I going to forget?

I'm not trying to create a comprehensive audit trail of my online accounts -- I'm just writing down stuff I think will be helpful later, and which I know I'm likely to forget.
It only takes a few seconds to write each note.

Writing notes is always a tricky balance.
You want to capture the useful information, but you don't want the note-taking to become a chore, or for the finished notes to be overwhelming.
I've only been writing notes in my password manager for a few years, so I might not have the right balance yet -- but I'm almost certainly better off than I was before, when I wasn't writing any.

I'm really glad I started keeping notes in my password manager, and if you've never done it, I'd encourage you to try it.

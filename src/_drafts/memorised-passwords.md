---
layout: post
title: The passwords I actually memorise
summary: Password managers promise you only need to remember one password, but I keep eight of them in my head to avoid a single point of failure.
tags:
  - infosec
---
The promise of a [password manager][wiki-password-manager] is that it remembers and autofills all of your passwords, so you only have to remember one -- the password that unlocks your password manager.

In practice, I have a handful passwords that I think worth memorising.
It's still a short list, but I'm not convinced that a single password is either sensible or feasible.
I generally trust my password manager, but I don't want it to be a single point of failure for my entire digital life.

## What passwords do I try to remember?

1.  **The login password for my computer.**
    I configure my Mac to sleep after a few minutes of inactivity, then ask for my login password when I try to resume.
    Although I often use Touch ID to log in, I remember this password because I still have to enter it multiple times a day.

2.  **The master password for my password manager.**
    This unlocks all of my other passwords.
    
3.  **The login passcode for my phone.**
    I use an alphanumeric password, and I remember it because I have to enter it multiple times a day.

4.  **My email password.**
    My email account is the gateway to all my other digital accounts.
    If I lost access to my password manager but could still receive email, I could reset my passwords and regain access to everything.

5.  **My remote backup password.**
    I have offsite backups of all of my computers with Backblaze.
    If all of my devices were destroyed at once (for example, in a house fire), this would allow me to retrieve files from my backups, even without access to my password manager.

6.  **The encryption password for my multi-factor authentication (MFA) recovery codes.**
    I have an MFA app on my phone, protected by Face ID or my passcode -- but in an emergency, I have single-use recovery codes I can use instead.
    These are stored in [an encrypted disk image][mfa-codes].

7.  **My Apple Account password.**
    I'm heavily enmeshed in the Apple ecosystem, and this account has powerful access to my devices, including remote wiping and backups.

8.  **The "memorable word" for my online banking.**
    When I log in to my bank account, my password manager autofills a password, and then I have to fill in three characters of a longer "memorable word".
    For example, I might be asked to enter the 1st, 5th, and 8th characters.

    I memorise this both for security and convenience.
    If somebody compromises my password manager, my bank account is safe -- and even if this was in my password manager, it can't fill in single characters this way.

All of these passwords are long, alphanumeric, and unique.

I have a regular calendar reminder to review them, and make sure I still remember them correctly.
This would be a useful feature in a password manager -- periodic tests on whether you still remember important passwords.

## Where are these passwords stored?

Although I've memorised all eight passwords, there are some copies elsewhere. 

Five of them are stored in my password manager, because it's convenient: my computer's login password, my phone's login passcode, my email password, my remote backup password, and my Apple account password.
(My email and Apple account are protected by multi-factor authentication, and the codes aren't in my password manager.)

Two of them aren't written down anywhere, but they might be soon: the master password for my password manager, and the encryption password for my MFA recovery codes.
At some point I'd like to change this, probably with a paper copy in a fire safe or similar.
This would allow my family to retrieve those passwords in an emergency.

The "memorable word" for my online banking isn't written down anywhere, and I doubt it ever will be.
If I lose access to my bank account and I'm really stuck, I can visit a physical branch.

## How would I regain access to my accounts?

Here's how I'd get back into my key accounts:

*   **Remote backups.**
    My Backblaze account is only protected with a password, not MFA.
    I have this memorised, so I could download files from my remote backups on any device.

*   **MFA recovery codes.**
    These are in an encrypted disk image in my remote backups.
    I've memorised the disk image password, so I could retrieve my MFA codes once I get to my remote backups.

*   **Email inbox.**
    This is protected by a password and MFA.
    I've memorised the password, and I could use an MFA recovery code to regain access to the account.

*   **Password manager.**
     I use 1Password.
    Logging in on a new device needs two secrets: my Master Password and [Secret Key][1p-secret-key].
    
    I remember the former, but the latter is a random UUID I don't type in or see regularly.
    Instead, I have a 1Password [Emergency Kit][1p-emergency-kit] which includes my Secret Key (but not my Master Password).
    I have a printed copy of this kit in my folder of important papers, and a digital copy in my disk image of MFA recovery codes.
    
    If I can get a copy of the Emergency Kit, I can regain access to my password manager.

## What passwords don't I remember?

There are a couple of important passwords you might expect me to memorise, but I don't:

1.  **The email password for my work email.**
    This password is stored in the password manager I use at work, and if I unexpectedly lost access, I'd contact the IT team for help.
    I don't need self-service recovery for this account.

2.  **The master password for my password manager at work.**
    For similar reasons to work email, I'd rely on the IT team to regain access in an emergency.

3.  **My banking app username or password password.**
    Logging into my bank requires three values: my username, the full-length password, and the "memorable information".
    I've memorised the memorable information, but not the username or password.
    If I need emergency access to my bank account, I can visit a high street branch.

## What scenario am I trying to prevent?

Imagine you lost all of your devices.
Could you regain access to your digital life?
That's my worst-case scenario that I'm trying to avoid, and these memorised passwords should be enough to bootstrap everything.

I can retrieve my MFA recovery codes from my remote backups, and then I can either log into my password manager and retrieve the current passwords, or log into my email inbox and reset all my passwords.
Either way, I'm back into my accounts.

This doesn't cover the scenario where I lose access to both my email inbox and my password manager, but that would be a catastrophic digital disaster.

It also doesn't cover the scenario where I'm incapacitated and a family member needs emergency access to my digital accounts.
That's something I'm planning to fix this year.
My plan is to purchase a fire safe that somebody else can open, in which I'd place printed instructions for access my password manager.
Inside my password manager, I'll have a note that explains what the key accounts are, which I can update regularly without reopening the safe.

I hope I can continue to rely on my password manager, and I never encounter one of these emergency scenarios -- but I feel better knowing I've tried to prepare.

[wiki-password-manager]: https://en.wikipedia.org/wiki/Password_manager
[mfa-codes]: /2026/recovery-codes/
[1p-secret-key]: https://support.1password.com/secret-key/
[1p-emergency-kit]: https://support.1password.com/emergency-kit/

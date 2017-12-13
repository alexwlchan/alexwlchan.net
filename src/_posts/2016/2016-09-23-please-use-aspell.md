---
date: 2016-09-23 07:40:00 +0000
layout: post
tags: writethedocs
title: aspell, a command-line spell checker
---

At this month's [WriteTheDocs London](https://www.meetup.com/Write-The-Docs-London/), there was a discussion of "docs-as-code".
This is the idea of using plain-text formats for your documentation, and storing it alongside your code -- as opposed to using a wiki or another proprietary format.
This allows you to use the same tools for code and for docs: version control, code review, text editors, and so on.
By making it easier to move between the two, it's more likely that docs will be written and updated with code changes.

But one problem is that text editors for programmers tend to disable spellcheck.
This is sensible for code: program code bears little resemblance to prose, and the spellcheck would be too noisy to be helpful.
But what about writing prose?
Where are the red and green squiggles to warn you of spelling mistakes?

To plug the gap, I'm a fan of the command-line spellchecker [aspell](http://aspell.net).

<!-- summary -->

## What is aspell?

aspell is a spell-checking tool that runs on the command-line.
I always have plenty of command-line windows open, so that works for me.
If you prefer graphical applications, you should probably try something else.
But a command-line tool can be very powerful, and allow you to batch process many files at once.

When you run aspell, it looks in a plain-text file for any word that it thinks might be misspelt, and offers to replace it.
It makes a few guesses of its own, or you can supply your own replacement.
It's easy to fix up spelling errors as it finds them.

Personally I find it an efficient and powerful way to spellcheck an entire directory of files.
When I post patches on GitHub that correct a bunch of spelling mistakes in a project's documentation, I'm almost certainly using aspell.

## Installing aspell

There are [installation instructions](http://aspell.net/man-html/Generic-Install-Instructions.html#Generic-Install-Instructions) on the aspell website which involve downloading and building from source.
In practice, I've found that it's simpler to install aspell using a package manager.

*   If you're using OS X, you can install aspell through [Homebrew](http://brew.sh):

    <div class="highlight"><pre><span class="gp">$</span> brew install aspell</pre></div>

* If you're using Ubuntu or Debian, try `apt-get`:

    <div class="highlight"><pre><span class="gp">$</span> apt-get install aspell</pre></div>

* On CentOS or RHEL, try `yum`:

    <div class="highlight"><pre><span class="gp">$</span> yum install aspell</pre></div>

* For Windows users, there are [pre-built binaries](http://aspell.net/win32/) on the aspell site, although I haven't tried those myself.

## Using aspell

To run spell-checking against a single file, you run the following command:

```console
$ aspell check <path_to_file.txt>
```

This reads the file, and for any words it thinks might be misspelt, it offers you an interface for fixing the word:

![](/images/2016/aspell-screenshot.png)

The interface highlights the problem word, and gives you several options:

* You can choose one of aspell's guesses for the correct spelling (the numbered options)
* You can supply your own replacement (type `r`)
* You can ignore this particular word, or add it to a custom dictionary, so you don't get warned about it again (type `i` or `a`)

If you decide to replace the word, aspell updates your copy of the file, and saves the original with `.bak` appended to the name.
This allows you to create a diff with just aspell's changes, so you can review them before committing.

When it's gone through the entire file, it drops you back to the command-line.

## Advanced usage

### Batch processing

Running aspell on a single file is fine, but that's not much less hassle than opening a file in your text editor and invoking the OS spellchecker manually.
The nice thing about a command-line tool is that we can batch process files, without explicitly opening each in turn.

For example, in the bash shell (Linux/OS X), I can check every file with a `.md` extension with the following command:

```console
$ for f in **/*.md; do aspell check $f; done
```

This is an efficient way to run spellcheck over an entire repository.
I've used this on several projects, and it always drops out spelling errors faster than I could find them by hand.

### Keep words in a personal dictionary

When you tell aspell to "add" a word to your dictionary, this tells aspell two things: don't flag this word as misspelt again, and consider it as a possible correction on other misspelt words.

Your personal dictionary is stored at <code>~/.aspell.<em>lang</em>.pws</code>, where <code><em>lang</em></code> is [one of the language codes](http://aspell.net/man-html/Supported.html#Supported) supported by aspell.
This file is fairly simple: a single header line, followed by a word per line for the rest of the file.

Here's an example of what that file might look like:

```console
$ cat ~/.aspell.en.pws
personal_ws-1.1 en 3
Bennet
Netherfield
Longbourn
```

To add new words to your personal dictionary, add new lines to this file, and update the word count in the header line.
The format of this file is described in more detail [in the aspell man page](http://aspell.net/man-html/Format-of-the-Personal-and-Replacement-Dictionaries.html#Format-of-the-Personal-and-Replacement-Dictionaries).

There's supposed to be a flag `--personal` that allows you to point to a file, and use that as your personal dictionary.
That would be useful for checking in your dictionary alongside your repository; unfortunately, I've never been able to use it successfully.

### Filter out format-specific markup

Some plain-text formats can look a bit like code.
They have special bits of syntax that describe the formatting, but which can confuse a spellchecker.
For example, HTML tags look a bit like English, but often use words that aren't in any dictionary.

Handily, aspell has [some filters](http://aspell.net/man-html/The-Options.html#The-Options) for coping with some types of markup.
You can tell it that a particular document is written in HTML or TeX, and it tries to avoid flagging the markup.
Annoyingly, it doesn't seem to have filters for Markdown or ReStructured Text (the two formats I work with most often), but it's worth knowing those filters are there.

## What aspell can't do

Spelling is necessary for a good document, but it's not sufficient.
aspell can't tell you if your document is grammatically correct, makes sense, or is in any way useful to the reader.

I treat aspell a bit like a code linter: it's a useful first step for checking something is correct, but it's no substitute for a another human.
---
layout: post
date: 2025-03-25 16:53:43 +0000
title: Whose code am I running in GitHub Actions?
summary: I wanted to know what third-party code I was using in my GitHub Actions. I was able to use standard text processing tools and shell pipelines to get a quick tally.
tags:
  - shell scripting
  - github
---
A week ago, somebody added malicious code [to the tj-actions/changed-files GitHub Action][compromise].
If you used the compromised action, it would leak secrets to your build log.
Those build logs are public for public repositories, so anybody could see your secrets.
Scary!

## Mutable vs immutable references

This attack was possible because it's common practice to refer to tags in a GitHub Actions workflow, for example:

<pre><code>jobs:
  changed_files:
    ...
    steps:
      - name: Get changed files
        id: changed-files
        uses: <mark>tj-actions/changed-files@v2</mark>
      ...</code></pre>

At a glance, this looks like an immutable reference to an already-released "version 2" of this action, but actually this is a mutable Git tag.
If somebody changes the `v2` tag in the `tj-actions/changed-files` repo to point to a different commit, this action will run different code the next time it runs.

If you specify a Git commit ID instead (e.g. `a5b3abf`), that's an immutable reference that will run the same code every time.

Tags vs commit IDs is a tradeoff between convenience and security.
Specifying an exact commit ID means the code won't change unexpectedly, but tags are easier to read and compare.

[compromise]: https://www.stepsecurity.io/blog/harden-runner-detection-tj-actions-changed-files-action-is-compromised




## Do I have any mutable references?

I wasn't worried about this particular attack because I don't use `tj-actions`, but I was curious about what other GitHub Actions I'm using.
I ran a short shell script in the folder where I have local clones of all my repos:

```shell
find . -path '*/.github/workflows/*' -type f -name '*.yml' -print0 \
  | xargs -0 grep --no-filename "uses:" \
  | sed 's/\- uses:/uses:/g' \
  | tr '"' ' ' \
  | awk '{print $2}' \
  | sed 's/\r//g' \
  | sort \
  | uniq --count \
  | sort --numeric-sort
```

This prints a tally of all the actions I'm using.
Here's a snippet of the output:

```
 1 hashicorp/setup-terraform@v3
 2 dtolnay/rust-toolchain@v1
 2 taiki-e/create-gh-release-action@v1
 2 taiki-e/upload-rust-binary-action@v1
 4 actions/setup-python@v4
 6 actions/cache@v4
 9 ruby/setup-ruby@v1
31 actions/setup-python@v5
58 actions/checkout@v4
```

I went through the entire list and thought about how much I trust each action and its author.

*   Is it from a large organisation like `actions` or `ruby`?
    They're not perfect, but they're likely to have good security procedures in place to protect against malicious changes.

*   Is it from an individual developer or small organisation?
    Here I tend to be more wary, especially if I don't know the author personally.
    That's not to say that individuals can't have good security, but there's more variance in the security setup of random developers on the Internet than among big organisations.

*   Do I need to use somebody else's action, or could I write my own script to replace it?
    This is what I generally prefer, especially if I'm only using a small subset of the functionality offered by the action.
    It's a bit more work upfront, but then I know exactly what it's doing and there's less churn and risk from upstream changes.

I feel pretty good about my list.
Most of my actions are from large organisations, and the rest are a few actions specific to my Rust command-line tools which are non-critical toys, where the impact of a compromised GitHub repo would be relatively slight.



## How this script works

This is a classic use of Unix pipelines, where I'm chaining together a bunch of built-in text processing tools.
Let's step through how it works.

<style>
  dd > p:first-child {
    margin-top: 0;
  }
</style>

<dl>
<dt>
  {% highlight shell %}
find . -path '*/.github/workflows/*' -type f -name '*.yml' -print0
{% endhighlight %}
</dt>
<dd>
  <p>
    This looks for any GitHub Actions workflow file – any file whose name ends with <code>.yml</code> in a folder like <code>.github/workflows/</code>.
    It prints a list of filenames, like:
  </p>
  <p><code>./alexwlchan.net/.github/workflows/build_site.yml<br/>
./books.alexwlchan.net/.github/workflows/build_site.yml<br/>
./concurrently/.github/workflows/main.yml
</code></p>
  <p>
    It prints them with a null byte (<code>\0</code>) between them, which makes it possible to split the filenames in the next step.
    By default it uses a newline, but a null byte is a bit safer, in case you have filenames which include newline characters.
  </p>
  <p>
    I know that I always use <code>.yml</code> as a file extension, but if you sometimes use <code>.yaml</code>, you can replace <code>-name '*.yml'</code> with <code>\( -name '*.yml' -o -name '*.yaml' \)</code>
  </p>
  <p>
    I have a bunch of local repos that are clones of open-source projects, and not my code, so I care less about what GitHub Actions they’re using.
    I excluded them by adding extra <code>-path</code> rules, like <code>-not -path './cpython/*'</code>.
  </p>
</dd>
<dt>
{% highlight shell %}
xargs -0 grep --no-filename "uses:"
{% endhighlight %}
</dt>
<dd>
  <p>
    Then we use <code>xargs</code> to go through the filenames one-by-one.
    The `-0` flag tells it to split on the null byte, and then it runs <code>grep</code> to look for lines that include <code>"uses:"</code> – this is how you use an action in your workflow file.
  </p>
  <p>
    The <code>--no-filename</code> option means this just prints the matching line, and not the name of the file it comes from.
    Not all of my files are formatted or indented consistently, so the output is quite messy:
  </p>
  <p><code>&nbsp;&nbsp;&nbsp;&nbsp;- uses: actions/checkout@v4<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;uses: "actions/cache@v4"<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;uses: ruby/setup-ruby@v1</code></p>
</dd>
<dt>
{% highlight shell %}
sed 's/\- uses:/uses:/g' \
{% endhighlight %}
</dt>
<dd>
  <p>
    Sometimes there's a leading hyphen, sometimes there isn’t – it depends on whether <code>uses:</code> is the first key in the YAML dictionary.
    This <code>sed</code> command replaces <code>"- uses:"</code> with <code>"uses:"</code> to start tidying up the data.
  </p>
  <p><code>&nbsp;&nbsp;&nbsp;&nbsp;uses: actions/checkout@v4<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;uses: "actions/cache@v4"<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;uses: ruby/setup-ruby@v1</code></p>
  <p>
    I know <code>sed</code> is a pretty powerful tool for making changes to text, but I only know a couple of simple commands, like this pattern for replacing text: <code>sed 's/old/new/g'</code>.
  </p>
</dd>
<dt>
{% highlight shell %}
tr '"' ' '
{% endhighlight %}
</dt>
<dd>
  <p>
    Sometimes the name of the action is quoted, sometimes it isn’t.
    This command removes any double quotes from the output.
  </p>
  <p><code>&nbsp;&nbsp;&nbsp;&nbsp;uses: actions/checkout@v4<br/>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;uses: actions/cache@v4<br/>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;uses: ruby/setup-ruby@v1</code></p>
  <p>
    Now I’m writing this post, it occurs to me I could use <code>sed</code> to make this substitution as well.
    I reached for <code>tr</code> because I've been using it for longer, and the syntax is simpler for doing single character substitutions: <code>tr '&lt;oldchar&gt;' '&lt;newchar&gt;'</code>
  </p>
</dd>
<dt>
{% highlight shell %}
awk '{print $2}'
{% endhighlight %}
</dt>
<dd>
  <p>
    This splits the string on spaces, and prints the second token, which is the name of the action:
  </p>
  <p><code>actions/checkout@v4<br/>
actions/cache@v4<br/>
ruby/setup-ruby@v1</code></p>
  <p>
    <code>awk</code> is another powerful text utility that I’ve never learnt properly – I only know how to print the nth word in a string.
    It has a lot of pattern-matching features I’ve never tried.
  </p>
</dd>
<dt>
{% highlight shell %}
sed 's/\r//g'
{% endhighlight %}
</dt>
<dd>
  <p>
    I had a few workflow files which were using carriage returns (<code>\r</code>), and those were included in the <code>awk</code> output.
    This command gets rid of them, which makes the data more consistent for the final step.
  </p>
</dd>
<dt>
{% highlight shell %}
sort | uniq --count | sort --numeric-sort
{% endhighlight %}
</dt>
<dd>
  <p>
    This sorts the lines so identical lines are adjacent, then it groups and counts the lines, and finally it re-sorts to put the most frequent lines at the bottom.
  </p>
  <p>
    I have this as a shell alias called <a href="/2016/a-shell-alias-for-tallying/"><code>tally</code></a>.
  </p>
  <p><code>&nbsp;&nbsp;&nbsp;6 actions/cache@v4<br>
&nbsp;&nbsp;&nbsp;9 ruby/setup-ruby@v1<br>
&nbsp;&nbsp;59 actions/checkout@v4</code></p>
</dd>
</dl>

This step-by-step approach is how I build Unix text pipelines: I can write a step at a time, and gradually refine and tweak the output until I get the result I want.
There are lots of ways to do it, and because this is a script I'll use once and then discard, I don't have to worry too much about doing it in the "purest" way -- as long as it gets the right result, that's good enough.

If you use GitHub Actions, you might want to use this script to check your own actions, and see what you're using.
But more than that, I recommend becoming familiar with the Unix text processing tools and pipelines -- even in the age of AI, they're still a powerful and flexible way to cobble together one-off scripts for processing data.

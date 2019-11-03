---
category: Python
date: 2017-03-25 11:27:00 +0000
index:
  best_of: true
layout: post
summary: I use Python-Markdown to render posts for my site. Here are a few examples
  of the extensions I'm using.
tags: python markdown
title: A few examples of extensions in Python-Markdown
---

I write a lot of content in Markdown (including all the posts on this site), and I use [Python-Markdown][pypi] to render it as HTML.
One of Python-Markdown's features is an [Extensions API][ext].
The package provides some extensions for common tasks – abbreviations, footnotes, tables and so on – but you can also write your own extensions if you need something more specialised.

After years of just using the builtin extensions, I've finally started to dip my toe into custom extensions.
In this post, I'm going to show you a few of my tweaked or custom extensions.

<!-- summary -->

## The perils of skimming the docs

The Python-Markdown documentation explains [how to use extensions][ref]:

>  The list of extensions may contain instances of extensions and/or strings
> of extension names.
>
> <pre>extensions=[MyExtension(), <span class="s1">&quot;path.to.my.ext&quot;</span>]</pre>

Every time I had to use Python-Markdown, I'd look at this paragraph, click straight through to the [extensions page][ext], copy the names of the extensions I wanted, and use them as strings.
But because that was enough to get me going, I never stopped to read the next paragraph on the reference page:

> The preferred method is to pass in an instance of an extension. Strings
> should only be used when it is impossible to import the Extension Class
> directly (from the command line or in a template).

Oops.

I've only recently gone back and read the reference page in full – and that's why I've only just discovered their full potential.

## Footnote markers as text, not emoji

One of the built-in extensions renders footnotes with the following syntax:

    Sometimes you are talking about something[^1] and you want to include a
    reference[^2].  You use a `[^1]` in the body, and `[^1]:` later for
    the footnote text.

    [^1]: What does something mean?
    [^2]: A pointer to the reference.

This is what it looks like rendered:

<blockquote> <p>Sometimes you are talking about something<sup id="fnref:2-1"><a class="footnote-ref" href="#fn:2-1" rel="footnote">1</a></sup> and you want to include a reference<sup id="fnref:2-2"><a class="footnote-ref" href="#fn:2-2" rel="footnote">2</a></sup>. You use a <code>[^1]</code> in the body, and <code>[^1]:</code> later for the footnote text.</p>
<div class="footnote"> <ol> <li id="fn:2-1"> <p>What does something mean?&nbsp;<a class="footnote-backref" href="#fnref:2-1" rev="footnote" title="Jump back to footnote 1 in the text">&#8617;&#xFE0E;</a></p> </li> <li id="fn:2-2"> <p>A pointer to the reference.&nbsp;<a class="footnote-backref" href="#fnref:2-2" rev="footnote" title="Jump back to footnote 2 in the text">&#8617;&#xFE0E;</a></p> </li> </ol> </div>
</blockquote>

In the footnote itself, there's a hook arrow that links back to the marker in the original text.
This symbol has two variants: text (&#8617;&#xFE0E;) and emoji (&#8617;&#xFE0F;).
The HTML entity for the arrow `&#8617;`, and you can force it to one of the two variants by appending `&#xFE0E;` or `&xFE0F;`, respectively.
See [Matias Singers' post about text/emoji variants][singers] for more detail.

By default, Python-Markdown only uses the base HTML entity `&#8617;` – which means its up to the OS to decide which variant to use.
For example, iOS defaults to using the emoji entity, whereas OS X sticks to text.
I prefer the text variant to the emoji variant, and so I want to append the `&#xFE0E;` in my documents.

This turns out to be a configuration option on the `FootnoteExtension`, like so:

```python
fn_extension = FootnoteExtension(configs={
    'BACKLINK_TEXT': '&#8617;&#xFE0E;',
})
```

And now by passing `fn_extension` instead of `'markdown.extensions.footnotes'`, I get footnote markers that look consistent across all devices.

[pypi]: https://pypi.org/project/Markdown/
[ext]: https://pythonhosted.org/Markdown/extensions/index.html
[ref]: https://pythonhosted.org/Markdown/reference/index.html
[singers]: http://mts.io/2015/04/21/unicode-symbol-render-text-emoji/

## Numbered code blocks

Python-Markdown also includes extensions for doing syntax-highlighting of code blocks – I used them several times in the last section.

One of the options on your code blocks is whether to include line numbers on your code blocks.
Here's an example with and without:

{% highlight python linenos %}
def hello_world(name):
    """Prints a friendly greeting."""
    print('Hello %s!' % name)
{% endhighlight %}

```python
def hello_world(name):
    """Prints a friendly greeting."""
    print('Hello %s!' % name)
```

Code blocks use four-space indents, and a shebang or triple-colon on the first line to indicate whether you want line numbers or not:

    Here's an example with and without:

        #!python
        def hello_world(name):
            """Prints a friendly greeting."""
            print('Hello %s!' % name)

        :::python
        def hello_world(name):
            """Prints a friendly greeting."""
            print('Hello %s!' % name)

But I don't like this syntax very much – I find it hard to remember which is which – and it's not compatible with [GitHub-Flavoured Markdown][gfm], which I use quite a lot elsewhere.
GFM uses triple backquotes and a language name for code blocks, like so:

    This is a GFM fenced code block:

    ```python
    def hello_world(name):
        """Prints a friendly greeting."""
        print('Hello %s!' % name)
    ```

Handily, Python-Markdown supports this syntax too, but it doesn't support switching line numbers on the fly.
That's something I find useful, so I created a new extension which adds that support.

With my new extension, I can add `linenums` to the language line, and it adds line numbering.
Like so:

    This GFM fenced code block would have line numbers:

    ```python linenums
    def hello_world(name):
        """Prints a friendly greeting."""
        print('Hello %s!' % name)
    ```

(As a nice benefit, all other GFM processors I've tried just ignore the `linenums` parameter.)

GFM-style fenced code blocks are provided by the [`FencedBlockPreprocessor`][fbp] class.
It has a rather messy regular expression that seeks out fenced code blocks in the text, which I modified to always look for my new `linenums` parameter.

```python
class LineNosFencedCodePreprocessor(FencedBlockPreprocessor):

    FENCED_BLOCK_RE = re.compile(r'''
(?P<fence>^(?:~{3,}|`{3,}))[ ]*         # Opening ``` or ~~~
(\{?\.?(?P<lang>[\w#.+-]*))?[ ]*        # Optional {, and lang
# Optional highlight lines, single- or double-quote-delimited
(hl_lines=(?P<quot>"|')(?P<hl_lines>.*?)(?P=quot))?[ ]*
linenums[ ]*
}?[ ]*\n                                # Optional closing }
(?P<code>.*?)(?<=\n)
(?P=fence)[ ]*$''', re.MULTILINE | re.DOTALL | re.VERBOSE)
```

My only addition is `linenums[ ]*` – so this preprocessor will _only_ find fenced code blocks with my new parameter.

I then override a couple of methods from `FencedBlockPreprocessor` which intercept the `run()` method (the method which processes the Markdown source) to always enable line numbers:

```python
    def __init__(self, md):
        super().__init__(md)

        for ext in self.markdown.registeredExtensions:
            if isinstance(ext, CodeHiliteExtension):
                self.codehilite_conf = ext.config
                self.checked_for_codehilite = True
                break

    def run(self, lines):
        self.codehilite_conf['linenums'][0] = True
        res = super().run(lines)
        self.codehilite_conf['linenums'][0] = False
        return res
```

I'm not entirely sure that's the optimal way to do it, but it's worked for me so far.

A preprocessor needs to be wrapped to be usable (this is cribbed from the source code for [`FencedCodeExtension`][fce]):

```python
class LineNosFencedCodeExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)
        md.preprocessors.add(
            'line_nos_fenced_block',
            LineNosFencedBlockPreprocessor(md),
            '>normalize_whitespace')
```

And voila, an extension that lets me use GFM-style fenced code blocks and enable line numbers on the fly.

[gfm]: https://help.github.com/categories/writing-on-github/
[fbp]: https://github.com/waylan/Python-Markdown/blob/b52293b2858138231795aa72aac1cf4799eb8da9/markdown/extensions/fenced_code.py#L37
[fce]: https://github.com/waylan/Python-Markdown/blob/b52293b2858138231795aa72aac1cf4799eb8da9/markdown/extensions/fenced_code.py#L26

## Performing text substitutions and corrections

Now let's go beyond tweaking the builtin extensions: let's look at two extensions I wrote from scratch.
The [extensions API docs][api] describe a couple of ways to build extensions.
The simplest is to use a *preprocessor*, which tidies up text before it goes to the core Markdown processor.

A preprocessor has a `run()` method which is passed a list of lines – from the original Markdown source – and which should return a list of modified lines.
This is a great place to perform simple text substitutions.

A practical example: in HTML, the entity `&nbsp;` is a [non-breaking space][nbs].
If you put a `&nbsp;` between two words, your browser will never insert an automatic line break between them when it's wrapping text to fit the screen.
It's useful for phrases that exist as a single entity – like "Dr.&nbsp;Jones", "Python 3", "OS X" – where splitting the two halves over different lines would make it slightly harder to read.

You could sprinkle `&nbsp;` throughout your Markdown source, but this is tedious and makes the source look ugly.
Why not have the computer insert them for you?

I have a substitution preprocessor that does this sort of text replacement for me.
Like so:

```python
class SubstitutionPreprocessor(Preprocessor):

    def __init__(self, substitutions):
        super().__init__()
        self.substitutions = substitutions

    def run(self, lines):
        new_lines = []
        for line in lines:
            for pattern, subn in self.substitutions.items():
                line = line.replace(pattern, subn)
            new_lines.append(line)
        return new_lines


class SubstitutionExtension(MarkdownExtensionMixin):
    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add('subn', SubstitutionPreprocessor(md), '_begin')
```

You pass a dict of substitutions to the constructor, and then the `run()` method applies each of those substitutions in turn.
I don't have to worry about doing it myself.

Here are some of the substitutions I have enabled for building this site:

```python
from collections import OrderedDict

substitutions = OrderedDict([
    ('OS X', 'OS&nbsp;X'),
    ('TextMate 2', 'TextMate&nbsp;2'),
    ('Python 2', 'Python&nbsp;2'),
    ('Python 3', 'Python&nbsp;3'),
    ('JK Rowling', 'JK&nbsp;Rowling'),

    ('LaTeX', '<span class="latex">L<sup>a</sup>T<sub>e</sub>X</span>'),
])

subn_extension = SubstitutionExtension(substitutions)
```

Note that I use an `OrderedDict`, so I can enforce the order in which substitutions are applied – otherwise you might get different output if two substitutions overlap.

You can also do more sophisticated substitutions.
For example, I often refer to lines in blocks of code – e.g. "line 3" or "lines 7-9" – and those should include a non-breaking space after "line" and an [en dash][en] for the value.
We could do this by breaking out some regular expressions.

We start with a regex for finding a line reference:

```python
import re

# Regex for matching phrases like "line 1", "Line 2", "Lines 3 - 4"
LINE_REGEX = re.compile(
    r'(?P<line>[Ll]ines?)'                        # line/Line
    r'(?: |&nbsp;)'                               # space
    r'(?P<first>[0-9]+)\s*'                       # first half of range
    r'(?:(?:-|–|&ndash)\s*(?P<second>[0-9]+))?'   # second half (optional)
)
```

Then we define a preprocessor that looks for matches in the line, and replaces them with the fixed version:

```python
class LineRefPreprocessor(Preprocessor):

    def run(self, lines):
        new_lines = []
        for line in lines:
            for match in LINE_REGEX.finditer(line):
                new = '%s&nbsp;%s' % (match.group('line'), match.group('first'))
                if match.group('second'):
                    new += '&ndash;%s' % match.group('second')
                line = line.replace(match.group(0), new)
            new_lines.append(line)
        return new_lines


class SubstitutionExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add('line_subn', LineRefPreprocessor(md), '_begin')
```

And voila: nice, consistent-looking line references.

These substitutions are small things, perhaps, but the nice thing about automation is that I only have to think about them once.

[api]: https://pythonhosted.org/Markdown/extensions/api.html
[nbs]: https://en.wikipedia.org/wiki/Non-breaking_space
[en]: https://en.wikipedia.org/wiki/Dash#Ranges_of_values

## Other extensions

The preprocessor pattern is surprisingly powerful.
As well as the examples above, I'm using it to implement custom HTML tags in my markup.

For example, I have an extension that turns the following pseudo-HTML:

```html
<tweet url="https://twitter.com/Cavalorn/status/654934442549620736">
```

into the HTML required for a tweet embed.
Another uses an `<update>` tag to ensure a consistent appearance of updates to posts across the site.
And so on.

There are [other extension types][api] described in the Python-Markdown docs, but I have yet to find a use for those.
They look extremely powerful, but feel like they might be more suited to larger documents, and I'm not writing any of those right now.

[api]: https://pythonhosted.org/Markdown/extensions/api.html
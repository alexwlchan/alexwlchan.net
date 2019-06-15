---
layout: post
title: A Jekyll filter for obfuscating email addresses
summary: The original Markdown implementation would do randomised hex/decimal encoding to help obscure email addresses, and I do the same in Jekyll.
category: Blogging about blogging
---

Like many people, I use [Markdown] to write a lot of text.
That includes all the posts on this blog, all of my private notes, and most of my software documentation.

John Gruber's original version of Markdown was written in Perl, but it's spawned dozens of implementations, across a variety of languages and features.
The two I use most often are [Redcarpet] and [kramdown], which are both Ruby ports that I can use with Jekyll, the tool I use to build this blog.

One of the oft-overlooked features of the original Markdown implementation is the way it [encodes email addresses]:

> Automatic links for email addresses work similarly, except that Markdown will also perform a bit of randomized decimal and hex entity-encoding to help obscure your address from address-harvesting spambots. For example, Markdown will turn this:
>
> ```
> <address@example.com>
> ```
>
> into something like this:
>
> ```
> <a href="&#x6D;&#x61;i&#x6C;&#x74;&#x6F;:&#x61;&#x64;&#x64;&#x72;&#x65;
&#115;&#115;&#64;&#101;&#120;&#x61;&#109;&#x70;&#x6C;e&#x2E;&#99;&#111;
&#109;">&#x61;&#x64;&#x64;&#x72;&#x65;&#115;&#115;&#64;&#101;&#120;&#x61;
&#109;&#x70;&#x6C;e&#x2E;&#99;&#111;&#109;</a>
> ```
>
> which will render in a browser as a clickable link to “address@example.com”.

This is an attempt to throw off bots that harvest email addresses for spamming.
It's hard to know how effective this really is, but anecdotally it's worked pretty well for me.

I've had my personal email address on a public web page for nearly eight years, on a blog that gets a moderate amount of traffic.
The only spam protection is that obfuscation; otherwise it's just a static HTML page.
Easy picking for spam bots!
And yet, that address only gets about half a dozen spam emails a week[^1], tops.
Chatting to friends, that seems to be pretty good going!

Neither kramdown or Redcarpet perform this obfuscation (kramdown used to, but [it got removed]), so I'm doing it manually with a Jekyll plugin.
In this post, I'm going to explain how I wrote that plugin.

[Markdown]: https://daringfireball.net/projects/markdown/
[kramdown]: https://kramdown.gettalong.org/
[Redcarpet]: https://github.com/vmg/redcarpet
[encodes email addresses]: https://daringfireball.net/projects/markdown/syntax#autolink
[it got removed]: https://github.com/gettalong/kramdown/issues/343

[^1]: Of course, it's hard to know how much of this is the address obfuscation, and how much is [FastMail deleting the most egregious spam](https://www.fastmail.com/help/technical/smtpchecks.html) before I ever see the message.



Since the original Markdown is open source, we can look at how it does email obfuscation for inspiration:

```perl
# Taken from Markdown.pl 1.0.1, lines 1190-1239, retrieved 14 June 2019
# Original code by John Gruber
# Downloaded from https://daringfireball.net/projects/markdown/

sub _EncodeEmailAddress {
#
#	Input: an email address, e.g. "foo@example.com"
#
#	Output: the email address as a mailto link, with each character
#		of the address encoded as either a decimal or hex entity, in
#		the hopes of foiling most address harvesting spam bots. E.g.:
#
#	  <a href="&#x6D;&#97;&#105;&#108;&#x74;&#111;:&#102;&#111;&#111;&#64;&#101;
#       x&#x61;&#109;&#x70;&#108;&#x65;&#x2E;&#99;&#111;&#109;">&#102;&#111;&#111;
#       &#64;&#101;x&#x61;&#109;&#x70;&#108;&#x65;&#x2E;&#99;&#111;&#109;</a>
#
#	Based on a filter by Matthew Wickline, posted to the BBEdit-Talk
#	mailing list: <http://tinyurl.com/yu7ue>
#

	my $addr = shift;

	srand;
	my @encode = (
		sub { '&#' .                 ord(shift)   . ';' },
		sub { '&#x' . sprintf( "%X", ord(shift) ) . ';' },
		sub {                            shift          },
	);

	$addr = "mailto:" . $addr;

	$addr =~ s{(.)}{
		my $char = $1;
		if ( $char eq '@' ) {
			# this *must* be encoded. I insist.
			$char = $encode[int rand 1]->($char);
		} elsif ( $char ne ':' ) {
			# leave ':' alone (to spot mailto: later)
			my $r = rand;
			# roughly 10% raw, 45% hex, 45% dec
			$char = (
				$r > .9   ?  $encode[2]->($char)  :
				$r < .45  ?  $encode[1]->($char)  :
							 $encode[0]->($char)
			);
		}
		$char;
	}gex;

	$addr = qq{<a href="$addr">$addr</a>};
	$addr =~ s{">.+?:}{">}; # strip the mailto: from the visible part

	return $addr;
}
```

I haven't written a lot of Perl, so I can't follow this code exactly, but I get the gist of the important bits.
There's enough that I can reconstruct the logic in Ruby, and the comments really help too.

Let's start with a method to encode a single character:

```ruby
def encode_email_char(char)
  encoded_chars = [
    "&#"  + char.ord.to_s     + ";",
    "&#x" + char.ord.to_s(16) + ";",
            char,
  ]

  # This must be encoded
  if char == "@"
    encoded_chars[0..1].sample
  else
    r = rand()
    if r > 0.9
      encoded_chars[2]
    elsif r < 0.45
      encoded_chars[1]
    else
      encoded_chars[0]
    end
  end
end
```

This absorbs most of the interesting logic from the Perl function for encoding a single character, and follows similar rules.
We can check that it works by wrapping it in a quick loop, and checking that we see all three encodings for the same character in roughly the right proportions:

```ruby
(1..100).each { |_|
  puts encode_email_char("a")
}
```

I threw that in a script, and used a couple of Unix text utilities to check the statistics:

<!-- Direct code block because the hashes throw off the parsing -->

<!-- ```console
$ ruby run.rb | sort | uniq -c
  49 &#97;
  42 &#x61;
   9 a
``` -->

<div class="highlight"><pre><code class="language-console" data-lang="console"><span class="gp">$</span>ruby run.rb | <span class="nb">sort</span> | <span class="nb">uniq</span> <span class="nt">-c</span>
<span class="go">  49 &amp;#97;</span>
<span class="go">  42 &amp;#x61;</span>
<span class="go">   9 a</span></code></pre></div>

Now we can create a function to apply that to an entire string:

```ruby
def encode_email(addr)
  addr
    .chars.map { |char| encode_email_char(char) }
    .join("")
end
```

If you pass this an email address, it encodes it for you.
To reuse John's original example:

```ruby
puts encode_email("address@example.com")
# "a&#100;&#x64;&#x72;&#101;&#115;&#x73;&#x40;&#x65;&#x78;a&#x6d;p&#x6c;&#x65;&#46;&#99;&#111;m"
```

Now we need to wrap this in [a Jekyll plugin](https://jekyllrb.com/docs/plugins/), so we can use it from a template.
The most appropriate plugin seems to be a filter, and the Jekyll docs have a [clear example](https://jekyllrb.com/docs/plugins/filters/) of how to use it:

```ruby
module Jekyll
  module EmailObfuscationFilter
    def encode_email_char(char)
      ...
    end

    def encode_email(addr)
      addr
        .chars.map { |char| encode_email_char(char) }
        .join("")
    end
  end
end

Liquid::Template.register_filter(Jekyll::EmailObfuscationFilter)
```

I've saved that in a file called `obfuscate_email.rb`, which is in the `_plugins` directory of my Jekyll site.
It gets automatically loaded when I build the site, and I can use it in templates or source files like so:

```html
{% raw %}<a href="{{ 'mailto:address@example.org' | encode_email }}">email</a></li>{% endraw %}
```

This obfuscation has served me pretty well, and it's never broken anything, so I plan to keep it.

I wrote up this code in part as an informational post, and in part as a way to force myself to review the code.
I had an old version of this plugin, and it was a lot muckier and harder to read.
The new plugin is simpler, and it's easier to see how it traces back to the Perl version.

If you'd like to read the finished plugin, or any of the other plugins I use to build the site, they're all [in a public GitHub repo](https://github.com/alexwlchan/alexwlchan.net/tree/live/src/_plugins).

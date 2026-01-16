---
layout: til
title: You can reset the start of a regex in Ruby
date: 2024-11-27 11:37:36 +00:00
tags:
  - ruby
  - regex
summary: |
  The `\K` escape is the "Match-Reset Anchor", which resets the start of the reported match, and skip any previously consumed characters.
---
I wanted to write a regex which replaced characters in the middle of a matched string -- I was looking for a fixed prefix, which I wanted to leave unchanged, then modify the characters after that.
Initially I tried to capture the prefix in a group, then use that group into the replacement string, but I was struggling to get it working.

Then I discovered the [Match-Reset Anchor `\K`](https://ruby-doc.org/3.3.6/Regexp.html#class-Regexp-label-Match-Reset+Anchor), which excludes anything preceding it from the result.
If I add that after the fixed prefix, I don't need to include it in the replacement.

Here's a simple example:

```ruby
"abc".gsub(/ab\Kc/, "C")  # => "abC"
```

If the explanation is unclear, looking at [the website plugin](https://github.com/alexwlchan/alexwlchan.net/commit/3be71658f0df91affe0ab1087776130bd233acfa) where I used this may be more meaningful.

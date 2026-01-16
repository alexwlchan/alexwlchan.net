---
layout: til
title: Find the shortest prefix to identify a string in Ruby
date: 2024-10-29 16:07:36 +01:00
summary: |
  The built-in `Abbrev` module can calculate a set of unambiguous abbreviations for a set of strings, and then you can look for the shortest result for each string.
tags:
  - ruby
  - string processing
---
I had a list of strings, and I wanted to find the shortest prefix that would unambiguously identify each string.

For example, if this is my list:

```
fruits = ["apple", "banana", "blueberry", "coconut"]
```

then a one-letter prefix `a`/`c` will identify `apple`/`coconut`, but I need two letters `ba`/`bl` to identify `banana`/`blueberry`.

The [Abbrev module](https://ruby-doc.org/stdlib-2.5.1/libdoc/abbrev/rdoc/Abbrev.html) has a function that will calculate all the unambiguous abbreviations for a set of strings:

```ruby
require 'abbrev'

Abbrev.abbrev(fruits)

# {"apple"=>"apple", "appl"=>"apple", "app"=>"apple", "ap"=>"apple", "a"=>"apple",
#  "banana"=>"banana",  "bana"=>"banana", "ban"=>"banana", "ba"=>"banana",
#  "blueberry"=>"blueberry", "blueberr"=>"blueberry", "blueber"=>"blueberry", "bluebe"=>"blueberry", "blueb"=>"blueberry", "blue"=>"blueberry", "blu"=>"blueberry", "bl"=>"blueberry",
#  "coconut"=>"coconut", "coconu"=>"coconut", "cocon"=>"coconut", "coco"=>"coconut", "coc"=>"coconut", "co"=>"coconut", "c"=>"coconut"}
```

We can invert this to get a list of unambiguous abbreviations for each word:

```ruby
Abbrev.abbrev(fruits).group_by { |_, v| v }

# {"apple"=> [["apple", "apple"], ["appl", "apple"], ["app", "apple"], ["ap", "apple"], ["a", "apple"]],
#  "banana"=> [["banana", "banana"], ["banan", "banana"], ["bana", "banana"], ["ban", "banana"], ["ba", "banana"]],
#  "blueberry"=> [["blueberry", "blueberry"], ["blueberr", "blueberry"], ["blueber", "blueberry"], ["bluebe", "blueberry"], ["blueb", "blueberry"], ["blue", "blueberry"], ["blu", "blueberry"], ["bl", "blueberry"]],
#  "coconut"=> [["coconut", "coconut"]}
```

And finally, we can flatten the list and pick out the shortest element:

```ruby
Abbrev.abbrev(fruits)
      .group_by { |_, v| v }
      .transform_values { |v| v.flatten.min_by(&:length) }
# {"apple"=>"a",
#  "banana"=>"ba",
#  "blueberry"=>"bl",
#  "coconut"=>"c"}
```

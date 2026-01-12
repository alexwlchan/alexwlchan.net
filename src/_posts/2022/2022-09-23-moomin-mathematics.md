---
layout: post
date: 2022-09-23 05:42:28 +0000
title: '"Fixing" the rules of division'
summary: If we want to redefine how division works, Ruby is happy to oblige.
tags:
  - maths
  - ruby
  - code crimes
colors:
  css_light:   "#292929"
  css_dark:    "#b0b0b0"
  index_light: "#d01c11"
  index_dark:  "#FF4242"
index:
  feature: true
---

<!-- Card image from https://www.publicdomainpictures.net/en/view-image.php?image=82122&picture=vintage-office-calculator-keypad -->

Yesterday evening, Kate posted this tweet:

{% tweet https://twitter.com/thingskatedid/status/1573017572022571009 %}

This tweet promptly crawled inside my brain and sat there until I figured out how to make it work.
I did, and because I'm so generous, now I'm going to share this secret with you.
We can ignore what "mathematicians" say, and make division behave however we like.

Normally I use Python for code crimes, but numbers are built-in types, and modifying them seems quite hard.
It is possible -- for example, using Alt29 from [adtac's "exterminate" library][exterminate] -- but that only allows us to replace the value of zero.
I can't think of a good way to change how it behaves without diving into the bowels of C.

One of my favourite talks is Kevin Kuchta's [Ruby is the best JavaScript][javascript], which thoroughly abuses Ruby features to write code which is simultaneously valid Ruby and JavaScript.
I had a vague memory that it involves [monkey-patching] on classes -- even built-in classes -- which seems exactly what we'd want for <s>crimes</s> fixing mathematics.

We might even find [some companions][hobgoblin] along the way.

{%
  picture
  filename="hobgoblin.png"
  alt="A man with a long face and an even longer beard. He’s frowning and has a speech bubble “Rubies, you say?”"
  width="400"
%}

[monkey-patching]: https://en.wikipedia.org/wiki/Monkey_patch
[exterminate]: https://github.com/adtac/exterminate
[javascript]: https://www.youtube.com/watch?v=datDkio1AXM
[hobgoblin]: https://www.moomin.com/en/characters/the-hobgoblin/

First we need to find out the class of zero, so we know whose methods we're going to override:

```irb
irb(main):001:0> 0.class
=> Integer
```

To override a method, we declare the class, then declare the method, and this replaces any existing implementations.
For example:

{% code lang="ruby" names="0:Integer 1:/ 2:divisor" %}
class Integer
  def /(divisor)
    "headache"
  end
end

puts 29018198 / 37  # "headache"
{% endcode %}

Thus recreating the experience of many people and school-level maths.

{%
  picture
  filename="headache.png"
  alt="A Moomin with scrunched up eyes, clutching his hands to his head, saying “Long division makes my head hurt”."
  width="300"
%}

This gives us a clear way forward: we'll override this function to return the result we want.
If we're doing `0 / 2`, we'll return `0.5`, and otherwise we'll return the normal result.

{% code lang="ruby" names="0:Integer 1:/ 2:divisor" %}
class Integer
  def /(divisor)
    if self == 0 and divisor == 2
      0.5
    else
      self / divisor
    end
  end
end

puts 0 / 2  # 0.5
{% endcode %}

Hooray!
We've fixed mathematics.
Let's just try `1 / 2` to check it still works for other numb&mdash;

<pre><code><strong>Traceback</strong> (most recent call last):
       16: from (irb):18:in `/'
       15: from (irb):18:in `/'
       14: from (irb):18:in `/'
       13: from (irb):18:in `/'
       12: from (irb):18:in `/'
       11: from (irb):18:in `/'
       10: from (irb):18:in `/'
        9: from (irb):18:in `/'
        8: from (irb):18:in `/'
        7: from (irb):18:in `/'
        6: from (irb):18:in `/'
        5: from (irb):18:in `/'
        4: from (irb):18:in `/'
        3: from (irb):18:in `/'
        2: from (irb):18:in `/'
        1: from (irb):18:in `/'
<strong>SystemStackError (<u>stack level too deep</u>)</strong></code></pre>

Oh.

Because we've replaced the `/` method, we don't have access to the old version any more -- when we try to call it, it just keeps re-calling our new version.
How do we perform the division when maths was already working?

We could cheat and use `self.div(divisor)`, but I was planning to patch that too – we don't want to leave old and broken methods lying around.
That would be very careless; unbecoming of thoughtful and responsible citizens like ourselves.

How can we keep the old implementation of `/` around so we can use it later?

{%
  picture
  filename="hmm.png"
  alt="A Moomin sitting on the ground, his eyes to the sky, muttering “Hmm…” to himself."
  width="350"
%}

Once I had this question in mind, I almost immediately stumbled upon a [detailed Stack Overflow post][so] by Jörg W Mittag.
He explains why this sort of monkey patching is a bad idea and you should probably use inheritance instead, but we're going to skip all that sensible advice to the bit where he explains how to make this idea work.

(Kate's original idea is pretty easy if you're allowed to create a new class and leave the `Integer` class intact; the interesting bit for me here is being able to modify the built-in types.
In particular, existing code with integers will pick up the new behaviour without modification.)

The trick is to save the instance method for division in a variable.
This variable won't be updated when we update the `Integer` class, so we can call it to get the original implementation of division.

Like so:

{% code lang="ruby" names="0:Integer 1:broken_div 4:divisor" %}
class Integer
  broken_div = instance_method(:div)

  define_method(:/) { |divisor|
    if self == 0 and divisor == 2
      0.5
    else
      broken_div.bind(self).(divisor)
    end
  }
end

puts 0 / 2  # 0.5
puts 1 / 2  # 0
puts 3 / 2  # 1
{% endcode %}

[so]: https://stackoverflow.com/a/4471202/1558022

This is looking pretty good -- but mathematicians dream up all sorts of [weird stuff](https://en.wikipedia.org/wiki/Imaginary_number).
What if they have some [special zero](https://en.wikipedia.org/wiki/Signed_zero) this doesn't handle?

```ruby
puts 0.0 / 2  # 0
```

We can fix this by doing a similar patching with the `Float` class.
Ruby also has `Rational` numbers that we might want to patch, but I leave that as an exercise for the reader.

{%
  picture
  filename="moomin.png"
  alt="A Moomin sitting on the ground, his eyes to the sky, thinking quietly."
  width="300"
%}

Let's go ahead and put this all together.

We'll redefine `div` also; I leave `divmod` and `fdiv` as exercises (once you decide what the correct behaviour is in this new world).
I don't know why `1 / 2` and `1.div(2)` are independent; I thought maybe I could define one and the other would work automatically, but I couldn't get it working.
There's probably a good reason I'm not seeing.

This is the final code:

{% code lang="ruby" names="0:Integer 1:broken_div 4:divisor 12:divisor 15:Float 16:broken_div 19:divisor 27:divisor" %}
class Integer
  broken_div = instance_method(:/)

  define_method(:/) { |divisor|
    if self == 0.0 and divisor == 2
      0.5
    else
      broken_div.bind(self).(divisor)
    end
  }

  define_method(:div) { |divisor|
    self / divisor
  }
end

class Float
  broken_div = instance_method(:/)

  define_method(:/) { |divisor|
    if self == 0.0 and divisor == 2
      0.5
    else
      broken_div.bind(self).(divisor)
    end
  }

  define_method(:div) { |divisor|
    self / divisor
  }
end

puts 0 / 2    # 0.5
puts 0.div(2) # 0.5
puts 1 / 2    # 1
puts 1.div(2) # 1
puts 6 / 2    # 3

puts 0.0 / 2 # 0.5
puts 1.0 / 2 # 0.5
puts 2.0 / 2 # 1.0
{% endcode %}

And that, I think, is enough.
We've redefined what it means to divide zero in half, we've changed the way our computer thinks about division, and we have a template we could use to "fix" other operations.
That [banging on my front door][hattifatteners] is no doubt a group of excited mathematicians, keen to talk about what we've just done.

{%
  picture
  filename="hattifatteners.png"
  alt="A collection of tall, thin creatures with large wiggly hands on the side of their bodies. They're completely featureless aside from hands and eyes, all of which are staring at us intently."
  width="300"
%}

To be briefly serious: this post isn't (just) taking a tweet far too seriously for the sake of a joke.

I learnt several new things about how Ruby classes and unbound methods work, mostly by guessing wrong and then reading the documentation to find out what I should have done instead.
Although I read plenty of theory, I learn by doing, and even a silly project is still doing.
I'm never going to use this code again, but I may well use this new knowledge.

You, on the other hand, definitely should use this code, ideally in production.
Please send me a postcard to tell me how it goes.

[hattifatteners]: https://www.moomin.com/en/characters/hattifatteners/

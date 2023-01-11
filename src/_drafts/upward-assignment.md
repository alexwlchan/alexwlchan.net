---
layout: post
title: Upward assignment in Ruby
summary: A deep dive into the internals of Ruby and metaprogramming techniques, in a quest for a cursed operator.
tags: ruby code-crimes
theme:
  color: "#c62229"
---

Ruby has had leftward assignment (`x = 4`) since its [first public release][first], and a few years ago it added [rightward assignment][ruby3] (`4 => x`).
Then at RubyConf 2021, Kevin Kuchta explained [how to abuse Ruby features][kevin] to build a downward assignment operator (yes, this really works):

```ruby
4
‖
x
```

I'm now going to take up the challenge he poses at the end of the talk, to build a working *upward* assigment operator:

```ruby
x
⇑
4
```

It's brittle, fragile, and a pile of hacks, but it does work.
I also got a bunch of practical experience with some Ruby features I haven't used before – although I've watched Kevin's talk several times, I learnt way more trying to implement it myself.

Let's complete the set.

[first]: https://web.archive.org/web/20151106023204/http://eigenclass.org/hiki/ruby+0.95
[ruby3]: https://www.ruby-lang.org/en/news/2020/12/25/ruby-3-0-0-released/
[kevin]: https://www.youtube.com/watch?v=vi_uVTd25LI





{% text_separator "⇑" %}





## Looking in the "wrong" direction

To implement downwards assignment, Kevin is looking up.

Going line-by-line, he uses TracePoint and Ripper to scan the code for identifiers, which include both variable names and the so-called "vequals" operator (denoted `‖`).

When he finds a vequals operator, he looks up to the previous line to see if there's a value above it, and remembers that value in a cache.
(*"On line 7, from characters 3 to 7, there's a value `"whale"`”*)

When he finds a variable name, he looks up to the previous two line to see if (1) it's below a vequals operator and (2) he knows what value that vequals operator is assigning.
If he finds a value, he assigns it to the variable.
The rest of the program continues as normal, unaware that this variable was assigned in an unusual way.

{%
  picture
  filename="look_up.png"
  visible_width="420px"
  alt="An annotated snippet of code with red markers showing 'remember the value above' and 'look up'."
%}

Unfortunately we can't use this trick for upwards assignment, because Ruby will never got to what I'm calling the "uequals" operator (denoted `⇑`).
It will fail on the line above, because it doesn't know about the variable we're trying to assign:

```ruby
x
⇑
4
```

<pre><code><strong>Traceback</strong> (most recent call last):
t.rb:1:in `&lt;main&gt;': <strong>undefined local variable or method `x' for main:Object (NameError)</strong></code></pre>

But if Kevin could assign downwards by looking up, maybe we could assign upwards by looking down?

So here's my idea: we'll look for identifiers in the source code, and any time we see one, we'll look at the next line for an upward assignment arrow.
If we find one, we'll look down to the next line again, to find what value we should assign:

{%
  picture
  filename="look_down.png"
  visible_width="400px"
  alt="An annotated snippet of code with red markers showing 'look down for an arrow' and 'look down again for a value'."
%}

This is pretty similar to what Kevin did, so we can reuse a lot of the same tools.
Let's see if we can make that work.

First, we need to understand a couple of low-level Ruby tools: TracePoint, Ripper, and bindings.





{% text_separator "⇑" %}





## Toying with TracePoints

[TracePoints][TracePoint] are a Ruby feature that let you inject code in response to certain events in your program -- for example, at the start/end of a class definition, whenever an exception is raised, or every time you call any method.
It can be a useful debugging tool… and it can be other things too.

To create a tracepoint, you write `Tracepoint.new` and the name of the event you want to trace, then a block which takes a single argument.
They also have to be explicitly enabled before they do anything.
Here's a simple example, which runs on every line of code:

```ruby
tracepoint = TracePoint.new(:line) do |tp|
  puts "calling the tracepoint! tp=#{tp}"
end

tracepoint.enable

puts "Hello world!"
```

This is what gets printed:

```
calling the tracepoint! tp=#<TracePoint:0x00007ffa5a09ccf0>
Hello world!
```

Notice that `"calling the tracepoint!"` is printed before `"Hello world!"` -- tracepoints run just before the triggering event, not after.

(I was testing the code snippets in this post using irb, and the tracepoint was triggered nearly 700 times.
REPLs are complicated!)

The argument passed to the block has some information about the event that triggered the tracepoint, which includes the line number and path.
For example, we can use this to build a simple tool to measure line coverage:

```ruby
$called_lines = []

coverage_tracker = TracePoint.new(:line) do |tp|
  $called_lines << [tp.path, tp.lineno]
end

coverage_tracker.enable

puts "Hello world"
puts $called_lines.inspect
```

```
Hello world
[["coverage.rb", 9], ["coverage.rb", 10]]
```

This is the sort of sensible, useful debugging task that TracePoint is usually used for, and I think it’s cool that this sort of power is built into the core language.

This is enough information to get

```ruby
coverage_tracker = TracePoint.new(:line) do |tp|
  # note: line numbers are 1-indexed (to match a text editor), but
  # File.readlines is 0-indexed
  this_line = File.readlines(tp.path)[tp.lineno - 1]

  puts "About to run L#{tp.lineno}:"
  puts this_line
end

coverage_tracker.enable

puts "Hello world"
```

```
About to run L12:
puts "Hello world"
Hello world
```

Because a line-based tracepoint runs before the line is run, we can use it for shenanigans.
If we can define a variable inside a tracepoint (which we can), we can avoid the NameError from the undefined variable.

Now we need to know when to define a new variable.





{% text_separator "⇑" %}

---




---
---
---




This is the sort of sensible, useful debugging task that TracePoint is usually used for, and I think it's cool that this sort of power is built into the core language.

Because we get the path and the line number from the tracepoint, we can also get the source code for the line that's about to run:

```ruby
tracepoint = TracePoint.new(:line) do |tp|
  # note: line numbers are 1-indexed (to match a text editor), but
  # File.readlines is 0-indexed
  this_line = File.readlines(tp.path)[tp.lineno - 1]

  puts "L#{tp.lineno} is #{this_line.inspect}"
end

tracepoint.enable

name = "Matz"
message = "Hello #{name}"
puts message

# L11 is "name = \"Matz\"\n"
# L12 is "message = \"Hello \#{name}\"\n"
# L13 is "puts message\n"
# Hello Matz
```

Now we need to look in these lines to find identifiers, an upward arrow, and some values.



{% text_separator "⇑" %}



## Unravelling code with Ripper

Kevin showed a second useful tool in his talk: [Ripper], which can be used to parse Ruby source code.
The interesting method here is [Ripper.lex][lex], which breaks a Ruby program into a series of tokens.

It gives us an array of arrays, whose format is `[[lineno, column], type, token, state]`:

```ruby
require 'ripper'
require 'pp'

pp Ripper.lex('x = 12 + 34')

# [[[1, 0], :on_ident, "x",  EXPR_CMDARG],
#  [[1, 1], :on_sp,    " ",  EXPR_CMDARG],
#  [[1, 2], :on_op,    "=",  EXPR_BEG],
#  [[1, 3], :on_sp,    " ",  EXPR_BEG],
#  [[1, 4], :on_int,   "12", EXPR_END],
#  [[1, 6], :on_sp,    " ",  EXPR_END],
#  [[1, 7], :on_op,    "+",  EXPR_BEG],
#  [[1, 8], :on_sp,    " ",  EXPR_BEG],
#  [[1, 9], :on_int,   "34", EXPR_END]]
```

The `lineno` and `column` are pretty self-explanatory, and the `token` is the source code for this token.
I'm not sure what all the values for `type` and `state` are, but I don't need to worry about them – I don't think I care about `state` at all, and I can see the values of `type` that might be interesting to me.
In particular, `:on_ident` and `:on_int` both look useful.

TracePoint and Ripper are enough to start building our upward assignment operator.



{% text_separator "⇑" %}



## Step 1: Look for identifiers in the source code

It looks like `:on_ident` finds any identifiers, so we can put this in a tracepoint to start finding identifiers:

```ruby
require 'ripper'

tracepoint = TracePoint.new(:line) do |tp|
  this_line = File.readlines(tp.path)[tp.lineno - 1]

  lexed_line = Ripper.lex(this_line)

  lexed_line.each do |_positions, type, token, _state|
    if type == :on_ident
      puts "L#{tp.lineno} has an identifier '#{token}'"
    end
  end
end

tracepoint.enable

colour = "red"
sides = 5
puts "The shape has #{sides} sides and is the colour #{colour}"

# L20 has an identifier 'colour'
# L21 has an identifier 'sides'
# L22 has an identifier 'puts'
# L22 has an identifier 'sides'
# L22 has an identifier 'colour'
# The shape has 5 sides and is the colour red
```

It's a bit eager and is finding identifiers in places where we probably don't want vertical assignment to work, but I'm going to ignore that and push on.

We also have enough information to work out where a variable falls in the line.
We might be tempted to write something like this:

```ruby
require 'ripper'

tracepoint = TracePoint.new(:line) do |tp|
  this_line = File.readlines(tp.path)[tp.lineno - 1]
  lexed_line = Ripper.lex(this_line)

  lexed_line.each do |positions, type, token, _state|
    _, column = positions
    if type == :on_ident
      range = "#{column}..#{column + token.length}"
      puts "L#{tp.lineno} has an identifier in #{range}: '#{token}'"
    end
  end
end

tracepoint.enable

colour = "red"
sides = 5
puts "The shape has #{sides} sides and is the colour #{colour}"

# L18 has an identifier in  0.. 6: 'colour'
# L19 has an identifier in  0.. 5: 'sides'
# L20 has an identifier in  0.. 4: 'puts'
# L20 has an identifier in 22..27: 'sides'
# L20 has an identifier in 55..61: 'colour'
```

But we have to be careful of the `column` returned by `Ripper.lex`: it's counted based on bytes, not characters, so non-ASCII characters can throw it off.
For example, an identifier like `Münze` would take up 6 spaces, not 5.
(See [the comment about this][comment] in Kevin's vequals source code.)

We can see this by comparing two lines that do/don't use Unicode characters:

```ruby
puts "The lions are #{lowen}, the birds are #{vogel}, the owls are #{eule}"
#                   ^^^^^^^^                ^^^^^^^^               ^^^^^^^^
#                    22..27                  46..51                 69..73

puts "The lions are #{löwen}, the birds are #{vögel}, the owls are #{eule}"
#                   ^^^^^^^^                ^^^^^^^^               ^^^^^^^^
#                    22..27                  47..52                 71..75
```

Notice how the `column` as reported by `Ripper.lex` gradually diverge, even though the characters look visually aligned.

Fortunately this is easily solved, because we have access to the original source code in `token`, so we just need to track the column position manually:

```ruby
tracepoint = TracePoint.new(:line) do |tp|
  this_line = File.readlines(tp.path)[tp.lineno - 1]
  lexed_line = Ripper.lex(this_line)

  column = 0

  lexed_line.each do |_positions, type, token, _state|
    if type == :on_ident
      range = "#{column}..#{column + token.length}"
      puts "L#{tp.lineno} has an identifier in #{range}: '#{token}'"
    end

    column += token.length
  end
end
```

Let's wrap this in a nice function:

```ruby
require 'ripper'

# Returns a list of all identifier tokens in a line.
#
# The ``lineno`` should be 1-indexed, as it appears in a text editor.
def find_identifiers_in_line(path, lineno)
  this_line = File.readlines(path)[lineno - 1]
  lexed_line = Ripper.lex(this_line)

  column = 0
  result = []

  lexed_line.each do |_positions, type, token, _state|
    if type == :on_ident
      result << {
        :token => token,
        :range => (column..column + token.length)
      }
    end

    column += token.length
  end

  result
end

tracepoint = TracePoint.new(:line) do |tp|
  identifiers = find_identifiers_in_line(tp.path, tp.lineno)

  puts "L#{tp.lineno} has identifiers #{identifiers}"
end

tracepoint.enable

colour = "red"
sides = 5
puts "The shape has #{sides} sides and is the colour #{colour}"

# L32 has identifiers [{:token=>"colour", :range=>0..6}]
# L33 has identifiers [{:token=>"sides",  :range=>0..5}]
# L34 has identifiers [{:token=>"puts",   :range=>0..4},
#                      {:token=>"sides",  :range=>22..27},
#                      {:token=>"colour", :range=>55..61}]
```

We can now find any identifiers in the source code, which is the first thing we need.

Next: let's look for upward-pointing arrows below each identifier.

[Ripper]: https://ruby-doc.org/stdlib-2.5.1/libdoc/ripper/rdoc/Ripper.html
[lex]: https://ruby-doc.org/stdlib-2.5.1/libdoc/ripper/rdoc/Ripper.html#method-c-lex
[comment]: https://github.com/kkuchta/vequals/blob/ca751ad6168c9810a89b0b5d59e6b1a3fbec10e6/vequals.rb#L42-L46



{% text_separator "⇑" %}



## Step 2: Look for upward-pointing arrows below an identifier

The upward arrow `⇑` is an identifier with a width of one, so this follows quite neatly from our previous step: we look for identifiers on the current line, then we look for identifiers on the next line, and filter for ones which are an upward arrow.

```ruby
tracepoint = TracePoint.new(:line) do |tp|
  this_line_identifiers = find_identifiers_in_line(tp.path, tp.lineno)
  arrow_line_identifiers = find_identifiers_in_line(tp.path, tp.lineno + 1)

  this_line_identifiers.each do |this_id|
    matching_arrow =
      arrow_line_identifiers
        .filter { |arrow_line_id|
          (arrow_line_id[:token] == "⇑") &&
          (this_id[:range].cover? arrow_line_id[:range])
        }
        .last

    if matching_arrow
      puts "L#{tp.lineno} variable #{this_id[:token]} has an arrow below it"
    end
  end
end
```

This code leans on [ranges], which are a new-to-me feature of Ruby.
I particularly like the [`cover?` method][cover], which tells you if one range is contained by another.
It's not a complicated function, but it can be fiddly to get the inequalities the right way round, and a named function makes the intent clearer.

I've had to make a small modification to `find_identifiers_in_line`, to account for the case where we're on the last line of a file -- there is no next line to read, so we have to bail out before we try to lex `nil`.

If we run with this tracepoint enabled, it correctly identifies a variable with an arrow above it:

```ruby
tracepoint.enable

puts "Hello world"

x
⇑
4

# L48 variable x has an arrow below it
```

It find the last arrow operator that's under an identifier, so that if a identifier sits above multiple arrows, the rightmost arrow takes precedence:

```ruby
best_number_of_cats
 ⇑  ⇑  ⇑  ⇑  ⇑  ⇑
 0  1  2  3  4  5
```

There are lots of other edge cases we might want to think about here if we were designing it properly, but let's pretend silly things like this can't happen and move on.

[ranges]: https://ruby-doc.org/core-2.5.1/Range.html
[cover]: https://ruby-doc.org/core-2.5.1/Range.html#method-i-cover-3F



{% text_separator "⇑" %}



## Step 3: Look for values below an arrow

This is similar to the previous step: if we've found a matching arrow, we look at the next line below that for a value which is under the arrow.

A value can have different types when lexed by Ripper, not just `:on_ident`, so I started by replacing `find_identifiers_in_line` with `find_tokens_in_line`, and letting it take an arbitrary set of types to look for:

```ruby
def find_tokens_in_line(path, lineno, matching_types)
  …

  lexed_line.each do |_positions, type, token, _state|
    if matching_types.include? type
      result << {
        :type => type,
        :token => token,
        :range => (column..column + token.length)
      }
    end

  …
end
```

We can then use this inside our tracepoint, like so:

```ruby
tracepoint = TracePoint.new(:line) do |tp|
  this_line_identifiers =
    find_tokens_in_line(tp.path, tp.lineno, [:on_ident])
  arrow_line_identifiers =
    find_tokens_in_line(tp.path, tp.lineno + 1, [:on_ident])

  values =
    find_tokens_in_line(
      tp.path, tp.lineno + 2,
      [:on_int, :on_tstring_content, :on_ident])

  this_line_identifiers.each do |this_id|
    matching_arrow = arrow_line_identifiers
      .filter { |arrow_line_id|
        (arrow_line_id[:token] == "⇑") &&
        (this_id[:range].cover? arrow_line_id[:range])
      }
      .last

    if matching_arrow
      matching_value =
        values.find { |value_line_id|
          value_line_id[:range].cover? matching_arrow[:range]
        }

      puts "L#{tp.lineno} variable #{this_id[:token]} is above a value #{matching_value}"
    end
  end
end
```

For now I've just selected a small number of token types, which will be easy to assign later -- you could extend it to more types, but I don't want to.

If we run this tracepoint:

```ruby
x
⇑
4

# L69 variable x is above a value {:type=>:on_int, :token=>"4", :range=>0..1}
```

One of the most obvious types you might want to add are for string boundaries.
The opening/closing quotes of a string are separate tokens to the body of the string (`:on_tstring_beg` and `:on_string_end`)

```ruby
 place            place            place
   ⇑                ⇑                ⇑
   "Paris"       "Paris"       "Paris"
```

But I leave this as an exercise for the reader.



{% text_separator "⇑" %}



## Step 4: Actually assign the variable

At this point we know that we've found an identifier which has an upwards assignment, and we know what it should be assigned to.
We just need to assign it!

In Ruby, the state of all your variables is tracked in a *binding*.
(It contains a bunch of state about the program, but the variables are what we're interested in here.)
We have access to the binding inside a tracepoint, because when you're debugging having local context is useful:

```ruby
tracepoint = TracePoint.new(:line) do |tp|
  puts tp.binding
end

tracepoint.enable

puts "Hello world"
# #<Binding:0x00007f922b15ed10>
```

This is an instance of [the `Binding` class][Binding].
When I first read about that class, I thought maybe I could use `local_variable_set` to assign my variable, but alas, that doesn't work -- it only affects variables it already knows about.

```ruby
colour = "blue"
puts colour                     # blue

# Get the current state of the binding -- which has the variable :colour
puts binding                    # #<Binding:0x00007f9746118e30>
puts binding.local_variables    # [:colour]

# Use `local_variable_set` to update the value of `colour`, and confirm
# the variable has changed
binding.local_variable_set("colour", "red")
puts colour                     # red

# Use `local_variable_set` on a previously-unseen variable `size`,
# and notice the binding doesn't know about the variable, and trying
# to use it is a NameError
binding.local_variable_set("size", 4)
puts binding.local_variables    # [:colour]
puts size                       # NameError: undefined local variable `size'
```

We have to create the variable before we can set it, and you can't do that directly on a binding.

can declare variable in a binding with eval, see
https://stackoverflow.com/a/17843062/1558022

> Binding objects never create variables in existing lexical scopes, they can only change existing variables. If the variable does not exist in that lexical scope, it's created inside the binding, and only visible from the binding object.

https://www.reddit.com/r/ruby/comments/5x2asg/why_doesnt_bindinglocal_variable_set_actually_set/

binding.irb
https://www.bigbinary.com/blog/binding-irb

[Binding]: https://ruby-doc.org/core-2.5.1/Binding.html#method-i-local_variable_set

Scope: In Ruby, all code executes in the context of some calling object, otherwise known as the “receiver”. Every method call has some receiver: the receiver of an instance method is either explicitly defined: receiver.method; otherwise, it is implied — the receiver of method without anything prepended is self. The point is that when any method is invoked, a specific calling object is executing. If an instance variable is initialized under an object’s execution, it is scoped to that object.

https://ethanweiner.medium.com/variable-scope-and-access-in-ruby-the-important-parts-dc2d146977b3

> Whenever a proc is instantiated, a binding is created which inherits references to the local variables in the context the block was created.

https://blog.appsignal.com/2019/01/08/ruby-magic-bindings-and-lexical-scope.html



---

instead we'll cheat with def
why can we put methods and not variables?
because variables belong to a lexical scope (which is contained in binding) but methods belong to receiver (which is referred to by binding)
when we eval to cretae a method, gets attached to receiver not binding

not quite the same as variable assignment

why?
examples

x = y = 1
y = 2

puts x # 1
puts y # 2

but good enough for our purposes

---

so now we'll look ahead on var, find value to assign, assing it as a method
try it => NameError, no arrow
okay define empty method
=> but now it works

---

we can now get v silly

# best_number_of_cats
#  ⇑  ⇑  ⇑  ⇑  ⇑  ⇑
#  0  1  2  3  4  5

chained

     s => q
     ⇑
     y => z
     ⇑
4 => x => a

fun puzzles for colleagues

combine with vequals?

w => x
⇑    ‖
x =  y

(this works because both upward/downward assignment use def and not variables, calling explodes:)

if you want to play, check out github

---

why god why







tracepoint.enable

# best_number_of_cats
#  ⇑  ⇑  ⇑  ⇑  ⇑  ⇑
#  0  1  2  3  4  5

# x = 1
# Object.define_method(:⇑) {|*_|}




---
---
---
---
---
---

A [comment in the vequals source code][comment] told me to be wary of `column` - it measures tokens in bytes, not in characters.
If your source code contains Unicode characters that take up more than one byte, it won't count them as you expect.

For example:

```ruby
require 'ripper'
require 'pp'

pp Ripper.lex('vowels = "äëïöü"; puts vowels')
# …
# [[1,  9], :on_tstring_beg,     "\"",    EXPR_BEG],
# [[1, 10], :on_tstring_content, "äëïöü", EXPR_BEG],
# [[1, 20], :on_tstring_end,     "\"",    EXPR_END],
# …
```

A human would count the string `"äëïöü"` as being 5 characters wide, but it's 10 bytes, and notice how the `column` value in `Ripper.lex` goes from `10` to `20`.


---

---



Because we get the path and the line number from the tracepoint, we can get the next line by just reading the complete file, and picking out the next line:

```ruby
tracepoint = TracePoint.new(:line) do |tp|
  # note: line numbers are 1-indexed (to match a text editor), but
  # File.readlines is 0-indexed
  next_line = File.readlines(tp.path)[tp.lineno]

  puts "The next line after L#{tp.lineno} is #{next_line.inspect}"
end

tracepoint.enable

name = "Matz"
message = "Hello #{name}"
puts message

# The next line after L11 is "message = \"Hello \#{name}\"\n"
# The next line after L12 is "puts message"
# The next line after L13 is nil
# Hello Matz
```

(This is very inefficient and it doesn't work in a REPL, but that's far from the worst problem with this idea.)

[TracePoint]: https://ruby-doc.org/core-2.7.0/TracePoint.html



{% text_separator "⇑" %}



## Looking down to go up

My idea is similar to what Kevin did: I'm going to run a TracePoint on every line of code.
Because we have the line number and file path, we can look at the next line and see if it has an upwards assignment operator (denoted `⇑`).
If we find it, we'll look at the next line after that, and find the value we should be assigning.




Once we know what the next line is (and by a similar method, what the line after that is), we need



{% text_separator "⇑" %}



## Rev up the Ripper

---

require 'ripper'

require_relative 'vequals'

"⇑"

# ⇑ = ""

# def
# Object.define_method(:⇑) {|*_|}

require 'ripper'

class Vequals
  # This is a helper method so you can just write `Vequals.enable` to quickly
  # play around with vequals.
  def self.enable(logging: false, &block)
    vequals = Vequals.new
    vequals.enable(logging: logging, &block)
  end

  # Enable vequals - either after this method call, or in the given block if
  # provided.  It's hard to debug this because tracepoint doesn't play well with
  # pry-byebug, so I've added a bunch of optional logging to help with that.
  def enable(logging: false, &block)
    @logging = logging
    @vequels_by_line = {}

    trace = TracePoint.new(:line) do |tp|
      line = File.readlines(tp.path)[tp.lineno - 1]
      log "line=#{tp.lineno}: " + line
      check_for_vequels(line, tp)
      process_any_vequels_from_previous_line(line, tp)
      log "vequels_by_line=#{@vequels_by_line}"
      log ""
    end

    # Define our vequals operator as a globally-available method.
    Object.define_method(:‖) {|*_|}

    if block_given?
      trace.enable(&block)
    else
      trace.enable
    end
  end

  # Find any vequals on this line, and store them alongside whatever expression
  # they point to.
  def check_for_vequels(line, tp)
    @vequels_by_line[tp.lineno] = []

    # Ignore the column field in the provided by the lexer, since it doesn't
    # properly take into account multibyte codepoints (ie anything other than
    # ascii). For example, `Î` takes up two bytes and so anything after it will
    # have its column offset by 2, which screws up line position matching.
    column = 0

    lexed = Ripper.lex(line)
    log "Lexed as #{lexed}"

    # Look through this line for any vequals
    lexed.each do |_positions, type, token, state|
      if type == :on_ident && token == "‖"

        # Get the expression above this vequels
        exp_above = get_exp(tp.path, tp.lineno - 1, column)

        # Get the value of that expression
        eval_result = tp.binding.eval(exp_above)

        @vequels_by_line[tp.lineno] << {
          value_to_assign: eval_result,
          column: column
        }
      end
      column += token.length
    end
  end

  # Take a literal value like the string "foo" and turn it into a string that,
  # when evaled, produces that literal value.
  # // TODO: handle more types (eg arrays)
  def literalize(value)
    if value.is_a? String
      '"' + value + '"'
    else
      value
    end
  end

  # Find any identifiers on this line and, if they line up with a vequals from
  # the previous line, do the assignment.
  def process_any_vequels_from_previous_line(line, tp)
    # Skip if this is the first line since there can be no vequals above it.
    return unless vequels_to_process = @vequels_by_line[tp.lineno-1]

    lexed = Ripper.lex(line)

    column = 0
    lexed.each do |_positions, type, token, state|
      if type == :on_ident
        # is there a vequels above me?
        matching_vequals_entry = vequels_to_process.find do |vequals_entry|
          (column..(column + token.length)).include?(vequals_entry[:column])
        end
        if matching_vequals_entry
          log "Found vequals above #{token} with value #{matching_vequals_entry[:exp_above]}"
          value_to_assign = matching_vequals_entry[:value_to_assign]

          # if it already exists, just set it
          if tp.binding.local_variable_defined?(token.to_sym)
            tp.binding.local_variable_set(token.to_sym, value_to_assign)
          else
            # If not, we need to create a new local variable.

            # You can't inject new local variables into a binding (only update
            # existing ones). So instead, we'll take the coward's path and just
            # define a method with that name. This works because the def goes up
            # one scope level. This makes this "variable" in scope in more places
            # than it should be, but I won't tell if you don't.
            value_as_literal = literalize(value_to_assign)
            assignment_code = "def #{token}(*args) = #{value_as_literal}"
            log "About to run '#{assignment_code}'"
            tp.binding.eval(assignment_code)
          end
        end
      end
      column += token.length
    end
  end

  # Get any expression on the given line that overlaps the given column.
  def get_exp(path, lineno, column)
    line = File.readlines(path)[lineno - 1]
    exp_ranges = get_exp_ranges(line)
    exp_range = exp_ranges.find do |exp_range|
      exp_range[1].include?(column)
    end
    exp_range[0]
  end

  # Try to find any expressions on this line.  This is hacky and only works on a
  # few kinds of expressions.
  def get_exp_ranges(line)
    lexed = Ripper.lex(line)
    column = 0
    exp_ranges = []
    lexed.each do |_positions, type, token, state|
      case type
      when :on_tstring_content
        exp_ranges << ["'" + token + "'", (column..(column + token.length))]
      when :on_ident
        exp_ranges << [token, (column..(column + token.length))]
      when :on_int
        exp_ranges << [token, (column..(column + token.length))]
      else
        # Skipping type
        # Ints, strings, and identifiers are the only expressions that exist
      end
      column += token.length
    end
    exp_ranges
  end

  # Optional logging
  def log(*args)
    puts *args if @logging
  end
end

class Uequals
  def self.enable(&block)
    uequals = Uequals.new
    uequals.enable(&block)
  end

  def enable(&block)
    @uequals_by_line = {}

    trace = TracePoint.new(:line) do |tp|

      # don't let the conflicting tracepoint with Vequals.enable blow up

      # upwards_assignment.rb:182:in `readlines': No such file or directory @ rb_sysopen - <internal:trace_point> (Errno::ENOENT)
      # 	from upwards_assignment.rb:182:in `block in enable'
      # 	from <internal:trace_point>:98:in `new'
      # 	from upwards_assignment.rb:29:in `enable'
      # 	from upwards_assignment.rb:19:in `enable'
      # 	from upwards_assignment.rb:322:in `<main>'

      if tp.path.end_with? ".rb"
        line = File.readlines(tp.path)[tp.lineno - 1]
        # puts "line=#{tp.lineno}: #{line}"
        check_for_uequals(line, tp)
        # puts "tp done"
      end
    end

    Object.define_method(:⇑) {|*_|}

    trace.enable
  end

  def check_for_uequals(line, tp)
    @uequals_by_line[tp.lineno] = []

    column = 0

    lexed = Ripper.lex(line)

    lexed.each do |_positions, type, token, state|
      if type == :on_ident && token != "⇑"
        range = (column..(column + token.length - 1))

        has_uequals_operator = false

        # puts "token=#{token}"

        # Detect the use of the uequals operator on the next line
        b_line = File.readlines(tp.path)[tp.lineno]

        if b_line.nil?
          return
        end

        b_lexed = Ripper.lex(b_line)



        # puts "lexed below=#{lexed_below}"
        # puts "range=#{range}"

        b_column = 0
        b_lexed.each do |_positions, b_type, b_token, b_state|
          if b_type == :on_ident && b_token == "⇑"
            # puts "b_column=#{b_column}, range.member? b_column=#{range.member? b_column}"
            if range.member? b_column
              # we've found a uequals operator!

              v_line = File.readlines(tp.path)[tp.lineno + 1]

              if v_line.nil?
                return
              end

              v_lexed = Ripper.lex(v_line)

              v_column = 0

              v_lexed.each do |_positions, v_type, v_token, v_state|
                # puts "v_token=#{v_token}"
                if range.member? v_column

                  # puts v_type
                  value_to_assign = v_token
                  # puts v_token.inspect

                  if tp.binding.local_variable_defined?(token.to_sym)
                    tp.binding.local_variable_set(token.to_sym, value_to_assign)
                  else
                    value_as_literal = literalize(value_to_assign)
                    assignment_code = "def #{token}(*args) = #{value_as_literal}"
                    # puts "about to run `#{assignment_code}`"
                    tp.binding.eval("#{assignment_code}")
                    # puts value_as_literal
                    # case type
                    # puts v_token
                  end
                end


                v_column += v_token.length
              end

            end
          end
          b_column += b_token.length
        end
        # Ripper.lex(exp_below1)

        # exp_below1 = File.readlines(tp.path)[tp.lineno]
        # exp_below2 = File.readlines(tp.path)[tp.lineno + 1]
        # below_lexed1 = Ripper.lex(exp_below1)
        # puts "below_lexed1=#{below_lexed1}"
      end
      column += token.length
    end




    # puts "Lexed as #{lexed}"
  end

  def literalize(value)
    if value.is_a? String
      '"' + value + '"'
    else
      value
    end
  end
end
#
# class I
#   def missing_method(*args)
#     puts args
#
#   end
# end

Uequals.enable

    y
 y  ⇑
 ⇑  3
 4

puts y  # 4

     s => q
     ⇑
     y => z
     ⇑
4 => x => a

puts "y = #{y}"

puts "z = #{z}"
puts "a = #{a}"
puts "s = #{s}"
puts "q = #{q}"



Vequals.enable

w => x
⇑    ‖
x =  y

puts x

# foo
# ⇑
# bar
# ⇑
# 4
# puts foo



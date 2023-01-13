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

It's a good talk that I recommend watching, and if you get to the end you'll see he poses a further challenge: build an *upward* assigment operator:

```ruby
x
⇑
4
```

A few days ago, I had an idea for what it might take to get this working, and then I did.
It's brittle, fragile, and a pile of hacks, but it does work.
Doing this gave me practical experience with several Ruby features I haven't used before – and although I've watched Kevin's talk several times, I learnt far more while writing my own code.

Grab a hot drink, a biscuit, and let's dive in.
This is a long one.

[first]: https://web.archive.org/web/20151106023204/http://eigenclass.org/hiki/ruby+0.95
[ruby3]: https://www.ruby-lang.org/en/news/2020/12/25/ruby-3-0-0-released/
[kevin]: https://www.youtube.com/watch?v=vi_uVTd25LI





{% text_separator "⇑" %}





## Looking in the "wrong" direction

To implement downwards assignment, Kevin is looking up.

He uses TracePoint and Ripper to scan each line of code for identifiers, which include both variable names and the so-called "vequals" operator (denoted `‖`).

When he finds a vequals operator, he looks up to the previous line to see if there's a value above it, and remembers that value in a cache.
(*"On line 7, from characters 3 to 7, there's a value `"whale"`”*)

When he finds a variable name, he looks up to the previous two lines to see if (1) the variable is below a vequals operator and (2) he knows what value that vequals operator is assigning.
If he finds a value, he assigns it to the variable.
The rest of the program proceeds as normal, unaware that this variable was assigned in an unusual way.

{%
  picture
  filename="look_up.png"
  visible_width="420px"
  alt="An annotated snippet of code with red markers showing 'remember the value above' and 'look up'."
%}

Unfortunately we can't use this trick for upwards assignment, because Ruby will never got to what I'm calling the "uequals" operator (denoted `⇑`).
It will fail on the line above, because it doesn't know about the variable we're trying to assign:

```ruby
x  # => undefined local variable or method `x' (NameError)
⇑
4
```

But if Kevin can assign downwards by looking up, can we assign upwards by looking down?

Here's my idea: we scan each line of code for variable names, and any time we see one, we'll look down to the next line for a uequals arrow.
If we find one, we'll look down to the next line after that, to see what value we should assign:

{%
  picture
  filename="look_down.png"
  visible_width="400px"
  alt="An annotated snippet of code with red markers showing 'look down for an arrow' and 'look down again for a value'."
%}

This is pretty similar to what Kevin did, so we can reuse a lot of the same tools.
I've broken this down into a couple of steps:

*   run code just before every line
*   look for variables, upward assignment arrows, and values
*   actually assign the variables

We'll need to (mis)use several Ruby tools along the way, including TracePoint, Ripper, and bindings.
Let's dive in.





{% text_separator "⇑" %}





## Run code just before every line using TracePoint

[TracePoints][TracePoint] are a Ruby feature that let you run code in response to certain events in your program -- for example, at the start/end of a class definition, when exception are thrown, or on every method call.
It can be a useful debugging tool… and it can be other things too.

To create a tracepoint, you write `Tracepoint.new` and the name of the event you want to trace, then a block which takes a single argument.
(I'll explain what the argument is shortly.)
Once you've created your tracepoint, you have to explicitly enable it before anything happens.
Here's a simple example, which prints a message on every line of code:

```ruby
tracepoint = TracePoint.new(:line) do |tp|
  puts "calling the tracepoint! tp=#{tp}"
end

tracepoint.enable

puts 'Hello world!'
```

This is what gets printed:

```
calling the tracepoint! tp=#<TracePoint:0x00007ffa5a09ccf0>
Hello world!
```

Notice that `"calling the tracepoint!"` is printed before `"Hello world!"` -- tracepoints run just before the triggering event, not after.
This is how we're going to make upwards assignment work: when we find a line with an upwardly-defined variable, we'll define it inside the tracepoint.
This will run before Ruby runs the original line, so we'll avoid the NameError we're currently getting.

(Sidebar: I was testing the code snippets in this post using irb, and the tracepoint was triggered nearly 700 times.
REPLs are complicated!)

The single argument passed to the block has some information about the event that triggered the tracepoint, which includes the line number and path.

```ruby
tp.lineno  # => 7
tp.path    # => example.rb
```

For example, we can use build a simple tool to measure line coverage:

```ruby
$covered_lines = []

coverage_tracker = TracePoint.new(:line) do |tp|
  $covered_lines << [tp.path, tp.lineno]
end

coverage_tracker.enable

puts 'Hello world'           # => 'Hello world'
puts $covered_lines.inspect  # => [['coverage.rb', 9], ['coverage.rb', 10]]
```

So far, so sensible.
This is the sort of useful debugging task that TracePoint is usually used for, and I think it’s cool that this sort of power is built into Ruby core.

This power does have limits: it doesn't know the source code of the line that's about to run, which is pretty important for what we're doing:

```ruby
tp.line    # => NameError
```

but that's not actually an issue, because we have all the information we need to get it ourselves, and none of the restraint that would stop us:

```ruby
# note: tracepoint line numbers are 1-indexed, so they match what you
# see in your text editor, but File.readlines is 0-indexed.
line = File.readlines(tp.path)[tp.lineno - 1]
```

Reading the entire file on every line is very inefficient and it breaks in a REPL, but it works -- and if we can read one line of code, there's nothing to stop us reading the next line, and the next line after that.
Now we have access to the currently-running source code, we need to inspect it for variables, upward assignment arrows, and values.

[TracePoint]: https://ruby-doc.org/3.2.0/TracePoint.html





{% text_separator "⇑" %}




## Parse Ruby code with Ripper

If we have a line of source code, we could look for arrows with something like [`String.index`][index]:

```ruby
'puts "Hello world"'.index('⇑')               # => nil
'⇑'.index('⇑')                                # => 0
'puts "upward assignment uses ⇑"'.index('⇑')  # => 29
```

But this will find arrows anywhere in the line, including in places where it's not an operator -- like in the third example, where it's found an arrow in a string.
To do this properly (and of course we care about doing things properly), we need to be able to parse Ruby source code.

Fortunately, Ruby has a built-in mechanism for doing this, in the [Ripper] module.
The method we want here is [Ripper.lex][lex], which breaks some code into a series of tokens.
Here's a simple example:

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

The result is an array of arrays, whose format is `[[lineno, column], type, token, state]`.
Each entry is a single token.

The `lineno` and `column` are pretty self-explanatory, and `token` is the source code for this token.
I'm not sure what all the values for `type` and `state` are, but I don't need to worry about them – I don't think I care about `state` at all, and I can see the values of `type` that might be interesting to me.
In particular, `:on_ident` and `:on_int` both look useful.

You need to be a bit careful of the `column` returned by `Ripper.lex`: it's counted based on bytes, not characters, so non-ASCII characters can throw it off.
For example, an identifier like `Münze` would take up 6 spaces, not 5.
(I was tipped off to this by [a comment in Kevin's vequals code][comment].)

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
Fortunately we have access to the original text in `token`, so we can just track the column manually.

By breaking the line into tokens with `Ripper.lex`, and filtering for tokens which have type `:on_ident`, we can find the identifiers:

```ruby
require 'ripper'

def find_identifiers_in_line(source_code)
  lexed_line = Ripper.lex(source_code)

  column = 0
  result = []

  lexed_line.each do |_positions, type, token, _state|
    if type == :on_ident
      result << {
        :token => token,
        :range => (column..column + token.length)
      }
    end

    # track the column manually
    column += token.length
  end

  result
end

find_identifiers_in_line('x = y + 1')
# [{:token=>"x", :range=>0..1},
#  {:token=>"y", :range=>4..5}]

find_identifiers_in_line('name = "Alex"')
# [{:token=>"name", :range=>0..4}]
```

This returns a list of hashes: each hash is a single identifier.
The hash has two keys: `:token` is the source code of the identifier, and `:range` tells us which characters it appears on in the line.

[index]: https://ruby-doc.org/3.2.0/String.html#method-i-index
[Ripper]: https://ruby-doc.org/stdlib-2.5.1/libdoc/ripper/rdoc/Ripper.html
[lex]: https://ruby-doc.org/stdlib-2.5.1/libdoc/ripper/rdoc/Ripper.html#method-c-lex
[comment]: https://github.com/kkuchta/vequals/blob/ca751ad6168c9810a89b0b5d59e6b1a3fbec10e6/vequals.rb#L42-L46





{% text_separator "⇑" %}




## Use TracePoint and Ripper to find the upward assignment arrows

We can put together what we've done so far to find all the identifiers on a line that have an upward assignment arrow below them:

```ruby
arrow_finder = TracePoint.new(:line) { |tp|
  this_line = File.readlines(tp.path)[tp.lineno - 1]
  this_identifiers = find_identifiers_in_line(this_line)

  next_line = File.readlines(tp.path)[tp.lineno]

  # if there's no next line, we're at the end of the file
  # there definitely isn't an arrow below us!
  return if next_line.nil?

  next_line_identifiers = find_identifiers_in_line(next_line)

  this_identifiers.each { |var|
    arrow_below =
      next_line_identifiers
        .filter { |id| id[:token] == "⇑" }
        .filter { |id| var[:range].cover? id[:range] }
        .last

    # If there's no arrow below us, we can move on to the next identifier
    next if arrow_below.nil?

    puts "L#{tp.lineno} variable #{var[:token]} has an arrow below it!"
  }
}

arrow_finder.enable

x
⇑
4
# L49 variable x has an arrow below it!
```

We read the current line and the next line; if there is no next line, then we can bail out early -- there's definitely no arrow below us!
For each identifier, we look for identifiers on the next line which (1) are the upward arrow and (2) overlap with this identifier.

This uses [ranges], which are a new-to-me feature of Ruby.
I particularly like the [`cover?` method][cover], which tells you if one range is contained by another.
It's not a complicated function, but it can be fiddly to get the inequalities the right way round, and a named function makes the intent clearer.

It find the last arrow operator that’s under an identifier, so that if a identifier sits above multiple arrows, the rightmost arrow takes precedence:

```ruby
best_number_of_cats
 ⇑  ⇑  ⇑  ⇑  ⇑  ⇑
 0  1  2  3  4  5
```

There are lots of other edge cases we might want to think about here if we were designing it properly, but let's pretend silly things like this can't happen, and move on.

[ranges]: https://ruby-doc.org/core-2.5.1/Range.html
[cover]: https://ruby-doc.org/core-2.5.1/Range.html#method-i-cover-3F





{% text_separator "⇑" %}





## Find the value below each arrow

Now we've found an arrow, we need to know what value is beneath it (if any).
A value is anything that we can assign to a variable -- a string, a number, another variable.
There are lots of different types of value; for now I'm going to just handle a couple of simple types, but you could extend this to find more types of value.

We can find values with a small modification of `find_identifiers_in_line`:

```ruby
require 'ripper'

def find_values_in_line(source_code)
  lexed_line = Ripper.lex(source_code)

  column = 0
  result = []

  lexed_line.each do |_positions, type, token, _state|
    if type == :on_ident || type == :on_tstring_content || type == :on_int

      result << {
        :type => type,
        :token => token,
        :range => (column..column + token.length)
      }
    end

    # track the column manually
    column += token.length
  end

  result
end

puts find_values_in_line('x = y + 1').inspect
# [{:type=>:on_ident, :token=>"x", :range=>0..1},
#  {:type=>:on_ident, :token=>"y", :range=>4..5},
#  {:type=>:on_int, :token=>"1", :range=>8..9}]

puts find_values_in_line('name = "Alex"').inspect
# [{:type=>:on_ident, :token=>"name", :range=>0..4},
#  {:type=>:on_tstring_content, :token=>"Alex", :range=>8..12}]
```

Then we drop this into our tracepoint, and look below the arrow we found in the prvious step:

```ruby
value_finder = TracePoint.new(:line) { |tp|
  this_identifiers = …
  next_line_identifiers = …

  value_line = File.readlines(tp.path)[tp.lineno + 1]
  return if value_line.nil?
  values = find_values_in_line(value_line)

  this_identifiers.each { |var|
    arrow_below = …

    matching_value =
      values.find { |v| v[:range].cover? arrow_below[:range] }

    next if matching_value.nil?

    puts "L#{tp.lineno} variable #{var[:token]} should be assigned to #{matching_value}"
  }
}

value_finder.enable

x
⇑
4
# L79 variable x should be assigned to {:type=>:on_int, :token=>"4", :range=>0..1}
```

This is quite fragile -- for example, if the arrow is above the opening/closing quotes of a string, it won't find the string, and it won't capture values that span multiple lines, but it's enough to get something basic working.

Now we know what we should be assigning, we just need to assign it.
Simple, right?





{% text_separator "⇑" %}





## Assign variables (or not) using bindings

This turned out to be the hardest bit, and I still don't fully understand what Ruby's doing here – but I got something working, and I'll explain as best I can.

When you're inside a tracepoint, you have access to something called a *binding*.
This contains a bunch of context about the current state of the program, including any variables and methods.

```ruby
tracepoint = TracePoint.new(:line) do |tp|
  puts tp.binding
end

tracepoint.enable

puts "Hello world"

# #<Binding:0x0000000143157090>
# Hello world
```

You can imagine how this would be useful for debugging -- by defining one tracepoint, you can track the value of a variable throughout your program, without having to litter your code with print statements everywhere you think might be useful.

This is an instance of the [Binding class][binding], and it doesn't just appear in tracepoints -- you can get bindings anywhere in Ruby.
Whenever you call the globally available [`binding` method][binding_meth], you get a copy of the current context, which you can then pass around like any any variable.
This allows us to break a bunch of rules around scope.

Here's an example of a program that doesn't work:

```ruby
def greet(name)
  first_name, last_name = name.split()
  puts "Hello #{first_name}!"
end

greet("Alex Chan")

puts first_name
```

<pre><code>Hello Alex!
greet.rb:8:in `&lt;main&gt;': <strong>undefined local variable or method `first_name' for main:Object (NameError)</strong></code></pre>

Inside `greet` I create a variable `first_name`, but it's only available inside that function.
When I'm in the top-level, I can't get to any of the variables inside the function.

But if I create a binding inside the function, and then return it, now I can get to all those variables:

```ruby
def greet(name)
  first_name, last_name = name.split()
  puts "Hello #{first_name}!"

  binding
end

b = greet("Alex Chan")

puts b.local_variable_get(:first_name)
```

```
Hello Alex!
Alex Chan
```

The binding holds a reference to the local variables inside the function, so when the binding is returned from the function, we can still get to those local variables.
This breaks the usual rules of scoping (*"variables defined inside a function are only available inside the function"*) and it's extremely powerful.
And as they say, power is a corrupting influence.

When I first read about bindings, I thought maybe I could use the [`local_variable_set` method][local_variable_set].
You can use it to update the value of an existing variable, and that gets reflected outside the binding:

```ruby
colour = "blue"

binding.local_variable_set(:colour, "red")

puts binding.local_variable_get(:colour)  # => red
puts colour                               # => red
```

but if you try to set a variable that doesn't exist yet, it's only available inside the binding:

```ruby
b = binding
b.local_variable_set(:shape, "square")

puts b.local_variable_get(:shape)         # => square
puts shape                                # => NameError
```

This is rather annoying, because it means we can't just call `tp.binding.local_variable_set` inside our tracepoint to create a new variable; we need to do something else.
We need to find a way to escape the binding.





{% text_separator "⇑" %}





## Sidebar: speculating about scope

I don't fully understand why this happens; scope is one of those topics I've never quite grokked.

Here's my best understanding of what happens: variables live in a *lexical scope*.
There are lots of different scopes in the lifetime of a program: for example, you get a new scope in the body of a function, and any variables defined in that function are only created in that scope.
When you leave that scope, you lose access to the varibales.

When a scope is created, it can include a reference to a variable in another scope.
This is how variables get passed into functions -- the function scope gets a reference to the variable in the main scope.

You can only access and modify variables you have access to in the current scope.
And if you modify a variable which is a reference to a variable in a parent scope, you modify it in the parent scope.

We can see this when, for example, a function modifies a variable that gets passed in:

```ruby
def append(shapes)
  new_shape = "square"
  shapes << new_shape
end

colours = ["red", "green", "blue"]
shapes = ["circle", "triangle"]
append(shapes)

puts shapes  # => ["circle", "triangle", "square"]
```

Here's what I think the scopes look like in this case:

<img src="/images/2023/scopes.png">

The main scope has two variables `colours` and `shapes`.
When we call the function, it gets a reference to the `shapes` variable, so it can access and modify that, but it can't access the `colours` variable.
It defines a variable `new_shape`, which is only available inside the function scope – it can't be accessed outside the function.
It then updates the `shapes` variable, which actually gets updated in the main scope.
When we leave the function, it's got the updated version of the variable.

Here's the key bit: I think you get a new lexical scope when you create a binding.
The binding scope has referneces to all the variables in the parent scope, but it's not the same scope.
If you update a variable which came from the parent scope, it gets updated in the parent scope.
When you create new variables in the binding, they're only created inside the binding scope, and not in the parent scope.

[binding]: https://ruby-doc.org/3.2.0/Binding.html
[binding_meth]: https://ruby-doc.org/3.2.0/Kernel.html#method-i-binding
[local_variable_set]: https://ruby-doc.org/3.2.0/Binding.html#method-i-local_variable_set





{% text_separator "⇑" %}





## Escaping through the `receiver`

Remember that a binding contains all the context about the program, including both variables and methods.
Variables live in the lexical scope, but where are the methods?

Methods are bound to objects, and every method in a binding is bound to an object called the `receiver`.
When you call a method in Ruby, people sometimes say you're sending a message to the object -- and the `receiver` is what receives those messages.
Crucially, the receiver is an object that lives outside the binding, so if define new methods on the receiver, they'll be available outside the binding.
And this is just what [`define_singleton_method` is for][define_singleton_method].

For example:

```ruby
b = binding
b.receiver    # => main
b.receiver.define_singleton_method(:greet) { puts "Hello world" }

greet         # => "Hello world"
```

We can also do this inside a tracepoint, and because the tracepoint runs before the line, the new method is available before the line runs:

```ruby
tracepoint = TracePoint.new(:line) do |tp|
  tp.binding.receiver.define_singleton_method(:greet) { puts "Hello world" }
end

tracepoint.enable

greet  # => "Hello world"
```

Methods and variables aren't quite the same, and they have slightly different behaviours, but they look close enough that I think we can get away with it.

[define_singleton_method]: https://ruby-doc.org/core-2.4.3/Object.html#method-i-define_singleton_method




{% text_separator "⇑" %}





## Turning a token into a value

When we found the value below each arrow, we got back a token from Ripper.lex, which isn't a value we can assign in a method.
But we can turn it into one:

```ruby
def convert_to_value(token)
  case token[:type]
  when :on_int
    token[:token].to_i
  when :on_tstring_content
    token[:token]
  when :on_ident
    eval("#{token[:token]}")
  end
end
```

The biggest crime here is the use of `eval` to turn a string containing a variable name into a variable.

We can drop this into our tracepoint, and our upward assignment operator springs into life:

```ruby
upwards_assignment = TracePoint.new(:line) { |tp|
  …

  this_identifiers.each { |var|
    arrow_below = …
    matching_value = …

    tp.binding.receiver.define_singleton_method(var[:token]) {
      |*args| literalize(matching_value)
    }
  }

  …
}
```

and now the variable will spring into existence!





{% text_separator "⇑" %}





## Putting it all together

We need a couple more tweaks to get this working: we need to define an empty method for `⇑` so it doesn't throw a NameError, and a bit more fiddling with bindings, but it does basically work.
I've wrapped it in a Uequals class (for "upward-equals", to match Kevin Kuchta's [Vequals class][vequals]), and it works like so:

```ruby
Uequals.enable

x
⇑
4

puts x  # => 4
```

You can chain instances of the uequals operator:

```ruby
x
⇑
y
⇑
3

puts x  # => 3
puts y  # => 3
```

This relies on a bit of trickery to create an empty placeholder for `y` just before the method for `x` is defined, otherwise you get more NameError's -- but it works, and that's the important thing:

You can also do parallel assignment:

```ruby
  x
y ⇑
⇑ 5
6

puts x  # => 5
puts y  # => 6
```

Unfortunately there are still some rough edges, and it starts to break down when you combine it with other assignment operators:

```ruby
x
⇑
y
⇑
z = 4

puts x  # => nil
puts y  # => nil
puts z  # => 4
```

I think you could make this example work, but it requires more and more looking ahead, and I'm running out of steam.
Minor issues like this, I think I can claim to have done what I set out to do: create a working upward assignment operator.

If you want to play with it yourself, I've uploaded a complete copy of the code in this post, including some comments and examples:

[vequals]: https://github.com/kkuchta/vequals





{% text_separator "⇑" %}





## Being serious, briefly

While creating an upward assignment operator is fun, it's not really the point of this post.
Absolutely nobody, including me, is going to use this code.


```ruby
           knowledge
utility        ⇑
   ⇑          100
   0
```

This was a learning exercise.
I'd already learnt some new stuff by watching Kevin's original talk, but actually implementing an operator myself taught me much more.

I wrote something like 100 scripts for this project, and by running them I learnt a lot of new stuff about Ruby behaves.
Most of the code I write is "familiar": it's using features I already know, and I have a good idea of what'll happen before I run it.
But here, because I was using so many new-to-me features – TracePoint, Ripper, bindings, lexical scope – I learnt a lot in a short amount of time.
This may not be useful code, but it is useful knowledge.

I really recommend downloading some of the code snippets and playing with it yourself; I think it's a much better way to learn than just reading about what somebody else has done.

And as always, writing it down on a blog post helped cement this new knowledge. I still don't understand all of it, but trying to explain what I've learned to somebody else how to find the gaps in my thinking.
Writing blog posts remains one of the best ways for me to learn about new programming concepts.

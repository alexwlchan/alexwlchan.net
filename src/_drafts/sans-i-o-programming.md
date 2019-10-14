---
layout: post
title: "Sans I/O programming: what, why and how (PyCon UK talk)"
summary:
category: Talks
theme:
  color: 008921

index:
  best_of: true
---

Last month I gave a talk about PyCon UK about "sans I/O programming".
This is a style of programming I've been trying to use for a while, and I've found it quite helpful.
It's not something revolutionary, but a slightly nicer way to write code.
The result is code that's simpler, cleaner, and easier to reuse and test.

This isn't an original idea or term: I first encountered it a couple of years ago while working on the [hyper HTTP/2 library](https://github.com/python-hyper/hyper-h2), and I'm sure the idea is older than that.

The talk was recorded, and you can watch it [on YouTube](https://www.youtube.com/watch?v=qwTWqy0uPbY)

{% youtube https://www.youtube.com/watch?v=qwTWqy0uPbY %}

You can read the slides and my notes on this page, or download the slides [as a PDF](/files/pyconuk_2019_sans_io.pdf).

The talk was transcribed, and these notes are based on that transcript.
The two STTRs that day were Wendy Osmond and Hilary Maclean; I'm not sure who was transcribing my particular talk.



## Links/recommended reading

Writing I/O-Free (Sans-I/O) Protocol Implementations
https://sans-io.readthedocs.io/how-to-sans-io.html
Building Protocol Libraries the Right Way
https://www.youtube.com/watch?v=7cC3_jGwl_U
Designing an async API, from sans-I/O on up
https://snarky.ca/designing-an-async-api-from-sans-i-o-on-up/
SansIO – Migrating microservices to async
https://smarketshq.com/sansio-migrating-microservices-to-asyncio-b97c69e391b2



## Slides and notes

{% slide_image :deck => "sans_io", :slide => 1, :alt => "Title slide." %}

Title slide.

I'm going to talk about sans I/O programming.
This is a pattern of programming I've been trying to use the last couple of years.
It helps my code be a bit simpler and cleaner to work with.
It's not revolutionary, it won't change the way you code forever, but hopefully it will help you write slightly nicer code -- whether or not you write Python for a day job.

I'll show you what it means, some of the problems of not adopting this pattern and you might want to use it in your own codebase.



{% slide_image :deck => "sans_io", :slide => 2, :alt => "Bio slide. Four icons on circles, with accompanying text (text below)." %}

Introductory slide.

*   Hi, I'm Alex.
    If you want to live tweet along with this talk, I'm @alexwlchan.

*   I've been helping to organise PyCon UK for the last four years.
    *[A common bit of feedback from 2018 was people asking for more technical talks -- hence why I wrote this one!]*

*   For my day job, I build digital preservation software for an organisation called the Wellcome Trust, who are sponsoring this year's conference.
    I'll talk more about my job in a moment.

*   I'm trans and I use they/them pronouns.



{% slide :deck => "sans_io", :slide => 3, :alt => "The Wellcome Collection building." %}
  Photo credit: Wellcome Collection.
{% endslide %}

I work for the [Wellcome Trust](https://wellcome.ac.uk).
Specifically, I work in [Wellcome Collection](https://wellcomecollection.org/), which is a free museum and library in London.
Among the things we hold in our museum, we have a large archive about the history of medicine and human health -- thousands of boxes and manuscripts.



{% slide :deck => "sans_io", :slide => 4, :alt => "A three step process. A BagIt package (a white paper bag), then the storage service (a green rect with some black gears), and then Amazon S3 (a red bucket). There are arrows from the BagIt package to the storage service, and from the storage service to S3." %}
  Icon credits: paper bag by [Dorian Dawance](https://thenounproject.com/term/paper-bag/28579/), process/gears by [Alice Design](https://thenounproject.com/term/process/2473979/), bucket from [AWS Simple Icons](https://commons.wikimedia.org/wiki/File:AWS_Simple_Icons_Storage_Amazon_S3.svg).
{% endslide %}

Alongside the physical archive we also hold a digital archive, and that's what I work on.
Specifically, I built a storage service that looks after all the digital files.

We receive files in a [BagIt package](https://tools.ietf.org/html/rfc8493) -- BagIt is a format often used for digital archives, which might contain things like a digitised book, sound or video recordings, files we've received from somebody's hard drive.
They get uploaded to a storage service (which is the thing I build), we count out the files, verify checksums and so on, and assuming it's all okay, we upload a copy to Amazon S3 where it will be stored in perpetuity.



{% slide_image :deck => "sans_io", :slide => 5, :alt => "GitHub search result for two libraries: LibraryOfCongress/bagit-python, and LibraryOfCongress/bagit-java." %}

To build our storage service, we need to be able to work with these BagIt packages.
We need some code that can unpack them, read them, understand their format and so on.

We looked on GitHub and we found two packages that will do this job for us.
Brilliant!
We'll use these packages, install them in our project, and we're good to go.
We can use Python, or we could use Java (because we write in Scala at Wellcome), so we have choices -- except we can't.

Both of these libraries have a fairly fundamental design limitation.
They assume that your BagIt packages exist as files on a local disk.
They assume you've downloaded the whole bag, saved it somewhere, and now they'll read it off your disk.



{% slide_image :deck => "sans_io", :slide => 6, :alt => "Examples of code from the BagIt libraries in Python and Java. In both cases, the code is using a parameter ‘/path/to/bag’, which is highlighted in green." %}

Here's an example of how to use both the libraries: you pass them a path to the bag, they go and start reading files from that path on disk.
They read some bytes from a file, do some parsing, read some more bytes from more files, do some parsing, and so on.

But our bags don't exist on a disk -- they exist in S3, and we don't want to be downloading the whole bag every time we want to do some work.
This means we can't use these libraries.



{% slide_image :deck => "sans_io", :slide => 1, :alt => "Placeholder" %}

Because the libraries are mixing this I/O logic and BagIt parsing, we ended up having to write our own BagIt parsing library.
That's a bit of shame -- it's work we would rather not have done.
It means there's another BagIt parser in the world, which isn't adding anything.

That was a bit of a pain for us, but maybe this is just because BagIt is a weird, obscure packaging format, and the people who wrote it aren't very good software developers?
Nope.



{% slide_image :deck => "sans_io", :slide => 1, :alt => "Placeholder" %}

Let's think about a much more popular protocol: HTTP.

There are more HTTP libraries than BagIt libraries.
In the Python ecosystem we have a rich variety of them.
There's urllib3, aiohttp, Flask, there are command line tools like httpie, and yet if you ever try to look at some of these HTTP libraries you will discover you have the same problem we have with BagIt libraries.
If a library doesn't match your I/O model or async primitive, it can be really hard to use.

For example, if it's a real pain to use Requests with Tornado unless you want to get really down and dirty with the Tornado threadpool.
HTTP libraries end up being written to suit the I/O or the async primitive, and so they don't share any code.

If you look at it, httplib does exactly what those BagIt libraries were doing, except with sockets instead of files.
To handle a HTTP request, it reads data from a socket, does some parsing, reads some data from a socket, does some parsing, but if you're not doing HTTP over a socket, or you want to control that socket yourself, that doesn't work for you.
Because the HTTP state machine logic in httplib is so closely tied to that logic, it's really hard to disentangle the two.
Every time somebody wants to create a new HTTP library, they have to build their own interpretation of the parser and state machine.
They're getting good code reuse, and that's kind of sad.
We're all told that code reuse is a good thing, we should strive to have more code reuse, so in something as fundamental as HTTP, maybe it's an anti-pattern that we don't seem to have as much code reuse as we would like.

I want to unpack the problems of not having so much code reuse.
A couple of reasons.



{% slide_image :deck => "sans_io", :slide => 1, :alt => "Placeholder" %}

It means we have wasted time and effort.

We're all solving the same problem, right?
The idea of file formats or protocols is that we all have a very consistent understanding of what they mean.
There is one way to parse a BagIt package.
There is one way to make a HTTP request, and we should all agree what that format is.
Creating another parser or another thing that's going to repeat that logic isn't really adding anything to the world; it's just repeating code.
That's that time and effort that we could be spending on something better.



{% slide_image :deck => "sans_io", :slide => 1, :alt => "Placeholder" %}

Another problem: if we have duplicate code hanging around, we have duplicate bugs.
Parsing stuff, doing business logic, is a tricky problem.
It's hard to get right.
There are subtle errors.

I imagine lots of people in this room think they can write an RFC compliant HTTP/1.1 or BagIt parser -- I'm one of them -- and we are probably all wrong because parsing is really hard!
So when we have multiple copies of the parser, and they're all independent and not showing any code, that means they're not sharing information about bugs.
If I find a bug in Gunicorn and fix it there, that same bug might exist in other HTTP stacks, but it's unlikely it will get to them.



{% slide_image :deck => "sans_io", :slide => 1, :alt => "Placeholder" %}

Another problem of not being able to share code is that it makes it harder to experiment.
We have some libraries with pretty good HTTP APIs.
Requests is very nice, and I imagine that's what most of you are using but it's not the only way to do HTTP.
Maybe you have a good idea of how we could do it using generators or the yield statement or dict comprehensions, I don't know, or whatever -- you know, using the matrix operator in Python 3.7.
Who knows?
But if you want to play with APIs like that, you'd have to write your own HTTP parser first.



{% slide_image :deck => "sans_io", :slide => 1, :alt => "Placeholder" %}

Finally, tying your I/O and business logic together makes it harder to optimise because the two things are inextricably linked.
Isolating, trying to work out where the slow bits and hot paths are and make things go faster is really hard.

Put your hand up if you've ever opened a file in Python.
*(Pretty much every hand in the room goes up.)*
Keep your hand up if you can tell me every one of the 30 different flags that `open()` accepts, which operating systems they are available for and what they all do.
*(Every hand goes down.)*

Fine, we don't care about those because maybe our job is not to optimise I/O, but there are people whose job it is.
It's their job to squeeze an extra three socket calls or five file handles out of the system every second, and if it's tied in with our parsing code, business logic, it's harder to optimise our code.



{% slide_image :deck => "sans_io", :slide => 1, :alt => "Placeholder" %}

So mixing I/O and business logic -- parsing, file format management, data analysis -- it causes some problems.

I hope you all accept these are legitimate problems, and these are things we have to worry about.
But it's probably not a catastrophe.
This is not a disaster.
My computer is not going to crash tomorrow because I mixed my I/O and my business logic.
That's why why this is often a thing that we don't think about, because we can do our jobs without it.
It slows us down, creates drag on development, adds some technical debt, but it's not the end of the world.
We can get by without it.



{% slide_image :deck => "sans_io", :slide => 1, :alt => "Placeholder" %}

But we know there is a problem here, there's an inefficiency in the way we write code.
Let's try and fix it.
How do we fix this problem?

Never do I/O!
We should rewrite everything as pure programming, give up on Python, just write Haskell, never do any side effects, never do any I/O.

That is not the message of this talk.



{% slide_image :deck => "sans_io", :slide => 1, :alt => "Placeholder" %}

We live in the real world and we do need to do I/O sometimes.
We do need to read things from files.
We have to do some I/O.

The better way is: **never mix your I/O and business logic**.

Try and keep those two things separate.
You want to build a 50-foot wall in your programme, put business logic on one side, everything that's doing in-memory operations, and put your I/O on the other side.
Then define a clear interface between them.
Push all the I/O out to the edges.



{% slide_image :deck => "sans_io", :slide => 1, :alt => "Placeholder" %}

I like to think about creating an I/O sandwich.
We have an inbound I/O layer talking to a network or socket or file; it gets some bytes in from wherever, then passes those to our business logic layer.
That layer gets some bytes, some in-memory objects; it manipulates them, does the transformations and works out what it wants to do next; and then it passes those objects back to the outbound I/O layer and the business logic is done with them.
It doesn't care whether you are going to send them to a file, or a socket, or by smoke signals -- it's just going to emit some bytes and then wash its hands of them.



{% slide_image :deck => "sans_io", :slide => 1, :alt => "Placeholder" %}

When you've done this, you can build a toolbox on top of it, so you have the business logic in the middle and it deals with nice in-memory objects or byte strings or whatever, and then you can change the I/O layer around it really easily.
It's just a thin wrapper around that core logic.



{% slide_image :deck => "sans_io", :slide => 1, :alt => "Placeholder" %}

This isn't everything.
There are some times when the parsing logic does need to inform our I/O, but it's a good start.
When you write your programs this way and build this I/O sandwich, you do see some benefits.



{% slide_image :deck => "sans_io", :slide => 1, :alt => "Placeholder" %}

So what are those benefits?



{% slide_image :deck => "sans_io", :slide => 1, :alt => "Placeholder" %}

You get much simpler code, because I/O is complicated.

I/O introduces a huge number of failure cases to your programme, a whole new set of exceptions or error cases that you need to catch and handle.
This is in the middle of what is already some potentially quite tricky code -- and at some point you might throw an error and that unravels the entire stack.
If there are bits of your codebase where you don't have to worry about I/O, those bits of your codebase get much simpler, and you get much simpler flow control.



{% slide_image :deck => "sans_io", :slide => 1, :alt => "Placeholder" %}

When your code is much simpler, it's much easier to test.

I/O in tests is just a pain, isn't it?
You've got to create temporary files or mock objects and account for the side effects and clean up afterwards and yuck, it's all just a mess.
If you're not doing any I/O, if you're just parsing around in-memory objects, byte strings, in-memory objects, lists, whatever -- it's just function calls, and testing function calls is easy.

It's really easy to test code that's not doing any I/O, because you don't have to worry about any weird I/O failure states.



{% slide_image :deck => "sans_io", :slide => 1, :alt => "Placeholder" %}

Better than that, if your function isn't doing any I/O and is just dealing with in-memory objects, then you can easily test your code to 100% coverage.
for every branch and statement in your function, there should be some in-memory object, sequence of bytes, whatever, that hits that line of code.
If there's no input that hits that line of code, then you can delete the code, because it's unhittable.

This is the sort of thing that's really hard to do if you're dealing with I/O, because you have to simulate all sorts of weird I/O failure cases and you have to hope that you've caught them all.
When you are just testing functions that deal in pure in-memory objects, it gets a lot simpler.



{% slide_image :deck => "sans_io", :slide => 1, :alt => "Placeholder" %}

One example: this is the test suite for hyper-h2, an HTTP/2 parsing library in Python.
This ran 1500 tests in barely half a minute.

That gives us a very high degree of confidence in this code.
It's been tested very thoroughly, and several of these tests are tests using Hypothesis (a property-based testing library which runs hundreds of examples for each test), so realistically you're getting closer to two or three thousand test cases here, all checking that this code is behaving correctly.
This is a level of coverage that's difficult to achieve if you mix I/O and logic.




{% slide_image :deck => "sans_io", :slide => 1, :alt => "Placeholder" %}

By just testing in-memory objects, we write dramatically simpler tests, and if you have better tests you have less bugs.
Because it's just function calls, it's really easy to explore all those weird corners of the program and make sure it is behaving correctly.
When you have less bugs, you have to deal with less bug reports, so that's another thing I enjoy.



{% slide_image :deck => "sans_io", :slide => 1, :alt => "Placeholder" %}

Finally, coming back to where I started -- when your code is sans I/O and you build these thin wrappers around the edge, your code gets much easier to re-use.
It's much simpler to take off one I/O layer and plug something else in -- everything in the middle doesn't care about the I/O layer and completely ignores it.



{% slide_image :deck => "sans_io", :slide => 1, :alt => "Placeholder" %}

So let's go back to this storage service I was talking about earlier.
We reading these bags, parse them and upload them to S3.
We've written code to deal with these BagIt packages -- to read and write them in S3

To make our archive more secure, we want multiple copies of these bags, so we write a copy of them to Azure Blob Storage.
That way, if AWS goes away or closes our account or Dublin sinks into the sea, all of our data is secure.

If we had written our BagIt parsing code to only be able to talk to S3, and we'd baked that in, it would be a pain to add Azure Blob Storage.
Because we wrote our code in a sans I/O way, it's really easy to reuse that code with Azure Blob Storage.
The BagIt parse doesn't know, it just hands out bytes and says: hey, put this somewhere.



{% slide_image :deck => "sans_io", :slide => 1, :alt => "Placeholder" %}

So those are some of the benefits you get from separating your I/O and your business logic, your I/O and your data analysis or your parsing layer.
You get simpler code, code that's easier to test, that's more robust and easier to re-use.
Again, these aren't ground breaking things, it's not a revolutionary thing that will change the way you program, it's just a nice solid improvement for code quality.



{% slide_image :deck => "sans_io", :slide => 1, :alt => "Placeholder" %}

Create that I/O sandwich.
Push the I/O out to the boundaries, and keep the core of your program I/O free and pure.




{% slide_image :deck => "sans_io", :slide => 1, :alt => "Placeholder" %}

I want to show you a few examples, so you can see how other people have done this.



{% slide_image :deck => "sans_io", :slide => 1, :alt => "Placeholder" %}

First, let's create an HTTP/2 server with a hyper-h2.

We create this Python object.
We call this `initiate_connection()` method, and this starts building a buffer of bytes internally that we can send on the wire -- but it doesn't send those bytes anymore, just stores them in-memory.
Later, we call `data_to_send()`, it hands us back that buffer and says, "great, here are some bytes you should send.  I don't care if you send them to a file or socket or pigeon carrier."
It washes its hands at that point -- it just does all of that HTTP/2 logic entirely in-memory.

I imagine most of you aren't working with low-level HTTP interactions, so let's look at something higher level.



{% slide_image :deck => "sans_io", :slide => 1, :alt => "Placeholder" %}

Second example is calling the Slack API with a slack-sansio Slack library

We will create a `CHAT_POST_MESSAGE` object and a dict that contains our payload data.
This library has an abstract class, and it asks you to fill in this `_request` method, which processes a simple HTTP request.
The class does all the work to turn your query object into an HTTP request, and then calls this `_request` method.
It provides an implementation in Requests, or in curio, or in asyncio or whatever, and it's easy to build new HTTP implementations on top of that if you need them.

The core of the library doesn't change.
That's another nice example to look at.



{% slide_image :deck => "sans_io", :slide => 1, :alt => "Placeholder" %}

One final example, looking at refactoring a function in the bagit-python library I mentioned at the start.

Sans I/O doesn't need to be a big, all-in-one change.
You can't take six weeks out of your sprint to re-factor all your code to be nice and sans I/O because someone at PyCon told you about it; you can make small, incremental improvements.

We've got a function here that's going to load something called a *tag file*.
It takes the name of that file, then opens that file on that disk, that yucky I/O I was talking about earlier that doesn't connect to S3 -- and then it has all the code that actually parses the content of that file.
It's treating open the file as a list of strings.


{% slide_image :deck => "sans_io", :slide => 1, :alt => "Placeholder" %}

Let's pull all this complex parsing logic out into a separate function.
This function is now a little bit simpler, deals entirely with an iterable of strings, so it's easy for us to test and we can re-use this function in a lot of other contexts.
Then we just call this new function from the old function.

The old API is preserved, all the tests will still pass.
Anybody using the old code won't notice the difference, but this code is now a little bit more reusable.
If you are getting your lines rather than from a file, say from S3, or Azure Blob Storage or somewhere else, you can feed them into the second function and you can reuse that code.



{% slide_image :deck => "sans_io", :slide => 1, :alt => "Placeholder" %}

So create that I/O sandwich, push the I/O out to the boundaries of your programme.

This isn't going to completely change the way you do programming and it won't turn the world upside-down, but it will just give you code that's a little bit simpler, a little bit cleaner, a little bit easier to work with.
I hope I've persuaded you that there is some virtue in writing your programs this way, given you some idea of how it's done and when you go back to your day jobs you'll try it yourself.

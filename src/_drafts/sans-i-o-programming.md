---
layout: post
title: "Sans I/O programming: what, why and how"
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

<!-- <style>
  .slide img {
    border: 1px solid #00D220;
  }
</style> -->

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

---

Because the libraries are mixing this I/O logic and mixing BagIt package of the packaging format we ended up having to write our own BagIt parsing library and that's a bit of shame, work we would rather not have done, it means there's another BagIt package in the world which really isn't adding anything so that was a bit of a pain for us but maybe this is just because BagIt is a weird, obscure packaging format and people who wrote it aren't very good software developers.  Who had heard of the BagIt packaging format before today?  One person!  We would admit this is a fairly obscure standard so let's look at something perhaps a few more of you have heard of.  Hands up if you have heard of this rarely used networking protocol called HTTP?  For the benefit of the video, we have a few more hands in the audience.  [Laughter]
So there are a few more HTTP libraries than BagIt libraries.  In the Python ecosystem we have a rich variety of them, there's urllib3, aiohttp, I think we have Flask in the very next slot, there are command lines like HTTP ie, and yet if you ever try to look at some of these HTTP libraries you will discover you have the same problem we have with BagIt libraries.  If your library isn't matched it can be really hard to use.  For example, if you are going to be using Requests, it's a real pain to use Requests with something like Tornado unless you want to get really down and dirty with the thread core.  HTTP libraries end up being written to suit the I/O or the async primitive and as a result these libraries don't share any code.  If you look at it, httplib does exactly what those BagIt libraries were doing except with sockets.  To parse a HTTP request is reads data from a socket, does some parsing, reads some data from a socket, do some parsing, but if you are not doing HTTP over a socket or you want to control that socket yourselves, that doesn't really work for you, and because the HTTP state machine logic in httplib is so closely tied to that logic it's really hard to disentangle the two.  So every time somebody wants to create a new HTTP library they end up having to build their own interpretation of the parser and state machine which means they are not getting good code re-use, and that's kind of sad.  We are all sold that code re-use is a good thing, we should strive to have more code re-use, so in something as fundamental as HTTP perhaps, you know, maybe it's an anti-pattern that we don't seem to have as much code re-use as we would like.  I want to unpack a bit more the problems of not having so much code re-use and why that is.  A couple of reasons.  First of all, it means we have wasted time and effort and basically we are solving the same problem, right?  The idea of file formats or protocols is that we all have a very consistent understanding of what they mean.  There is one way to parse BagIt package.  There is one way to make a HTTP request and we should all agree what that format is.  Creating another parser or another thing that's going to do that logic isn't really adding anything to the world; it's just repeating code.  So that's that time and effort that we could perhaps best be spending on something else.  Another problem, if we have a duplicate code hanging around is we have duplicate bugs.  Parsing stuff, doing business logic, is quite a hard, tricky problem.  It's hard to get right.  There are subtle errors.  I imagine lots of people in this room think they can write an RFC compliant HTTP/1 .1 or BagIt parser -- I'm probably one of them -- and we are probably all wrong because parsing is really hard!  So when we have multiple copies of the parser and they are all independent and not showing any code, that means they are not sharing information about bugs and so if I fix a bug in Gunicorn and then I fix it in Twisted or -- sorry, I completely screwed up the sentence.  Let me try again.  If I find a bug in Gunicorn and fix it there, that same bug might exist in others but it's unlikely it will get across to it.  There are multiple independent sources of bugs, so that's another problem.  Another thing about not being able to share code is that it makes it harder to experiment.  We have some libraries with pretty good HTTP APIs.  Request is very nice and I imagine that's what most of you are using but Request is probably not the pinnacle.  Maybe you have a good idea of how we could do it using generators or the yield statement or dict comprehensions, I don't know, or whatever -- you know, using the matrix operator in Python 3.7.  Who knows?  But if you want to expand with APIs like that and write with HTTP you would have to write your HTTP parser first.
Finally, tying your I/O and business logic together makes it harder to optimise because the two things are inextricably linked.  Isolating, trying to work out where the slow bits and hot paths are and make things go faster is really hard.  Yes, we are in Python world so maybe we don't care about optimisation and performance, but you know, there are some people who do.  A quick show of hands in the room, who here has opened a file in Python?  Okay, that's pretty much every hand in the room.  Now put your hand up if you can tell me every one of the 30 different flags that command accepts, which operating systems they are available for and what they all do.  Okay, that's nobody.  Of course, fine, we don't care about those because maybe our job is not to optimise I/O but there are people whose job it is.  It's their job to squeeze an extra three socket calls or five call handles out of the system every second and if it's tied in with our parsing code, business logic, it's really hard to get our code optimising.
So mixing I/O and business logic, which could be parsing, it could be file format management, it could be data analysis, it causes some problems.  I think you would all accept these are legitimate problems and these are things we have to worry about.  I hope you also realise that this is probably not a catastrophe.  This is not a disaster.  My computer is not going to crash tomorrow because I mixed my I/O and my business logic.  That, I think, is why this is often a thing that we don't often think about because we can afford to do our jobs without it.  It slows us down, creates drag on development, adds some technical debt but it's not the end of the world.  We can get by without it.  But let's suppose, you know, there is a problem here, there is perhaps inefficiency in the way we write code, so let's try and fix it, so how do we fix this problem?  Well, I hope the answer is clear: never do I/O!  We are going to re-write everything as pure programming, we are going to give up on Python, just write Haskell, never do any side effects, never do any I/O.  That is not the message of this talk.  [Laughter]
Because, you know, we live in the real world and we do need to do I/O sometimes and we do need to read things from files.  We have to do some I/O.  The answer is: never mix your I/O and business logic.  Try and keep those two things separate.  You want to build a 50-foot wall in your programme, put business logic on one side, everything that's doing manipulations, and put your I/O on the other side and define a career interface between them so you push all the I/O out so I like to think about creating an I/O sandwich, so we have an inbound I/O layer talking to a network or socket or file; it gets some bytes in from wherever, then passes those to our business logic layer which just gets some bytes, some in memory objects, it manipulates, does the transformations and works out what it wants to do next; and then it parses those objects back out to the outbound I/O layer and the business logic is done with them.  It doesn't care whether you are going to send them to a file or a socket or by smoke signals, it's just going to send those bytes out and then wash its hands of them.  What you can do when you've done this is you can build a toolbox on top of it, so you have the business logic in the middle and it deals with nice in memory objects or byte strings or whatever, and then you can change the I/O layer around it really easily because it's just a thin wrapper around that core logic.
This isn't everything, right?  There are some times when the parsing logic does need to inform our I/O but it's a good start and when you write your programs this way and build this I/O sandwich that pushes I/O out to the boundaries you do see some benefits.  So what are those benefits?
First of all, you get much simpler code because I/O is complicated.  I/O introduces a huge number of failure cases to your programme, a whole new number of exceptions or error cases that you need to try and catch and handle and this is in the middle of what is already some potentially quite tricky code that you are doing in business logic, working out what analysis to do, working out how to do parsing, at some point you might throw an error and that unravels the entire stack.  If there are bits of your codebase where you don't have to worry about I/O those bits of your codebase get much simpler, so you get much simpler control when you are not having to worry about I/O.
When your code is much simpler, it is much easier to test, and we all test our code, right?  I didn't see everyone in the audience nodding so let's try that again.  We all test our code, right?  [Laughter]
I will talk to the people at the back later.
Okay, no, code is easier to test -- why, when you are not doing I/O -- aside from it being simpler, well, because I/O in tests is just a pain, isn't it?  You've got to create temporary files or mock objects and account for the side effects and clean up afterwards and yuck, it's all just a mess.  If you are not doing any I/O, if you are just parsing around in memory objects, byte strings, in memory objects lists, byte strings or whatever, it's just function calls and testing function calls is easy.  So you can test -- it's really easy to test code that's not doing any I/O, you've not got to worry about any weird failure states.  Better than that, if your functioning isn't doing any I/O and is just dealing with in memory objects you can test your code to 100% coverage really easily because for every branch and statement in your function there should be some in memory object, some sequence of bytes, whatever, that hits that line of code and if there's no input that you can provide that hits the line of code then you can delete it because it's unhittable.  This is the sort of thing that's really hard to do if you are dealing with I/O because you have to simulate all sorts of weird I/O failure cases and you have to hope that you've caught them all but when you are just testing functions that deal in pure in memory objects it gets a lot simpler.
One example, this is the test suite for a HTTP/2 parsing library in Python.  This ran the test in a little under the time -- just under the time it took me to finish this sentence.  And that gives us a very high degree of confidence in this code.  It's been tested very thoroughly and in fact several of these tests are tests using hypothesis which is a property-based testing library which runs hundreds of examples for each test, so realistically you are probably getting closer to 2 or 3,000 test cases here that are certain that this code really is behaving correctly.  This is a level of coverage that it's very difficult to achieve if we are mixing I/O logic in here so by just testing in memory object we are able to write dramatically simpler tests and of course if you run better tests you have less bugs and everybody likes less bugs.  Because it's just function calls, it's really easy to explore all those weird forms of the program and make sure it is behaving correctly and when you have less bugs you have to deal with less bug reports so that's another thing that I really like.
Finally, coming back to where I started where I talked about code re-use, when your code is sans I/O and you are building these thin wrappers around the edge your code gets much easier to re-use.  It's much simpler to take off one I/O layer, plug something else in because all the data analysis whatever in the middle doesn't care about the I/O layer and completely ignores it.
So let's go back to this storage service I was talking about earlier.  We were reading these bags, parsing and uploading to S3.  Now, if we just -- okay -- let me try again.  We've written code to deal with all these BagIt packages to read and write them and we are going to write them into S3 but in fact to make our archive more secure what we would really like to do is actually have multiple copies of these packages, so in particular what we also do is we write a copy of them to Azure Blob Storage.  That way, if AWS goes away or closes our account or sinks into the sea, all of our data is secure.  If we have written our BagIt parsing code to only be able to talk to those three and we baked in a layer into that it would be a real pain to change this to Azure Blob Storage but because we wrote our code in a way that didn't care about the I/O layer it's really easy to parse that code into Azure Blob Storage and it doesn't know, it just hands out bytes and says: hey, put this somewhere.  So that's really nice.  So those are some of the benefits you get from separating your I/O and your business logic, your I/O and your data analysis or your parsing layer.
You get simpler code, code that's easier to test, that's more robust and easier to re-use.  Again, these aren't ground breaking things, it's not a revolutionary thing that will change the way you programme, it's just a nice solid improvement for code quality.  Again, creating that I/O sandwich, pushing the I/O out to the boundaries and keeping the core of your programme I/O free and pure.
So we've got five minutes left so I want to show you a couple of examples of what this looks like in practice so you can see what other people have been doing to build this.  First one, we are going to create a HTTP/2 server with a hyper-h2, so what we are going to do is create this Python object, all in memory.  We call this initiate connection method and what this starts doing is building up a buffer of bytes internally that we can send on the wire but it doesn't send those bytes anymore, just stores them in memory and at some point we call data to send, it hands us back those bytes and says: great, here are some bytes you should send.  I don't care if you send them to a file or socket or pigeon carrier, it washes its hands at that point but is able to do all of that HTTP/2 logic entirely in memory.  I imagine most of you are not dealing at low level HTTP libraries although if you are, please come and talk to me because I'm really interested.  So let's look at something high level.
Second example is calling the Slack API with a slack-sansio Slack library, so again we will create our little object, this is in memory too, this chat post message object and a dict that contains our pay load data and this library has a little abstract class and it asks you to put in this underscore method which takes a simple request, it will then do all the work of how to turn your query object into a HTTP request and put it back on the wire for you.  So it provides an implementation in Requests, or in curio, or in asyncio or whatever, and it's easy to build HTTP implementations on top of that if you need them.  The core of the library doesn't change, so that's another nice library to look at.
One final one, looking at refactoring a function in that BagIt Python that I looked at to start with.  You don't take six weeks out of your sprint to re-factor all your code to be nice and sans I/O because someone at PyCon told me about it; you can just make these small, incremental improvements.  So let's look at that very briefly.  We've got a function here that's going to load something called a tag file, takes the name of that file, then opens that file on that disk, that yucky I/O I was talking about earlier that doesn't connect to S3 and then it has all the code that actually parses the content of that file where it's treating the file as a list of strings.  Let's pull all this complex parsing logic out into a separate function.  This function is now a little bit simpler, deals entirely with in memory lists of strings, so it's easy for us to test and we can re-use this function in a lot of other contexts.  Then we will just call this new function from the old function.  So the old API is preserved, all tests will still pass.  Anybody using the old code is not going to notice the difference but this code is now a little bit more re-usable so if you are getting your lines rather than from a file, say from S3, your Azure Blob or somewhere else, you can feed them into the second function and you will be able to re-use that code fine.  So create that I/O sandwich, push the I/O out to the boundaries of your programme.  This is not going to completely change the way you do programming and not going to turn your programme upside-down but it will just give you code that's a little bit simpler, a little bit cleaner, a little bit easier to work with.  I hope I've persuaded you that maybe there is some virtue in trying to write your programs this way, given you some idea of how it's done and maybe when you go back to your day jobs you will try this.  With that now I will finish, thank you very much.  [Applause]
JOHN:  Thank you very much.  We don't have time for questions, but I am sure Alex will be happy to answer loads at some point.
ALEX CHAN:  I'm around all week.
JOHN:  Thank you very much.  Give them another round of applause.  We will be back in five minutes for asynchronous web development.

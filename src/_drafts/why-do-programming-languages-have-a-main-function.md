---
layout: post
title: Why do programming languages have a main() function?
summary: Lots of programming languages have a function called main() where code starts executing. Where does this come from?
tags: programming history
---

Two days ago, Chris Siebenmann posted an article about [why Python doesn't require a main function][pymain]:

> Many languages start running your program by calling a function of yours that must have a specific name.
> In C (and many C derived languages), this is just called `main()`; in Go, it's `main.main()` (the `main()` function in the main package).
> Python famously doesn't require any such function, and won't automatically call a function called `main()` even if you create it.

This made me wonder: why do programming languages have a `main()` function?
Where did the idea for this special function come from, and who decided to call it `main`?
This didn't magically spring into existence; somebody had to design it first.
This took me down a bit of a rabbit hole into the history of programming languages.

This post is half an attempt to answer the question, half some interesting things I found along the way.
I'm not a computer history, and this is the result of an evening spent on Google -- please judge accordingly.

If you know of a proper answer to this question, please [send it my way](/#contact).
I'm unlikely to spend more time researching this, but I'd love to read about it if somebody else has.



## The main function in C

The [original version of C][c_wiki] was developed by Dennis Ritchie and Ken Thompson in the early 1970s.
This led to the publication of [*The C Programming Language*][k_and_r] (informally nicknamed *K&R*) in 1978, which introduces the concept of a `main()` function in the first chapter:

> In C, the program to print `“hello, world”` is
>
> ```
> #include <stdio.h>
>
> main()
> {
>     printf("hello, world\n");
> }
> ```
>
> […] Normally you are at liberty to give functions whatever names you like, but “`main`” is special---your program begins executing at the beginning of `main`.
> This means that every programm must have a `main` somewhere.

This is based on my copy of K&R, which is the 1988 second edition.
I don't have a first edition, but I know `main()` was being used as far back as 1978, because I found some C code [hand-written by Brian Kernighan][auction] (the K in K&R):

![](/images/2020/kernighan_hello_world.jpg)

Given how popular C was, I feel pretty safe saying that all the C-derived languages that came after C got the idea of `main()` from C.
So where did C get the idea from?



## Life before C

The introduction of K&R tells us a bit about the history of C:

> Many of the important ideas of C stem from the language BCPL, developed by Martin Richards.
> The influence of BCPL on C proceeded indirectly through the language B, which was written by Ken Thompson in 1970 for the first UNIX system on the DEC PDP-7.

Dennis Ritchie wrote a paper about the history of C, [*The Development of the C Language*][c_dev].
It goes into a lot of detail about the languages that preceded C, the development of Unix, and the culture of Bell Labs.

Among other things, you see ideas that would be familiar to programmers today.
For example:

> Other fiddles in the transition from BCPL to B were introduced as a matter of taste, and some remain controversial, for example the decision to use the single character `=` for assignment instead of `:=`.
> Similarly, B uses `/**/` to enclose comments, where BCPL uses `//`, to ignore text up to the end of the line.

We take a lot of these conventions for granted, but somebody had to invent them.
As I was searching around, I found several other times where a now-commonplace convention was introduced as something new.

If you have time, I recommend reading Ritchie's paper in full.



## What comes before C? B

Ritchie's paper includes a lot of information about B, including both the history and the technical aspects.
It explains that B was created as the systems programming language for the early versions of Unix.
He dryly notes, "[B] is BCPL squeezed into 8K bytes of memory and filtered through Thompson's brain".

He also describes B as the parent of C -- so does B have a `main()` function?

There's no sample B program in *The Development of C*, but I did find [*A Tutorial Introduction to the Language B*][b_tutorial], written in 1973, and it sounds very similar to K&R:

> All B programs consist of one or more "functions", which are similar to the functions and subroutines of a Fortran program, or the procedures of PL/I.
> `main` is such a function, and in fact all B programs must have a `main`.
> Execution of the program begins at the first statement of `main`, and usually ends at the last.

The tutorial includes a sample program to print the sum of three numbers:

```
main( ) {
  auto a, b, c, sum;

  a = 1; b = 2; c = 3;
  sum = a+b+c;
  putnumb(sum);
}
```

So it seems like C took the idea of `main` directly from B.
Where did B get the idea?



## BCPL (a Before C Programming Language)

If B is the parent of C, then BCPL is the grandparent.
It was designed by Martin Richards in 1967, two years before B.

I found a [BCPL reference manual from 1979][bcpl_ref].
The sample program in section 2.2 uses a function called `Main`:

```
let Main() be
  [main
        // Initialize the global vectors
        ...
  ]main
```

but I couldn't find the bit of the manual that explains why this procedure is special.
(The perils of scanned PDFs without OCR.)

It's also not clear if this was part of the original BCPL, or influenced by C.
Dennis Ritchie has an [older reference manual for BCPL][old_bcpl_ref], from 1967 (also no mention of `Main()`), which acknowledges that features went in both directions:

> BCPL has had a productive life of its own, but my interest in it is more in the basis it provided for the development of the B language and then in the history of C. […]
>
> Some of the lexical conventions actually used in early BCPL were directly adopted into B; some more recent ones may owe to back-influence from C.

Meanwhile, a [more modern BCPL spec][bcpl_modern] uses a procedure called `start()` as the initial function of a program, but no such procedure appears in the earlier manuals.

So maybe BCPL came up with this idea, or maybe it came back from C -- I'm not sure.



## Tangent #1: octal numbers

In the B tutorial, I was amused by a reference to the use of leading 0 to represent [octal numbers][octal].
This confused me when I first came across it; I've never had a use for octal numbers.

> Since B is often used for system programming and bit-manipulation, octal numbers are an important part of the language.
> The syntax of B says that any number that begins with 0 is an octal number (and hence can't have any 8's or 9's in it).
> Thus 0777 is an octal constant, with decimal value 511.

This seems to be new in B; in the 1979 BCPL reference section 4.2 describes a different syntax for octal numbers:

>   *   A string of digits preceded by a `"#"` is interpreted as an octal integer.
>       It must be less than 2**16-1 (177777 octal, 65535 decimal).
>   *   A string of digits immediately followed by "B" or "b" is also interpreted as an octal integer.
>       If the "B" or "b" is immediately followed by a (decimal) number n, the octal value is shifted n bits.
>       Thus, #1230, 1230B and 123B3 all represent the same value.
>       One-bits may not be shifted out of bit 0.



## Tangent #2: A world of no `return`

Today pretty much every language uses `return` to exit a function, optionally passing a value back to the caller -- but the 1979 BCPL reference hints at a different world.

In section 3.6 "Procedure declarations", it makes the following distinction:

> There are two kinds of BCPL procedures: "functions", which return a value upon completion, and "routines", which do not.

I can't think of any modern programming language that makes this distinction.
Further down, in section 5.6 "Returns", there are different statements depending on whether you're in a function or a routine:

> return <br/>
> resultis EXP
>
> These statements cause a return from the procedure in which they appear.
> "return" is only legal in a routine body; "resultis EXP" is only legal in a function body.

By the time B came around, the two statements had been collapsed into one: `return` was used whether or not the procedure passed a value back to the caller.

I wonder if there's an alternative timeline where we kept both statements?



## Tangent #3: Trusting the programmer

The [BCPL Wikipedia entry][bcpl_wiki] includes a passage from *BCPL: The language and its compiler*:

> The philosophy of BCPL is not one of the tyrant who thinks he knows best and lays down the law on what is and what is not allowed; rather, BCPL acts more as a servant offering his services to the best of his ability without complaint, even when confronted with apparent nonsense. The programmer is always assumed to know what he is doing and is not hemmed in by petty restrictions.

This has echoes of the ["We are all responsible users"][responsible] saying that I often hear in the Python community.



## Back to the `main` problem

Modern languages get their `main()` function from C.
That in turn came from B, and possibly from BCPL.

I did try to dig back further, into languages like FORTRAN, COBOL and ALGOL, all of which predate BCPL and B, and were cited as influences.
I couldn't find anything definitive about a main-like function in those languages, but I did find phrases like *"main procedure"* and *"main program"*.

I found a page of [historical documents in computer science][historical], with lots of manuals which might have more clues, but I haven't dug any deeper.


---

[pymain]: https://utcc.utoronto.ca/~cks/space/blog/python/WhyNoMainFunction
[c_wiki]: https://en.wikipedia.org/wiki/C_(programming_language)
[k_and_r]: https://en.wikipedia.org/wiki/C_(programming_language)#K&R_C
[auction]: https://www.artsy.net/artwork/brian-kernighan-hello-world
[c_dev]: https://www.bell-labs.com/usr/dmr/www/chist.html
[b_tutorial]: https://www.bell-labs.com/usr/dmr/www/btut.html
[octal]: https://en.wikipedia.org/wiki/Octal
[py_octal]: https://www.python.org/dev/peps/pep-3127/
[bcpl_ref]: http://bitsavers.org/pdf/xerox/alto/bcpl/AltoBCPLdoc.pdf
[old_bcpl_ref]: https://www.bell-labs.com/usr/dmr/www/bcpl.html
[bcpl_modern]: https://www.cl.cam.ac.uk/~mr10/bcplman.pdf
[bcpl_wiki]: https://en.wikipedia.org/wiki/BCPL
[responsible]: https://docs.python-guide.org/writing/style/#we-are-all-responsible-users
[historical]: http://web.eah-jena.de/~kleine/history/

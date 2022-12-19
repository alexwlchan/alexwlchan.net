---
layout: post
date: 2020-07-22 14:18:15 +0000
title: Why do programming languages have a main() function?
summary: Lots of programming languages have a function called main() where code starts executing. Where does this come from?
tags: programming history
---

<style>
  svg {
    margin-top: 2.6em;
  }
</style>

On Monday, Chris Siebenmann posted an article about [why Python doesn't require a main function][pymain], which began:

> Many languages start running your program by calling a function of yours that must have a specific name.
> In C (and many C derived languages), this is just called `main()`; in Go, it's `main.main()` (the `main()` function in the main package).
> Python famously doesn't require any such function, and won't automatically call a function called `main()` even if you create it.

This made me wonder: why do programming languages have a `main()` function?
Where did the idea for this special function come from, and who decided to call it `main`?
It seems ubiquitous today, but it didn't just spring into existence -- somebody had to design it.
Trying to answer the question took me down a bit of a rabbit hole into the history of programming languages.

This post is half an attempt to answer the question, half some interesting things I found along the way.
I'm not a computer historian, and this is only the result of an evening spent on Google -- please judge accordingly.
These are a few of the notes I made; not a complete answer.

If you know of a proper answer to this question, please [send it my way](/#contact).
I'm unlikely to spend more time researching this, but I'd love to read about it if somebody else has.



<center>
  <svg viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg" width="50">
    <rect x="25" y="75" width="450" height="350" fill="rgba(0, 0, 0, 0)" stroke="#f0f0f0" stroke-width="30" rx="25"/>

    <path d="M120 170, L200 250, L120, 330" stroke-width="30" stroke="#f0f0f0" stroke-linecap="round" fill="rgba(0,0,0,0)"/>
    <path d="M250 330, L380 330" stroke-width="30" stroke="#f0f0f0" stroke-linecap="round" fill="rgba(0,0,0,0)"/>
  </svg>
</center>



## The main function in C

The [original version of C][c_wiki] was developed by Dennis Ritchie and Ken Thompson in the early 1970s, while they were both working at Bell Labs.
It was devised as a language to use with their then-new Unix operating system.

In 1978, Dennis Ritchie worked with Brian Kernighan to write [*The C Programming Language*][k_and_r] (informally nicknamed *K&R*), which served as an informal specification for C for a long time.
Although I'm sure earlier documents about C exist, the was the earliest I had readily available.
It introduces the concept of a `main()` function in the first example:

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

This book helped popularise the idea of ["hello world"][hello_world] as a simple first program, but it wasn't the first instance of it (more on that below).

This quote is taken from my copy of K&R, which is the 1988 second edition.
I don't have a first edition to hand, but I did find some C code [hand-written by Brian Kernighan][auction] in 1978:

![A hand-written and signed C program, mounted in a black frame.](/images/2020/kernighan_hello_world.jpg)

Given how popular C was, I feel pretty safe saying that most contemporary languages got the idea of calling their entrypoint `main` from C.
So where did C get the idea?



<center>
  <svg viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg" width="50">
    <rect x="25" y="75" width="450" height="350" fill="rgba(0, 0, 0, 0)" stroke="#f0f0f0" stroke-width="30" rx="25"/>

    <path d="M120 170, L200 250, L120, 330" stroke-width="30" stroke="#f0f0f0" stroke-linecap="round" fill="rgba(0,0,0,0)"/>
    <path d="M250 330, L380 330" stroke-width="30" stroke="#f0f0f0" stroke-linecap="round" fill="rgba(0,0,0,0)"/>
  </svg>
</center>



## Life before C

The introduction of K&R tells us a bit about the history of C:

> Many of the important ideas of C stem from the language BCPL, developed by Martin Richards.
> The influence of BCPL on C proceeded indirectly through the language B, which was written by Ken Thompson in 1970 for the first UNIX system.

Shortly before I was born, Dennis Ritchie wrote a paper [*The Development of the C language*][c_dev].
It goes into a lot more detail about the languages that preceded C, the development of Unix, and the culture at Bell Labs.
He describes B as the "parent" of C, and BCPL as the "grandparent".

B isn't quite the same as C, but you can easily see the familial relation.
Here's one paragraph that caught my eye, as a reminder that programmers don't change that much:

> Other fiddles in the transition from BCPL to B were introduced as a matter of taste, and some remain controversial, for example the decision to use the single character `=` for assignment instead of `:=`.
> Similarly, B uses `/**/` to enclose comments, where BCPL uses `//`, to ignore text up to the end of the line.

If you have time, I recommend reading the whole paper.



<center>
  <svg viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg" width="50">
    <rect x="25" y="75" width="450" height="350" fill="rgba(0, 0, 0, 0)" stroke="#f0f0f0" stroke-width="30" rx="25"/>

    <path d="M120 170, L200 250, L120, 330" stroke-width="30" stroke="#f0f0f0" stroke-linecap="round" fill="rgba(0,0,0,0)"/>
    <path d="M250 330, L380 330" stroke-width="30" stroke="#f0f0f0" stroke-linecap="round" fill="rgba(0,0,0,0)"/>
  </svg>
</center>



## What comes before C? B

If B is the predecessor to C, did B have a `main` function?

There's no sample B program in *The Development of C*, but I did find [*A Tutorial Introduction to the Language B*][b_tutorial], published by Brian Kernighan in 1973 (five years before K&R, and when C was still fairly new).
This passage has the same vibe as C:

> All B programs consist of one or more "functions", which are similar to the functions and subroutines of a Fortran program, or the procedures of PL/I.
> `main` is such a function, and in fact all B programs must have a `main`.
> Execution of the program begins at the first statement of `main`, and usually ends at the last.

So it seems like C took the idea of `main` directly from B.
Where did B get the idea?



<center>
  <svg viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg" width="50">
    <rect x="25" y="75" width="450" height="350" fill="rgba(0, 0, 0, 0)" stroke="#f0f0f0" stroke-width="30" rx="25"/>

    <path d="M120 170, L200 250, L120, 330" stroke-width="30" stroke="#f0f0f0" stroke-linecap="round" fill="rgba(0,0,0,0)"/>
    <path d="M250 330, L380 330" stroke-width="30" stroke="#f0f0f0" stroke-linecap="round" fill="rgba(0,0,0,0)"/>
  </svg>
</center>



## Digression: before C and B comes… A?

There was no predecessor language A that came before B, but *The Development of C* does explain that A stands for assembler:

> Thompson's PDP-7 assembler outdid even DEC's in simplicity; it evaluated expressions and emitted the corresponding bits.
> There were no libraries, no loader or link editor: the entire source of a program was presented to the assembler, and the output file—with a fixed name—that emerged was directly executable.
> (This name, `a.out`, explains a bit of Unix etymology; it is the output of the assembler.
> Even after the system gained a linker and a means of specifying another name explicitly, it was retained as the default executable result of a compilation.)



<center>
  <svg viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg" width="50">
    <rect x="25" y="75" width="450" height="350" fill="rgba(0, 0, 0, 0)" stroke="#f0f0f0" stroke-width="30" rx="25"/>

    <path d="M120 170, L200 250, L120, 330" stroke-width="30" stroke="#f0f0f0" stroke-linecap="round" fill="rgba(0,0,0,0)"/>
    <path d="M250 330, L380 330" stroke-width="30" stroke="#f0f0f0" stroke-linecap="round" fill="rgba(0,0,0,0)"/>
  </svg>
</center>



## BCPL (a Before C Programming Language)

If BCPL is the predecessor to B, did BCPL have a `main` function?

The original version of BCPL was written by Martin Richards in 1967 at the University of Cambridge.
(If you went to Cambridge, you may be amused to know that he also wrote an operating system called [TRIPOS].)
The language is still being developed, so there are lots of different versions.

I found a BCPL reference manual [from 1967][bcpl_1967], and [another from 1974][bcpl_1974] (lovely cover art).
I haven't read them end-to-end, but I had a quick skim, and I couldn't see a mention of anything like `main` function.
The 1974 manual does have a function `Start`, but I'm not sure that's the same as `main`.

Another [manual from 1979][bcpl_1979] has a sample program in section 2.2 with a procedure called `Main`, but I couldn't find the bit of the manual that explains why this procedure is special.
(The perils of scanned PDFs without OCR.)

```
let Main() be
  [main
        // Initialize the global vectors
        ...
  ]main
```

1979 is after the publication of K&R, so it's possible the name `main` has floated back from C.

Finally, the [most recent BCPL manual][bcpl_2020], updated March this year, includes a function called `start` which sounds very similar to `main`:

> **start**.
> This is global 1 and is, by convention, the main function of a program.
> It is the first user function to be called when a program is run by the Command Language Interpreter.

Here's one of the example programs in BCPL using this function like C uses `main`:

```
GET "libhdr"
LET start() = VALOF
{ writef("Hello*n")
  RESULTIS 0
}
```

So maybe BCPL came up with this idea, or maybe it came back from C -- I'm not sure.

[bcpl_1967]: https://www.bell-labs.com/usr/dmr/www/bcpl.html
[bcpl_1974]: http://www.bitsavers.org/pdf/bbn/tenex/TenexBCPL_1974.pdf
[bcpl_1979]: http://bitsavers.org/pdf/xerox/alto/bcpl/AltoBCPLdoc.pdf
[bcpl_2020]: https://www.cl.cam.ac.uk/~mr10/bcplman.pdf



<center>
  <svg viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg" width="50">
    <rect x="25" y="75" width="450" height="350" fill="rgba(0, 0, 0, 0)" stroke="#f0f0f0" stroke-width="30" rx="25"/>

    <path d="M120 170, L200 250, L120, 330" stroke-width="30" stroke="#f0f0f0" stroke-linecap="round" fill="rgba(0,0,0,0)"/>
    <path d="M250 330, L380 330" stroke-width="30" stroke="#f0f0f0" stroke-linecap="round" fill="rgba(0,0,0,0)"/>
  </svg>
</center>



## Digression: Where did "hello world" come from?

Like everything else in programming, somebody had to invent "hello world".
K&R helped make it popular, but where did it come from?

The B tutorial includes some sample programs, including this earlier version of "hello world":

```
main( ) {
  extrn a, b, c;
  putchar(a); putchar(b); putchar(c); putchar('!*n');
}

a 'hell';
b 'o, w';
c 'orld';
```

(Note that unlike C, B uses the asterisk instead of a backslash for escape characters.
Compare `\n` and `*n`.
I've heard this is because B was written on a machine whose keyboard didn't have a backslash, but I can't find a reference for that.)

I'm less clear on whether the idea started with B, or whether it came from BCPL.
The [Jargon File entry for BCPL][jargon] says:

> BCPL was the language in which the original hello world program was written

but the claim is unreferenced.
I found a [Stack Overflow answer][so_bcpl] that supports this claim, then I found [another blog post][medium_hw] that refutes it, both authors claiming to have emailed Brian Kernighan and received different answers.

So I'm still confused on this one.



<center>
  <svg viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg" width="50">
    <rect x="25" y="75" width="450" height="350" fill="rgba(0, 0, 0, 0)" stroke="#f0f0f0" stroke-width="30" rx="25"/>

    <path d="M120 170, L200 250, L120, 330" stroke-width="30" stroke="#f0f0f0" stroke-linecap="round" fill="rgba(0,0,0,0)"/>
    <path d="M250 330, L380 330" stroke-width="30" stroke="#f0f0f0" stroke-linecap="round" fill="rgba(0,0,0,0)"/>
  </svg>
</center>



## Digression: octal numbers

In the B tutorial, I chuckled at a reference to the use of leading 0 to represent [octal numbers][octal].
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

One octal digit is equivalent to three binary digits, so octal was [used in computing][octal] when systems used words whose length was divisible by three: 6-, 12-, 24-, and 36-bit words were common.
These days, computers use word lengths that are powers of 2: 16-, 32-, and 64-bits words, and we use hexadecimal instead of octal (one hexadecimal digit is four binary digits).
Indeed, octal has fallen so out of fashion that some languages have [removed the leading 0 for octal numbers][pep_3127].



<center>
  <svg viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg" width="50">
    <rect x="25" y="75" width="450" height="350" fill="rgba(0, 0, 0, 0)" stroke="#f0f0f0" stroke-width="30" rx="25"/>

    <path d="M120 170, L200 250, L120, 330" stroke-width="30" stroke="#f0f0f0" stroke-linecap="round" fill="rgba(0,0,0,0)"/>
    <path d="M250 330, L380 330" stroke-width="30" stroke="#f0f0f0" stroke-linecap="round" fill="rgba(0,0,0,0)"/>
  </svg>
</center>




## Digression: a world of no `return`

Today pretty much every language uses `return` to exit a function, optionally passing a value back to the caller -- but the 1979 BCPL reference suggests another approach.

In section 3.6 "Procedure declarations", it makes the following distinction:

> There are two kinds of BCPL procedures: "functions", which return a value upon completion, and "routines", which do not.

Further down, in section 5.6 "Returns", there are different statements depending on whether you're in a function or a routine:

> return <br/>
> resultis EXP
>
> These statements cause a return from the procedure in which they appear.
> "return" is only legal in a routine body; "resultis EXP" is only legal in a function body.

By the time B came around, the two statements had been collapsed into one: `return` was used whether or not the procedure passed a value back to the caller.

I wonder if there's an alternative timeline where we kept both statements?



<center>
  <svg viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg" width="50">
    <rect x="25" y="75" width="450" height="350" fill="rgba(0, 0, 0, 0)" stroke="#f0f0f0" stroke-width="30" rx="25"/>

    <path d="M120 170, L200 250, L120, 330" stroke-width="30" stroke="#f0f0f0" stroke-linecap="round" fill="rgba(0,0,0,0)"/>
    <path d="M250 330, L380 330" stroke-width="30" stroke="#f0f0f0" stroke-linecap="round" fill="rgba(0,0,0,0)"/>
  </svg>
</center>



## Back to the `main` problem

Modern languages get their `main()` function from C.
That in turn came from B, and possibly some version of it came from BCPL.

I did try to dig back further, into languages like FORTRAN, COBOL and Algol, all of which predate BCPL and B, and were cited as influences.
I couldn't find anything definitive about a main-like function in those languages, but I did find phrases like *"main procedure"* and *"main program"*.
Even if B was the first language to use this as a function name, "main" goes back further.

I found a page of [historical documents in computer science][historical], with lots of manuals which might have more clues, but I haven't read any of them yet.

I hope you found some of this history interesting.
I don't know if I'll spend more time on this question, but if somebody else has a better answer [please let me know](/#contact).
I'm sure somebody must know where `main()` came from, even if I don't.

[pymain]: https://utcc.utoronto.ca/~cks/space/blog/python/WhyNoMainFunction
[c_wiki]: https://en.wikipedia.org/wiki/C_(programming_language)#History
[k_and_r]: https://en.wikipedia.org/wiki/C_(programming_language)#K&R_C
[auction]: https://www.artsy.net/artwork/brian-kernighan-hello-world
[c_dev]: https://www.bell-labs.com/usr/dmr/www/chist.html
[b_tutorial]: https://www.bell-labs.com/usr/dmr/www/btut.html
[octal]: https://en.wikipedia.org/wiki/Octal
[py_octal]: https://www.python.org/dev/peps/pep-3127/
[bcpl_wiki]: https://en.wikipedia.org/wiki/BCPL
[responsible]: https://docs.python-guide.org/writing/style/#we-are-all-responsible-users
[historical]: http://web.eah-jena.de/~kleine/history/
[hello_world]: https://en.wikipedia.org/wiki/%22Hello,_World!%22_program
[jargon]: http://www.catb.org/jargon/html/B/BCPL.html
[so_bcpl]: https://stackoverflow.com/a/12785204/1558022
[medium_hw]: https://medium.com/@ozanerhansha/on-the-origin-of-hello-world-61bfe98196d5
[TRIPOS]: https://en.wikipedia.org/wiki/TRIPOS
[octal]: https://en.wikipedia.org/wiki/Octal#In_computers
[pep_3127]: https://www.python.org/dev/peps/pep-3127/


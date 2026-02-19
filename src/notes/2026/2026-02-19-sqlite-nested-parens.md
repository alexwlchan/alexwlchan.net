---
layout: note
title: The SQLite command line shell will show the level of parentheses
summary: Prefixes like `(x1` or `(x2` tell you if you're in the middle of some unclosed parentheses.
date: 2026-02-19 21:05:41 +00:00
topic: SQLite
---
While writing [my previous note][sqlite-triggers], I noticed an unexpected prefix in the SQLite shell:

<pre class="lng-sqlite3"><code><span class="gp">sqlite&gt;</span><span class="w"> </span>CREATE TABLE KeyValuePairs <span class="p">(</span>
<span class="gp">(x1...&gt;</span><span class="w"> </span>    Key   TEXT NOT NULL PRIMARY KEY,
<span class="gp">(x1...&gt;</span><span class="w"> </span>    Value TEXT NOT NULL
<span class="gp">(x1...&gt;</span><span class="w"> </span><span class="p">);</span></code></pre>

What does that `(x1` prefix mean?
I couldn't find any reference to it online, so I had to read the [SQLite source code][sqlite-src].

The relevant code is in `shell.c.in`.
First I found the default prompts, and two variables where the main and continuation prompts are stored:

```c {"names":{"1":"PROMPT_LEN_MAX","2":"mainPrompt","4":"continuePrompt"},"line_numbers":"406-414","caption":"Lines 406–414 of <code>src/shell.c.in</code> at <a href='https://sqlite.org/src/info?name=15285c21cc3f1da9289b0b6c5fd0b2ca8ab2e664b4b300c404afe7634ce9876f&ln=406-414'><code>15285c21cc</code></a>"}
/*
** Prompt strings. Initialized in main. Settable with
**   .prompt main continue
*/
#define PROMPT_LEN_MAX 128
/* First line prompt.   default: "sqlite> " */
static char mainPrompt[PROMPT_LEN_MAX];
/* Continuation prompt. default: "   ...> " */
static char continuePrompt[PROMPT_LEN_MAX];
```

Looking at where those variables get used leads to another interesting snippet, which names this feature as "dynamic continuation prompt":

```c {"names":{"2":"CONTINUATION_PROMPT","4":"CONTINUATION_PROMPT"},"line_numbers":"444-452,…,460-461","caption":"Lines 444–461 of <code>src/shell.c.in</code> at <a href='https://sqlite.org/src/info?name=15285c21cc3f1da9289b0b6c5fd0b2ca8ab2e664b4b300c404afe7634ce9876f&ln=444-461'><code>15285c21cc</code></a>"}
/*
** Optionally disable dynamic continuation prompt.
** Unless disabled, the continuation prompt shows open SQL lexemes if any,
** or open parentheses level if non-zero, or continuation prompt as set.
** This facility interacts with the scanner and process_input() where the
** below 5 macros are used.
*/
#ifdef SQLITE_OMIT_DYNAPROMPT
# define CONTINUATION_PROMPT continuePrompt
…
#else
# define CONTINUATION_PROMPT dynamicContinuePrompt()
```

And looking for the definition of that `dynamicContinuePrompt` function, I can see it updating a `dynPrompt.dynamicPrompt` variable with expressions like the `(x1` I saw in my SQLite shell:

```c {"names":{"1":"dynamicContinuePrompt","10":"ncp","13":"ndp"},"line_numbers":"499-528","caption":"Lines 499–528 of <code>src/shell.c.in</code> at <a href='https://sqlite.org/src/info?name=15285c21cc3f1da9289b0b6c5fd0b2ca8ab2e664b4b300c404afe7634ce9876f&ln=499-528'><code>15285c21cc</code></a>"}
/* Upon demand, derive the continuation prompt to display. */
static char *dynamicContinuePrompt(void){
  if( continuePrompt[0]==0
      || (dynPrompt.zScannerAwaits==0 && dynPrompt.inParenLevel == 0) ){
    return continuePrompt;
  }else{
    if( dynPrompt.zScannerAwaits ){
      size_t ncp = strlen(continuePrompt);
      size_t ndp = strlen(dynPrompt.zScannerAwaits);
      if( ndp > ncp-3 ) return continuePrompt;
      shell_strcpy(dynPrompt.dynamicPrompt, dynPrompt.zScannerAwaits);
      while( ndp<3 ) dynPrompt.dynamicPrompt[ndp++] = ' ';
      shell_strncpy(dynPrompt.dynamicPrompt+3, continuePrompt+3,
              PROMPT_LEN_MAX-4);
    }else{
      if( dynPrompt.inParenLevel>9 ){
        shell_strncpy(dynPrompt.dynamicPrompt, "(..", 4);
      }else if( dynPrompt.inParenLevel<0 ){
        shell_strncpy(dynPrompt.dynamicPrompt, ")x!", 4);
      }else{
        shell_strncpy(dynPrompt.dynamicPrompt, "(x.", 4);
        dynPrompt.dynamicPrompt[2] = (char)('0'+dynPrompt.inParenLevel);
      }
      shell_strncpy(dynPrompt.dynamicPrompt+3, continuePrompt+3,
                    PROMPT_LEN_MAX-4);
    }
  }
  return dynPrompt.dynamicPrompt;
}
#endif /* !defined(SQLITE_OMIT_DYNAPROMPT) */
```

I don't completely understand this function, but I think I get the general gist.
The first branch is looking for "open SQL lexemes", or unterminated strings, while the second branch is counting open parentheses.
I can compare this to what I see in the SQLite shell:

<ul>
<li>If you have between 1 to 9 unclosed parentheses, the prompt starts with <code>(x</code> and the number of unclosed parens:
<pre class="lng-sqlite3"><code><span class="gp">sqlite&gt;</span><span class="w"> </span><span class="p">(</span>
<span class="gp">(x1...&gt;</span>
<span class="gp">sqlite&gt;</span><span class="w"> </span><span class="p">(((((((((</span>
<span class="gp">(x9...&gt;</span></code></pre>
</li>
<li>If you have 10 or more unclosed parentheses, the prompt starts with prints <code>(..</code>:
<pre class="lng-sqlite3"><code><span class="gp">sqlite&gt;</span><span class="w"> </span><span class="p">((((((((((</span>
<span class="gp">(x.....&gt;</span></code></pre>
</li>
<li>
<p>If you have more closed parentheses than you've opened, the prompt starts with prints <code>)x!</code>:</p>
<pre class="lng-sqlite3"><code><span class="gp">sqlite&gt;</span><span class="w"> </span><span class="p">)))</span>
<span class="gp">)x!...&gt;</span></code></pre>
</li>
<p>If you’re in this state, I’m not sure if it's ever possible to get back to a valid SQL expression?</p>
<li><p>If you have an unfinished string, square bracket, or <a href="https://sqlite.org/lang_comment.html">multi-line comment</a>, the prompt starts with the quote character you need to close the string:</p>
<pre class="lng-sqlite3"><code><span class="gp">sqlite&gt;</span><span class="w"> </span>SELECT '
<span class="gp">'  ...&gt;</span><span class="w"> </span>hello world
<span class="gp">'  ...&gt;</span><span class="w"> </span>'
<span class="go"></span>
<span class="go">hello world</span>
<span class="go"></span>
<span class="gp">sqlite&gt;</span><span class="w"> </span>SELECT "
<span class="gp">"  ...&gt;</span><span class="w"> </span>hello world
<span class="gp">"  ...&gt;</span><span class="w"> </span>"
<span class="go"></span>
<span class="go">hello world</span>
<span class="go"></span>
<span class="gp">sqlite&gt;</span><span class="w"> </span>[
<span class="gp">[  ...&gt;</span><span class="w"> </span>

<span class="gp">sqlite&gt;</span><span class="w"> </span>/*
<span class="gp">/* ...&gt;</span><span class="w"> </span>
</code></pre>
</li>
</ul>

I wonder where this behaviour came from?
It feels like the sort of thing that might have come from Lisp, which is famous for having lots of brackets and exactly where this sort of indicator might be useful, whereas I imagine writing a heavily nested expression in the SQLite shell interface is comparatively rare.

[sqlite-src]: https://sqlite.org/src/dir?ci=trunk
[sqlite-triggers]: /notes/2026/sqlite-triggers-to-catch-errors/

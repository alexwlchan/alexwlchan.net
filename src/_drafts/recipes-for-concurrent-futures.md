---
layout: post
title: Python recipes for concurrent.futures
summary: Some examples of how I've been using concurrent.futures to speed up my batch scripting in Python.
category: Python
---

I use a lot of Python for scripting, and in particular to script repetitive tasks.
A lot of my scripts are some variant on the following pattern:

```python
for task in get_tasks_to_do():
    perform(task)
```

This is a *sequential* programming pattern -- the tasks run one after another, with only one task running at a time.
It keeps the code simple, and because it's only ever doing one task at a time, it's easy to follow the script as it's running.
It starts task 1, then task 2, then task 3, and so on.

This is fine when the tasks are few or fast, but if if I have lots of slow tasks, the overall script is very slow.

I've written a lot of scripts recently where the tasks are slow -- for example, making HTTP requests -- and I want to run more than one task at once.
Each task spends a lot of time waiting for an external resource -- say, a response from a distant server -- and that time could be spent doing something more useful, like starting the next request.
This is a [*concurrent* programming pattern][concurrent].

[concurrent]: https://en.wikipedia.org/wiki/Concurrent_computing

Concurrent programming trades simplicity for speed.
The code gets more complicated, and there are more ways for it to go wrong, but it's usually faster.
It's not better or worse than sequential programming; it's just a different set of tradeoffs.

I've been experimenting with Python's [concurrent.futures module][confut] as a way to introduce concurrency into my scripts.
In this post, I'm going to show off some of the patterns I've been using -- both so you can use them, and to help me understand them better.

[confut]: https://docs.python.org/3/library/concurrent.futures.html

(This post started as a discussion of a single problem: listing all the rows in a DynamoDB table.
The concurrency was a key part of the script, and I realised it was worth digging into that aspect on its own.)



## Running a small, fixed number of tasks

If I have a small number of tasks, I submit them all in one go, and wait for them all to complete.
Here's a simple example:

```python
import concurrent.futures


with concurrent.futures.Executor() as executor:
    futures = {
        executor.submit(perform, task)
        for task in get_tasks_to_do()
    }

    for fut in concurrent.futures.as_completed(futures):
        print(f"The outcome is {fut.result()}")
```

We start by creating an Executor.
Using the `with` statement creates a *context manager*, which ensures any stray threads or processes get cleaned up properly when we're done.

In real code, this would be a ThreadPoolExecutor or a ProcessPoolExecutor -- I've been using ThreadPoolExecutor without any arguments, because that's been fast enough for my scripts, and I don't understand the difference.
But if you want to squeeze the performance of your scripts, you can probably do some fine-tuning here.

Then I use a set comprehension to start all the tasks, using `executor.submit` to schedule each task.
This creates a Future object, which represents the task to be done.

Once all the tasks have been scheduled, I call [`concurrent.futures_as_completed`][as_completed], which yields the futures as they're done -- that is, as each task completes.
The `.result()` method gives me the return value of `perform(task)`, or throws an exception if it failed.

[as_completed]: https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.as_completed

The Future object doesn't hold any context, so if you want to match the results to the original task, you need to track that yourself:

```python
import concurrent.futures


with concurrent.futures.Executor() as executor:
    futures = {
        executor.submit(perform, task): task
        for task in get_tasks_to_do()
    }

    for fut in concurrent.futures.as_completed(futures):
        original_task = futures[fut]
        print(f"The outcome of {original_task} is {fut.result()}")
```

Rather than creating a set, we're creating a dict that maps each Future to its original task.
When the Future completes, we look in the dict to find the task.

There's a concrete example of this pattern [in the Python docs][docs].

[docs]: https://docs.python.org/3/library/concurrent.futures.html?highlight=concurrent.futures#threadpoolexecutor-example

This approach gets all the tasks at once, and creates a Future for each of them.
That's fine if you have a small number of tasks, but if you have lots of tasks it means you're using lots of memory, and at some point your program might just crash.
If we have a lot of tasks, we want to limit how many we're working on at a time.



## Running a large, fixed number of tasks

Often my tasks come from a lazy generator, because lazy generators are more memory efficient if you're only processing one thing at a time.
The pattern above loads all the tasks immediately, potentially using a lot of memory.
It would be nicer if it was only keeping a small number of tasks in memory -- the ones that were currently being worked on.

One approach to handle a very large number of tasks would be to [break them into small chunks](/2018/12/iterating-in-fixed-size-chunks/), and process each of them in turn using the pattern above.
We could do something like:

```python
for task_chunk in chunked_iterable(get_tasks_to_do(), HOW_MANY_TASKS_AT_ONCE):
    with concurrent.futures.Executor() as executor:
        futures = {
            executor.submit(perform, task)
            for task in task_chunk
        }

        for fut in concurrent.futures.as_completed(futures):
            print(f"The outcome is {fut.result()}")
```

This code is simple, but we're losing some of the efficiency gains -- it queues up N pieces of work, gets through them all, then loads another N pieces of work.
When it's near the end of a chunk, it's only processing a few pieces of work at once.

This graph shows the number of tasks available to the executor against time -- you can see when each chunk starts and ends.
We're getting some of the benefits of concurrency, but we could be doing better.

<svg viewBox="0 0 900 320" xmlns="http://www.w3.org/2000/svg"
     role="img" aria-label="A graph showing time on the horizontal axis, tasks in progress on the vertical axis.  There is a red area, showing an inverse sawtooth curve -- it rises sharply, drops gradually to zero, then repeats.">
  <marker id="arrowhead" markerWidth="8" markerHeight="5.6" refX="0" refY="2.8" orient="auto">
    <polygon fill="#000" points="0 0, 8 2.8, 0 5.6"/>
  </marker>

  <polygon points="75,300 100,100 300,300 325,100 525,300 550,100 750,300" style="fill: #d01c11" />

  <line x1="75"
        x2="800"
        y1="300"
        y2="300"
        stroke-width="3"
        stroke="black"
        marker-end="url(#arrowhead)" />

  <text x="860"
        y="300"
        text-anchor="middle"
        dominant-baseline="middle"
        font-size="20px">time</text>

  <!-- y-axis -->
  <line x1="75"
        x2="75"
        y1="300"
        y2="80"
        stroke-width="3"
        stroke="black"
        marker-end="url(#arrowhead)" />

  <text x="75"
        y="11"
        text-anchor="middle"
        dominant-baseline="middle"
        font-size="20px">tasks in</text>
  <text x="75"
        y="38"
        text-anchor="middle"
        dominant-baseline="middle"
        font-size="20px">the pool</text>
</svg>

It would be better if we could keep the pool "topped up" -- as one task finishes, we generate and schedule the next one.

If we have an iterable of Futures, we can find ones that have already completed with [`concurrent.futures.wait()`][wait]:

[wait]: https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.wait

```python
done, not_done = concurrent.futures.wait(
    futures, return_when=concurrent.futures.FIRST_COMPLETED
)
```

We can choose to wait for the first Future to complete, to throw an exception, or for everything to complete (which is equivalent to `as_completed`).

Here's what it looks like:

```python
import concurrent.futures
import itertools


tasks_to_do = get_tasks_to_do()

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = {
        executor.submit(perform, task)
        for task in itertools.islice(tasks_to_do, HOW_MANY_TASKS_AT_ONCE)
    }

    while futures:
        done, futures = concurrent.futures.wait(
            futures, return_when=concurrent.futures.FIRST_COMPLETED
        )

        for fut in done:
            print(f"The outcome is {fut.result()}")

        for task in itertools.islice(tasks_to_do, len(done)):
            futures.add(
                executor.submit(perform, task)
            )
```

A lot of heavy lifting is being done by [`itertools.islice(iterable, N)`][islice], which generates the first *N* elements of an iterable (or the whole thing, if there are less than *N* elements left).

We start by scheduling the initial batch of futures, then loop as long as there are uncompleted futures.
When a future completes, we split the set into `done` or `futures` (the new set of uncompleted futures).

We process the completed futures (`for fut in done:`), then schedule an equivalent number of new futures.
This way, the executor always has plenty of tasks to do, and we're making efficient use of the concurrency.
This is what the number of tasks available looks like:

[islice]: https://docs.python.org/3/library/itertools.html#itertools.islice

<svg viewBox="0 0 900 320" xmlns="http://www.w3.org/2000/svg"
     role="img" aria-label="A graph showing time on the horizontal axis, tasks in progress on the vertical axis.  There is a red area, showing an initial spike to the top, then a zigzag pattern, then declining back to zero.">
  <marker id="arrowhead" markerWidth="8" markerHeight="5.6" refX="0" refY="2.8" orient="auto">
    <polygon fill="#000" points="0 0, 8 2.8, 0 5.6"/>
  </marker>

  <polygon points="75,300 100,100 125,125 128.125,100 153.125,125 156.25,100 181.25,125 184.375,100 209.375,125 212.5,100 237.5,125 240.625,100 265.625,125 268.75,100 293.75,125 296.875,100 321.875,125 325.0,100 350.0,125 353.125,100 378.125,125 381.25,100 406.25,125 409.375,100 434.375,125 437.5,100 462.5,125 465.625,100 665.625,300" style="fill: #d01c11" />

  <line x1="75"
        x2="800"
        y1="300"
        y2="300"
        stroke-width="3"
        stroke="black"
        marker-end="url(#arrowhead)" />

  <text x="860"
        y="300"
        text-anchor="middle"
        dominant-baseline="middle"
        font-size="20px">time</text>

  <!-- y-axis -->
  <line x1="75"
        x2="75"
        y1="300"
        y2="80"
        stroke-width="3"
        stroke="black"
        marker-end="url(#arrowhead)" />

  <text x="75"
        y="11"
        text-anchor="middle"
        dominant-baseline="middle"
        font-size="20px">tasks in</text>
  <text x="75"
        y="38"
        text-anchor="middle"
        dominant-baseline="middle"
        font-size="20px">the pool</text>
</svg>

The pool is kept topped up with new tasks to start, until we run out of tasks and it gradually shrinks back to zero.
In practice, the exact shape will be less regular, but it gives the general idea.

This pattern makes it a little harder to track the task a future was associated with, because `concurrenct.futures.wait()` always returns a set, regardless of what iterable was passed in.
But it's still possible, like so:

```python
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = {
        executor.submit(perform, task): task
        for task in itertools.islice(tasks_to_do, HOW_MANY_TASKS_AT_ONCE)
    }

    while futures:
        done, _ = concurrent.futures.wait(
            futures, return_when=concurrent.futures.FIRST_COMPLETED
        )

        for fut in done:
            original_task = futures.pop(fut)
            print(f"The outcome of {original_task} is {fut.result()}")

        for task in itertools.islice(tasks_to_do, len(done)):
            fut = executor.submit(perform, task)
            futures[fut] = task
```

As before, we're storing the context in a dict `futures`.
When a Future completes, we `.pop()` from the dict to delete the entry and retrieve the original task.
When we schedule a new task, we store it in the dict.
The `futures` dict still contains all the unfinished Futures, so we can continue to use it as a check for when the process is complete.



## Running tasks that might have follow-up work

This is the problem I was originally trying to solve -- I'd schedule some Futures based on initial tasks, but then the result of those Futures might uncover more tasks.

For example, the DynamoDB Scan API is paginated.
You don't know where the page boundaries are in advance -- each response tells you how to request the next page.
When you get page 1, that tells you how to request page 2.
When you get page 2, that tells you how to request page 3, and so on.
This means you can only schedule a task to request page 2 after you've received page 1.

When I first tried to do this, I kept having problems -- everything I scheduled in the initial batch would complete, but I'd never see the result of any new Futures that I'd scheduled.
I had to try a simpler problem (running large, fixed number of tasks) to learn about `concurrent.futures.wait()`, which can be used to solve this problem.

We can make a small modification to the `for fut in done:` loop in the example above:

```python
for fut in done:
    print(f"The outcome is {fut.result()}")

    if has_follow_up_task(fut.result()):
        new_task = get_follow_up_task(fut.result())
        futures.add(
            executor.submit(perform, new_task)
        )
```

If there's a follow-up task to run, it schedules that task as another Future.
It's now in the pool of running Futures, and it will get checked the next time we call `concurrent.futures.wait()`.
(In theory you could schedule multiple new tasks here, but be careful -- if you create too many, you could trigger a [fork bomb][forkbomb].)

Eventually your process should stop scheduling new futures, or it'll get stuck in an [infinite loop][infiniloop] and never terminate.

[forkbomb]: https://en.wikipedia.org/wiki/Fork_bomb
[infiniloop]: https://en.wikipedia.org/wiki/Infinite_loop

If there's a follow-up task, we also need to skip scheduling a task from the initial batch of tasks -- otherwise `futures`, the pool of currently running Futures, will increase in size.
Here's how that works:

```python
import concurrent.futures
import itertools


with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = {
        executor.submit(perform, task)
        for task in itertools.islice(tasks_to_do, HOW_MANY_TASKS_AT_ONCE)
    }

    while futures:
        done, futures = concurrent.futures.wait(
            futures, return_when=concurrent.futures.FIRST_COMPLETED
        )

        new_tasks_to_schedule = 0

        for fut in done:
            print(f"The outcome is {fut.result()}")

            if has_follow_up_task(fut.result()):
                new_task = get_follow_up_task(fut.result())
                futures.add(
                    executor.submit(perform, new_task)
                )
            else:
                new_tasks_to_schedule += 1

        for task in itertools.islice(tasks_to_do, new_tasks_to_schedule):
            futures.add(
                executor.submit(perform, task)
            )
```

And we can also use a dict to track the task a future was started from:

```python
import concurrent.futures
import itertools


with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = {
        executor.submit(perform, task): task
        for task in itertools.islice(tasks_to_do, HOW_MANY_TASKS_AT_ONCE)
    }

    while futures:
        done, _ = concurrent.futures.wait(
            futures, return_when=concurrent.futures.FIRST_COMPLETED
        )

        new_tasks_to_schedule = 0

        for fut in done:
            original_task = futures.pop(fut)
            print(f"The outcome of {original_task} is {fut.result()}")

            if has_follow_up_task(fut.result()):
                new_task = get_follow_up_task(fut.result())
                fut = executor.submit(perform, new_task)
                futures[fut] = new_task
            else:
                new_tasks_to_schedule += 1

        for task in itertools.islice(tasks_to_do, new_tasks_to_schedule):
            fut = executor.submit(perform, task)
            futures[fut] = task
```



## Using this code

When I want to use this code, I copy/paste it into my newest script, and fill in the parts that have changed.
If you'd like to try the code, you can do the same!

Most of my scripts are only ever intended to run on one machine, so I optimise for runtime on that computer.
I experiment with ThreadPoolExecutor and ProcessPoolExecutor and the max_workers variable until I get something that's fast enough.
It isn't necessarily optimal -- it's just fast enough that it's not worth fiddling any further.
Getting a script from 5&nbsp;minutes to 30&nbsp;seconds is pretty good.
Saving another 5–10 seconds is diminshing returns.

Now I have these templates and a write-up, I hope I'll be able to use it much more.
As well as being easy to find, I'm more confident that I understand how the code works, and where the rough edges are.
Once again, a detailed walkthrough of code is as useful as me as for the reader.

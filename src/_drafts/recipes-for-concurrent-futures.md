---
layout: post
title: Three Python recipes for concurrent.futures
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

Once all the tasks have been scheduled, I call `concurrent.futures_as_completed`, which yields the futures as they're done -- that is, as each task completes.
The `.result()` method gives me the return value of `perform(task)`, or throws an exception if it failed.

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

## Running tasks that might have follow-up work

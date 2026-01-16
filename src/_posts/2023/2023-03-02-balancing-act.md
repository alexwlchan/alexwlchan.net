---
layout: post
date: 2023-03-02 14:03:08 +00:00
title: Splitting a class into balanced groups
summary: How do you make sure everyone gets to work with everyone else?
tags:
  - combinatorics
  - python
colors:
  index_light: "#8c3526"
  index_dark:  "#d7a59d"
---

Earlier this week, my mum sent me an interesting problem.

She's got a class of 12 students, who are going to meet over 7 sessions.
In each session, they're going to split into 3 or 4 groups, and she wants to find an even distribution of groups -- each person gets to work with every other person in the class at least once, and avoid any extremes like two people being in the same group every time.
It feels like a good solution should exist, but trying to write it out manually gets quite tricky -- could I write some code to do it?

Let's give it a go.

---

Whenever I'm faced with a problem like this, my initial thought is "can I just try every possibility?"
Even a "slow" computer can crunch through [a lot of examples][floats] pretty quickly, and this saves me from having to think of any clever way to select the "good" combinations.

Unfortunately there are way too many combinations to sensibly test -- I don't have an exact number, but my rough napkin scribbles suggest there are something like 1e30 combinations of groups across the 7 sessions.
(Getting an exact number would be a bit fiddly and I didn't bother trying; the important thing is that it's Very Big.)

I started by writing a program that would shuffle the groups randomly in each session -- but that didn't give very good results.
Usually there'd be a few people who never worked together, and a few who worked together lots of times, which is what we're trying to prevent.

I was a bit stumped at this point, because I couldn't see how to find the "best" solution -- and I couldn't find anybody else who'd solved the problem when I searched Google.
(I'm sure somebody has, but I'm not using the right search terms.)

But I don't need to find the "best" solution, I just need to find a "good enough" solution.
That seems much easier.

[floats]: https://randomascii.wordpress.com/2014/01/27/theres-only-four-billion-floatsso-test-them-all/

---

I started by coming up with a list of student names.

```python
students = {
    "Alice", "Bryony", "Caroline", "Danielle", "Emma", "Faith",
    "Gabrielle", "Helen", "Imogen", "Julia", "Katie", "Lily",
}
```

I didn't need to do this – it would be quicker to use `student1`, `student2`, …, `student12` – but I find names helpful for this sort of problem.
I often end up working through examples by hand, and it's easier for me to think about distinct named entities than a collection of near-identical numbers.

In a similar vein, I avoid variable names that are a single character apart, say `student`/`students`.
I'll try to go for something more visually distinct, like `s`/`students` or `student`/`all_students`.
Otherwise, it's easy for me to mix them up.

Then I came up with a data structure to count how many times any two students have worked together:

```python
pairs = {
    s: {other_s: 0 for other_s in students if other_s != s}
    for s in students
}

# {
#   'Alice': {'Bryony': 0, 'Caroline': 0, 'Danielle': 0, …},
#   'Bryony': {'Alice': 0, 'Caroline': 0, …},
#   …
# }
```

We'll update this as we assign students to various groups.

The keys of this dictionary are the names of each student, and the values count how many times this student has worked with other students.
For example, to see how many times Lily and Katie have been in the same group:

```python
pairs['Lily']['Katie']
```

This is a bit inefficient, because the same value is also available in `pairs['Katie']['Lily']` -- we'll have to remember to update it in both places.
If this was a bigger project, I might create a custom data structure to handle this properly, but it's overkill for a simple problem.

After this, I came up with a way to assign the groups.
This approach was my first idea, which turned out to work pretty well:

```python
for i in range(1, session_count + 1):
    print(f"# Session {i}")

    group_size = random.choice([3, 4])

    # These variables track how the students are grouped.
    #
    # We're going to assign the groups one-by-one; the `groups` variable
    # tracks all the groups that we've assigned, and `next_group` tracks
    # the group we're currently assigning.
    groups = []
    next_group = []

    # Which students aren't in a group yet?
    remaining_students = {s for s in students}

    while remaining_students:
        # If there aren't any students in the next group yet, pick one
        # randomly from the pool of remaining students.
        if next_group == []:
            next_student = random.choice(list(remaining_students))

        else:
            # For each remaining student, count how many times they've worked
            # with everyone already in `next_group`.
            previous_pairings = {
                s: sum(pairs[student_in_group][s] for student_in_group in next_group)
                for s in remaining_students
            }

            # Pick the student who's worked with everyone in this group the
            # least number of times.
            next_student = min(remaining_students, key=lambda s: previous_pairings[s])

        # Add the next student to the group; remove them from the list of
        # students who haven't been assigned a group yet.
        remaining_students.remove(next_student)
        next_group.append(next_student)

        # If this group is big enough, save it and reset.
        if len(next_group) == group_size:

            # For each pair of students in this group, update the number
            # of times they've worked together.
            for (a, b) in itertools.combinations(next_group, 2):
                pairs[a][b] += 1
                pairs[b][a] += 1

            groups.append(next_group)
            next_group = []

    for g in groups:
        print(' '.join(sorted(g)))
```

In each session, it builds the groups one-by-one.

*   To start each group, it picks a random student who isn't in a group yet (say, Alice).

*   Then it looks at all the other students who aren't in a group yet, and counts how many times they've worked with Alice.
    It picks whoever has worked with Alice least often, and adds them to the group (say, Imogen).
    This prioritises students who've never worked with Alice before, and deprioritises students who've already worked with her several times.
    
*   It then repeats, counting how many times each of the other students has worked with Alice *or* Imogen.
    It picks the student who's worked with them least often, and adds them to the group.

*   It keeps doing this until the group is big enough, then it moves on to the next group.

It also updates the counts in the `pairs` dictionary, which will be used to pick groups in the next session.
This is using [itertools.combinations(<em>iterable</em>, r=2)](https://docs.python.org/3/library/itertools.html?highlight=itertools%20combinations#itertools.combinations), which is a quick and easy way to find all the pairs in a collection.

This is what the output looks like:

```
# Session 1
Alice Bryony Emma Faith
Caroline Danielle Imogen Julia
Gabrielle Helen Katie Lily

# Session 2
Alice Caroline Katie
Emma Gabrielle Julia
Faith Helen Imogen
Bryony Danielle Lily
```

This is a [greedy algorithm], and those are rarely optimal -- in this case, there are no constraints on the last group of "leftovers".
The other groups were all chosen to be made up of people who hadn't worked together much in the past, but we don't know anything about the last group.
It's possible that group could be made up entirely of people who've worked together before.

To help me see how good a solution it had come up with, I wrote another snippet to pretty-print the contents of the `pairs` data:

```python
longest_name = max(len(n) for n in students)

print(' ' * longest_name + ' A B C D E F G H I J K L')

for name in sorted(students):
    print(name.ljust(longest_name), end='')
    for s in sorted(students):
        if name == s:
            print(' ·', end='')
        else:
            print(f' {pairs[name][s]}', end='')
    print('')
```

Here's an example of the output:

```
          A B C D E F G H I J K L
Alice     · 2 2 2 2 1 1 2 2 2 2 2
Bryony    2 · 2 2 3 1 2 2 1 2 2 1
Caroline  2 2 · 2 2 1 3 2 1 2 1 2
Danielle  2 2 2 · 2 2 2 1 2 2 2 1
Emma      2 3 2 2 · 2 2 1 1 1 2 2
Faith     1 1 1 2 2 · 2 3 3 1 2 2
Gabrielle 1 2 3 2 2 2 · 2 2 2 0 2
Helen     2 2 2 1 1 3 2 · 1 3 1 2
Imogen    2 1 1 2 1 3 2 1 · 1 4 2
Julia     2 2 2 2 1 1 2 3 1 · 2 2
Katie     2 2 1 2 2 2 0 1 4 2 · 2
Lily      2 1 2 1 2 2 2 2 2 2 2 ·
```

We can see this particular solution isn't what we're looking for -- notice that Katie and Imogen have been in the same group three times, but Katie has never worked with Gabrielle.

I could probably fix this by tweaking the algorithm (hard), or I could run the script a few more times and see if I get a more balanced mix (easy).
Because the first member in each group is chosen randomly, running the script different times will get a different set of groups.

After a few more tries, I got a slightly better solution:

```
          A B C D E F G H I J K L
Alice     · 1 1 2 1 3 3 2 2 1 1 1
Bryony    1 · 3 2 1 1 2 1 2 1 2 2
Caroline  1 3 · 2 1 1 1 2 2 1 2 2
Danielle  2 2 2 · 1 2 1 2 1 1 2 2
Emma      1 1 1 1 · 2 2 1 2 3 2 2
Faith     3 1 1 2 2 · 2 2 1 2 1 1
Gabrielle 3 2 1 1 2 2 · 1 1 3 1 1
Helen     2 1 2 2 1 2 1 · 2 1 2 2
Imogen    2 2 2 1 2 1 1 2 · 2 2 1
Julia     1 1 1 1 3 2 3 1 2 · 1 2
Katie     1 2 2 2 2 1 1 2 2 1 · 2
Lily      1 2 2 2 2 1 1 2 1 2 2 ·
```

<!--
  # Round 1
  Caroline Danielle Helen Katie
  Alice Bryony Imogen Lily
  Emma Faith Gabrielle Julia

  # Round 2
  Bryony Gabrielle Katie
  Alice Danielle Emma
  Caroline Imogen Julia
  Faith Helen Lily

  # Round 3
  Alice Caroline Gabrielle
  Danielle Faith Imogen
  Emma Katie Lily
  Bryony Helen Julia

  # Round 4
  Bryony Caroline Emma Faith
  Alice Gabrielle Helen Imogen
  Danielle Julia Katie Lily

  # Round 5
  Bryony Danielle Gabrielle
  Caroline Helen Lily
  Alice Faith Katie
  Emma Imogen Julia

  # Round 6
  Bryony Caroline Imogen Katie
  Alice Danielle Faith Helen
  Emma Gabrielle Julia Lily

  # Round 7
  Bryony Caroline Danielle Lily
  Emma Helen Imogen Katie
  Alice Faith Gabrielle Julia
-->

I think this is about as good as you can do, so I sent this off to my mum, and she's going to use it in her class.
It'll likely need tweaking as people miss the occasional class and groups have to be rearranged, but it's a good starting point.

There are lots of ways this code could be made better, but I'm going to leave it as-is.
I needed it for a one-off question, I enjoyed doing it, and it got a good enough answer.
It strikes me that this might work as a question in a coding interview, a class of problems I usually don't enjoy, but knowing it had a practical purpose made this fun.

[greedy algorithm]: https://en.wikipedia.org/wiki/Greedy_algorithm

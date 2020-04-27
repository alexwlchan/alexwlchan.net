---
layout: post
date: 2020-04-27 09:23:04 +0000
title: Using DynamoDB as a calculator
summary: Taking advantage of Amazon's least-loved compute platform.
category: Amazon Web Services
---

On a recent [AWS Cost Optimisation Q&A](https://www.youtube.com/watch?t=52m01s&v=Nmyxo68jM2s), Corey Quinn talked about his experiments with [DynamoDB][dynamodb]:

> I've been diving deeper into Dynamo than I would expect.
> It's surprisingly awesome.
> I don't know much about databases, but I'm looking at it, and now I'm wondering: *"Dynamo's awesome, what can I misuse it as?"*
> S3 is my favourite message queue, Route&nbsp;53 is my favourite database, but I'm not entirely sure what's going on as far.
> As far as other creative uses, the things I could misuse.
> Maybe using Dynamo as a compute service -- I bet I can teach that thing to place chess.

DynamoDB is Amazon's hosted NoSQL service -- basically, a database.
It's a key-value store for holding large amounts of unstructured data.
We use DynamoDB for data storage at work, so I know a bit about using it, and I love taking <s>terrible</s> brilliant ideas and dialling them up to 11.

When you're learning to program, a common task is building a calculator: addition, subtraction, multiplication and division.
**This would be a good way to test Amazon's least-loved compute platform -- can we build a calculator on top of DynamoDB?**
It turns out we can, and that's what I'm going to walk through in this post.
(Extending this experiment to play chess is left as an exercise for the reader.)

[dynamodb]: https://en.wikipedia.org/wiki/Amazon_DynamoDB

For the avoidance of doubt: this is a Bad Idea&#8482;.
Do not use this code in production, or within a ten-mile radius of a production environment.
This is a satire post, not serious programming.

<figure>
  <img src="/images/2020/nuclear_waste_1x.jpg" srcset="/images/2020/nuclear_waste_1x.jpg 1x, /images/2020/nuclear_waste_2x.jpg 2x" alt="Yellow barrels with radiation warning signs lying in a field.">
  <figcaption>
    Wikimedia Commons says this is a protest against <a href="https://commons.wikimedia.org/wiki/File:WendlandAntiNuclearProtest7.jpg">German nuclear policy</a>, but it's actually a warning about using any of my ideas in production.
  </figcaption>
</figure>



<style>
  @media screen and (min-width: 500px) {
    img.operation {
      float: right;
      width: 300px;
      margin-top: -1.4em;
    }
  }

  @media screen and (max-width: 500px) {
    h2 {
      margin-bottom: 0.5em;
    }
  }

  h2 {
    margin-top: 5em;
  }
</style>



## Getting started

DynamoDB supports a wide variety of programming languages, including [Java](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Java.html), [.NET](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.NET.html) and [Python](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.html).
I'm going to use Python in this post, because that's what I'm familiar with, but these ideas can be used in other languages.

Within DynamoDB, we run all our computing inside *Table*.
Within a table, operations run within *Rows*.
Let's write some code to create a table for us, and to assign a row ID that we can use to track an individual calculation:

```python
import contextlib
import uuid

import boto3


dynamodb = boto3.resource("dynamodb")


class DynamoCalculator:
    """
    An integer calculator that uses DynamoDB for compute.
    """
    def __enter__(self):
        table_name = f"calculator-{uuid.uuid4()}"

        dynamodb.create_table(
            AttributeDefinitions=[{
                "AttributeName": "calculation_id",
                "AttributeType": "S",
            }],
            TableName=table_name,
            KeySchema=[{
                "AttributeName": "calculation_id",
                "KeyType": "HASH"
            }],
            BillingMode="PAY_PER_REQUEST"
        )

        self.table = dynamodb.Table(table_name)
        self.table.wait_until_exists()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.table.delete()
        self.table.wait_until_not_exists()

    @contextlib.contextmanager
    def row_id(self):
        calculation_id = str(uuid.uuid4())
        yield calculation_id
        self.table.delete_item(Key={"calculation_id": calculation_id})


with DynamoCalculator() as calculator:
    print(calculator)

    with calculator.row_id() as row_id:
        # do calculations with ``row_id``
        pass
```

The context manager handles creation *and* cleanup for us -- not only does it create a table for us, it deletes it afterwards.
This does create a bit of latency before you can do your first calculation, but it means we don't have tables hanging around in our account.

Remember: the expensive part of the cloud isn't what you use, it's what you forget to turn off.
This API ensures that we'll never forget to turn off our table!

> Serious point: **if you create resources that have cleanup that should always run, context managers are a great way to enforce this in a Python API.**
> Examples are sockets or files, which you should always close when you're done.
>
> In other languages, you use `try … except … finally`, but the caller has to remember to do the cleanup.
> Python has the `with` statement to hide this complexity from the caller.
> You've probably used one already -- `with open(…)`, which always closes the file once you're done using it, whether your code returned or threw an exception.
>
> If you're not using them, they're a powerful feature and worth learning.



<h2>Addition<img src="/images/2020/addition.png" alt="X + Y = ?" class="operation"></h2>

DynamoDB supports numbers as a first-class type, and we can read and write numeric values with the GetItem and PutItem APIs, respectively.
The PutItem API completely replaces the contents of a row, which is useful in some cases and easy to batch, but it's not always the right tool for the job.

Suppose we were using DynamoDB to store a counter.
We want to increment the value of the counter, but without reading the existing value from the table -- if another process updated the counter between the read and the write, we'd lose data.
For this, we can use the UpdateItem API, which can modify a row based on its existing values.

For example, we could tell it to add one number to another, like so:

```python
class DynamoCalculator:
    ...

    def add(self, x: int, y: int) -> int:
        """
        Adds two integers and returns the result.
        """
        with self.row_id() as calculation_id:
            self.table.put_item(
                Item={"calculation_id": calculation_id, "sum": x}
            )
            self.table.update_item(
                Key={"calculation_id": calculation_id},
                UpdateExpression="SET #sum = #sum + :y",
                ExpressionAttributeNames={"#sum": "sum"},
                ExpressionAttributeValues={":y": y}
            )
            resp = self.table.get_item(
                Key={"calculation_id": calculation_id}
            )
            return int(resp["Item"]["sum"])
```

Here we use PutItem to write the first number (*x*) to the table.
Then we do an UpdateItem to add the second number (*y*) to the existing value.
Finally, we call GetItem to retrieve the sum.

It turns out we can consolidate these three API calls into one.
The UpdateItem API creates a row if it doesn't exist yet (saving the PutItem), and we can also ask it to give us the value it just wrote to the row (saving the GetItem).
Here's what the consolidated version looks like:

```python
class DynamoCalculator:
    ...

    def add(self, x: int, y: int) -> int:
        """
        Adds two integers and returns the result.
        """
        with self.row_id() as calculation_id:
            resp = self.table.update_item(
                Key={"calculation_id": calculation_id},
                UpdateExpression="SET #sum = :x + :y",
                ExpressionAttributeNames={"#sum": "sum"},
                ExpressionAttributeValues={":x": x, ":y": y},
                ReturnValues="ALL_NEW"
            )
            return int(resp["Attributes"]["sum"])
```

Let's check it works:

```python
with DynamoCalculator() as calculator:
    print(calculator.add(1, 2))   # 3
    print(calculator.add(5, 3))   # 8
    print(calculator.add(5, -1))  # 4
```

Addition is a very common operation, so it's important we make it as fast as possible.
Consolidating three API calls into one is a good optimisation!



<h2>Subtraction<img src="/images/2020/subtraction.png" alt="X + Y = ?" class="operation"></h2>

Subtraction is the opposite of addition, with the convenient property that subtracting *y* is the same as adding (negative *y*).
This leads some people to define subtraction like so:

```python
    def subtract(self, x: int, y: int) -> int:
        """
        Subtracts one integer from another and returns the result.
        """
        return self.add(x, -y)
```

But you and I know these people are feeble and weak-willed.
This approach uses Python to reverse the sign of *y* for us, which is a computational operation.
What's the point of having a compute platform like DynamoDB if we don't use it for computing?

DynamoDB's UpdateItem API supports subtraction as well as addition, which is a much better approach:

```python
class DynamoCalculator:
    ...

    def subtract(self, x: int, y: int) -> int:
        """
        Subtracts one integer from another and returns the result.
        """
        with self.row_id() as calculation_id:
            resp = self.table.update_item(
                Key={"calculation_id": calculation_id},
                UpdateExpression="SET #difference = :x - :y",
                ExpressionAttributeNames={"#difference": "difference"},
                ExpressionAttributeValues={":x": x, ":y": y},
                ReturnValues="ALL_NEW"
            )
            return int(resp["Attributes"]["difference"])
```

Two operations down, two to go!



<h2>Multiplication<img src="/images/2020/multiplication.png" alt="X * Y = ?" class="operation"></h2>

This is where things get a bit trickier -- the UpdateExpression used by the UpdateItem API doesn't support multiplication, only addition and subtraction.
We'll have to build our own implementation of multiplication.
A simple approach is to use a recursive algorithm:

```
def multiply(x, y):
    if y == 0:
        return 0
    else:
        return x + multiply(x, y - 1)
```

Consider an example:

```
multiply(5, 3) = 5 + multiply(5, 2)
               = 5 + (5 + multiply(5, 1))
               = 5 + (5 + (5 + multiply(5, 0)))
               = 5 + (5 + (5 + 0))
               = 15
```

(Let's ignore the case where *y* is negative for now.)

If we want to implement this, we need a test for equality, and branching statements.
How do we do that?
We could use Python, or we could find a way to do them with DynamoDB.
We both know what the correct answer is.

Let's start by testing if two integers are the same.
For this, we can misuse [conditional operations](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ConditionExpressions.html).

Suppose we were using DynamoDB to store date-based information.
Each row includes a timestamp, and we want newer data to replace older data, but not the other way around.
We could do a GetItem and then a PutItem before we write anything, but if the row changes between the Get and the Put, we could write bad data.

A better approach would be to supply a condition with our PutItem -- for example, *"only update this row if the timestamp in the new row is greater than the timestamp in the already-stored row"*.
If the condition is true, the write succeeds.
If the condition is false, the write fails and we get an error.

One of the conditions you can specify is that two values are the same.
So let's try to write to the table with this condition -- if it succeeds, the numbers are equal; if it fails, they're not.

```python
class DynamoCalculator:
    ...

    def eq(self, x: int, y: int) -> bool:
        """
        Returns True if two integers are equal, False otherwise.
        """
        with self.row_id() as calculation_id:
            try:
                self.table.put_item(
                    Item={"calculation_id": calculation_id},
                    ConditionExpression=":x = :y",
                    ExpressionAttributeValues={":x": x, ":y": y},
                )
            except Exception as exc:
                return False
            else:
                return True
```

(We are using a bit of Python control flow for the `try … except` block -- I can't think of a better way to do this, but at least the equality testing is done inside DynamoDB.)

Next, let's use DynamoDB to implement basic control flow.
For an IF statement, we have a condition, an "if true" action, and an "if false" action.
We can continue to misuse conditional operations, and pass the boolean directly to DynamoDB:

```python
from typing import Callable


class DynamoCalculator:
    ...

    def if_(
        self,
        condition: bool,
        if_true: Callable[[], int],
        if_false: Callable[[], int]
    ) -> bool:
        """
        If ``condition`` is True, returns the output of ``if_true``.
        If ``condition`` is False, returns the output of ``if_false``.
        """
        with self.row_id() as calculation_id:
            try:
                self.table.put_item(
                    Item={"calculation_id": calculation_id},
                    ConditionExpression=":condition = :true",
                    ExpressionAttributeValues={":condition": condition, ":true": True}
                )
            except Exception as exc:
                return if_false()
            else:
                return if_true()
```

Notice that this code doesn't call "if_true" or "if_false" until they're needed.
This is a sophisticated programming technique called [*lazy evaluation*](https://en.wikipedia.org/wiki/Lazy_evaluation), and our ability to use it here speaks to the power of DynamoDB as a computing platform.

Now we have enough pieces to start building out our multiplication function:

```python
class DynamoCalculator:
    ...

    def multiply(self, x: int, y: int) -> int:
        """
        Multiplies two integers and returns the result.
        """
        def if_y_non_zero():
            return self.add(x, self.multiply(x, self.subtract(y, 1)))

        return self.if_(
            self.eq(y, 0),
            if_true=lambda: 0,
            if_false=if_y_non_zero
        )
```

This works if *y* is positive or zero, but if *y* is negative it keeps decrementing forever.
We need to tweak our algorithm slightly:

```
def multiply(x, y):
    if y == 0:
        return 0
    elif y < 0:
        return -1 * multiply(x, -y)
    else:
        return x + multiply(x, y - 1)
```

We can get `-y` by computing `0 - y`, and similar for `-1 * multiply(x, -y)`.
This leaves the problem of working out if `y` is negative.

DynamoDB supports all the logical operators in conditional updates, so we can follow the same technique we've already used twice:

```python
class DynamoCalculator:
    ...

    def lt(self, x: int, y: int) -> int:
        """
        Returns True if x < y, False otherwise.
        """
        with self.row_id() as calculation_id:
            try:
                self.table.put_item(
                    Item={"calculation_id": calculation_id},
                    ConditionExpression=":x < :y",
                    ExpressionAttributeValues={":x": x, ":y": y},
                )
            except Exception as exc:
                return False
            else:
                return True
```

This gives us the last piece we need to create a fully working multiplication function:

```python
class DynamoCalculator:
    ...

    def multiply(self, x: int, y: int) -> int:
        """
        Multiplies two integers and returns the result.
        """
        def if_y_non_negative():
            return self.add(x, self.multiply(x, self.subtract(y, 1)))

        def if_y_negative():
            y_pos = self.subtract(0, y)
            return self.subtract(0, self.multiply(x, y_pos))

        return self.if_(
            self.eq(y, 0),
            if_true=lambda: 0,
            if_false=lambda: self.if_(
                self.lt(y, 0),
                if_true=if_y_negative,
                if_false=if_y_non_negative
            )
        )
```



<h2>Division<img src="/images/2020/division.png" alt="X / Y = ?" class="operation"></h2>

We can tackle division in a similar way to multiplication, using a recursive algorithm:

```
def divide(x, y):
    if y < 0:
        return -1 * divide(x, -y)
    else:
        if x < y:
            return 0
        else:
            return 1 + divide(x - y, y)
```

Which falls out of the pieces we've already built like so:

```python
class DynamoCalculator:
    ...

    def divide(self, x: int, y: int) -> int:
        """
        Divides x by y and returns the result.  Assumes y != 0.
        """
        def if_y_negative():
            return self.subtract(0, self.divide(x, self.subtract(0, y)))

        def if_y_positive():
            return self.if_(
                self.lt(x, y),
                if_true=lambda: 0,
                if_false=lambda: self.add(1, self.divide(self.subtract(x, y), y))
            )

        return self.if_(
            self.lt(y, 0),
            if_true=if_y_negative,
            if_false=if_y_positive,
        )
```

This is the great thing about building our calculator from a library of reusable functions and operators: we can combine them to create more sophisticated functions.



## More logical operators and comparisons functions

We can continue to compose the functions we've already written to round out our calculator.

We can get "not equal to" by defining a NOT operator, and applying that to the output of "eq()":

```python
    def not_(self, condition: bool) -> bool:
        """
        Returns the negation of ``condition``.
        """
        return self.if_(
            condition,
            if_true=lambda: False,
            if_false=lambda: True
        )

    def ne(self, x: int, y: int) -> bool:
        """
        Returns True if two integers are different, False otherwise.
        """
        return self.not_(self.eq(x, y))
```

We can define "less than or equal to" by defining an OR operator, and applying that to the output of "lt()" and "eq()":

```python
    def or_(self, condition1: bool, condition2: bool) -> bool:
        """
        Returns True if at least one of ``condition1`` and ``condition2`` is True.
        """
        int_1 = self.if_(condition1, if_true=lambda: 1, if_false=lambda: 0)
        int_2 = self.if_(condition2, if_true=lambda: 1, if_false=lambda: 0)
        return self.ne(self.add(int_1, int_2), 0)

    def le(self, x: int, y: int) -> bool:
        """
        Returns True if x <= y, False otherwise.
        """
        return self.or_(
            self.eq(x, y),
            self.lt(x, y)
        )
```

We can define "greater than" and "greater than or equal to" as the negation of "less than or equal to" and "less than", respectively:

```python
    def gt(self, x: int, y: int) -> bool:
        """
        Returns True if x > y, False otherwise.
        """
        return self.not_(self.le(x, y))

    def ge(self, x: int, y: int) -> bool:
        """
        Returns True if x >= y, False otherwise.
        """
        return self.not_(self.lt(x, y))
```

And finally, for completion's sake, let's define an AND operator and a NAND operator:

```python
    def and_(self, condition1: bool, condition2: bool) -> bool:
        """
        Returns True if both ``condition1`` and ``condition2`` are True.
        """
        int_1 = self.if_(condition1, if_true=lambda: 1, if_false=lambda: 0)
        int_2 = self.if_(condition2, if_true=lambda: 1, if_false=lambda: 0)
        return self.eq(self.add(int_1, int_2), 2)

    def nand(self, condition1: bool, condition2: bool) -> bool:
        """
        Returns True if at least one of ``condition1`` and ``condition2`` are False.
        """
        return self.not_(self.and_(condition1, condition2))
```

The [NAND gate](https://en.wikipedia.org/wiki/Sheffer_stroke) is a key part of processor design, and being able to do it only using DynamoDB proves its capabaility as a computing platform.




## Conclusion

This post shows the potential for using DynamoDB as a cloud computing platform.
We were able to implement a simple calculator, comparison operators, and even better, a set of [logical gates](https://en.wikipedia.org/wiki/Logic_gate) (AND, OR, NOT and NAND).
This lays the foundation for building far more sophisticated programs.

Performance remains an issue.
As we'd expect, simple operations (addition, subtraction) are faster than more complex operations (multiplication, division), but there's room for improvement in both areas.
It's not clear whether the bottleneck is DynamoDB itself, or my home internet connection.
Hopefully a future update will bring the ability to run code directly inside DynamoDB itself.

Pricing follows the usual AWS model of "clear as mud".
DynamoDB pricing is based on [how many read and write "units" you use](https://aws.amazon.com/dynamodb/pricing/on-demand/), but it's not obvious how many units a given operation might require.

It's too soon to recommend using DynamoDB for production compute workloads, but these early signs are promising.
I hope Amazon continues to work on improving DynamoDB, and I look forward to seeing how other people use it in future.



## FAQs

**This is amazing.**
Not a question, but I appreciate the enthusiasm!

**This is an abomination.**
See above.

**DynamoDB isn't a compute platform, it's a database.**
Still not a question.
And you're wrong -- it *is* a compute platform, as this experiment shows.

**Why did you do this?**
Finally, a proper question!
Partly for fun, partly as a way to get some practice with the gnarly bits of the DynamoDB API that I forget every time I use.

**Can I get all the code you've written?**
Sure, it's all here:

{% details %}
<summary>dynamo_calculator.py</summary>

```python
#!/usr/bin/env python
"""
What happens if you try to use DynamoDB as an integer calculator?
"""

import contextlib
from typing import Callable
import uuid

import boto3


dynamodb = boto3.resource("dynamodb")


class DynamoCalculator:
    """
    An integer calculator that uses DynamoDB for compute.
    """
    def __enter__(self):
        table_name = f"calculator-{uuid.uuid4()}"

        dynamodb.create_table(
            AttributeDefinitions=[{
                "AttributeName": "calculation_id",
                "AttributeType": "S",
            }],
            TableName=table_name,
            KeySchema=[{
                "AttributeName": "calculation_id",
                "KeyType": "HASH"
            }],
            BillingMode="PAY_PER_REQUEST"
        )

        self.table = dynamodb.Table(table_name)
        self.table.wait_until_exists()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.table.delete()
        self.table.wait_until_not_exists()

    @contextlib.contextmanager
    def row_id(self):
        calculation_id = str(uuid.uuid4())
        yield calculation_id
        self.table.delete_item(Key={"calculation_id": calculation_id})

    def __repr__(self):
        return f"<DynamoCalculator {self.table.name}>"

    def add(self, x: int, y: int) -> int:
        """
        Adds two integers and returns the result.
        """
        with self.row_id() as calculation_id:
            resp = self.table.update_item(
                Key={"calculation_id": calculation_id},
                UpdateExpression="SET #sum = :x + :y",
                ExpressionAttributeNames={"#sum": "sum"},
                ExpressionAttributeValues={":x": x, ":y": y},
                ReturnValues="ALL_NEW"
            )
            return int(resp["Attributes"]["sum"])

    def subtract(self, x: int, y: int) -> int:
        """
        Subtracts one integer from another and returns the result.
        """
        with self.row_id() as calculation_id:
            resp = self.table.update_item(
                Key={"calculation_id": calculation_id},
                UpdateExpression="SET #difference = :x - :y",
                ExpressionAttributeNames={"#difference": "difference"},
                ExpressionAttributeValues={":x": x, ":y": y},
                ReturnValues="ALL_NEW"
            )
            return int(resp["Attributes"]["difference"])

    def eq(self, x: int, y: int) -> bool:
        """
        Returns True if two integers are equal, False otherwise.
        """
        with self.row_id() as calculation_id:
            try:
                self.table.put_item(
                    Item={"calculation_id": calculation_id},
                    ConditionExpression=":x = :y",
                    ExpressionAttributeValues={":x": x, ":y": y},
                )
            except Exception as exc:
                return False
            else:
                return True

    def if_(
        self,
        condition: bool,
        if_true: Callable[[], int],
        if_false: Callable[[], int]
    ) -> bool:
        """
        If ``condition`` is True, returns the output of ``if_true``.
        If ``condition`` is False, returns the output of ``if_false``.
        """
        with self.row_id() as calculation_id:
            try:
                self.table.put_item(
                    Item={"calculation_id": calculation_id},
                    ConditionExpression=":condition = :true",
                    ExpressionAttributeValues={":condition": condition, ":true": True}
                )
            except Exception as exc:
                return if_false()
            else:
                return if_true()

    def lt(self, x: int, y: int) -> int:
        """
        Returns True if x < y, False otherwise.
        """
        with self.row_id() as calculation_id:
            try:
                self.table.put_item(
                    Item={"calculation_id": calculation_id},
                    ConditionExpression=":x < :y",
                    ExpressionAttributeValues={":x": x, ":y": y},
                )
            except Exception as exc:
                return False
            else:
                return True

    def multiply(self, x: int, y: int) -> int:
        """
        Multiplies two integers and returns the result.
        """
        def if_y_non_negative():
            return self.add(x, self.multiply(x, self.subtract(y, 1)))

        def if_y_negative():
            y_pos = self.subtract(0, y)
            return self.subtract(0, self.multiply(x, y_pos))

        return self.if_(
            self.eq(y, 0),
            if_true=lambda: 0,
            if_false=lambda: self.if_(
                self.lt(y, 0),
                if_true=if_y_negative,
                if_false=if_y_non_negative
            )
        )

    def divide(self, x: int, y: int) -> int:
        """
        Divides x by y and returns the result.  Assumes y != 0.
        """
        def if_y_negative():
            return self.subtract(0, self.divide(x, self.subtract(0, y)))

        def if_y_positive():
            return self.if_(
                self.lt(x, y),
                if_true=lambda: 0,
                if_false=lambda: self.add(1, self.divide(self.subtract(x, y), y))
            )

        return self.if_(
            self.lt(y, 0),
            if_true=if_y_negative,
            if_false=if_y_positive,
        )

    def not_(self, condition: bool) -> bool:
        """
        Returns the negation of ``condition``.
        """
        return self.if_(
            condition,
            if_true=lambda: False,
            if_false=lambda: True
        )

    def ne(self, x: int, y: int) -> bool:
        """
        Returns True if two integers are different, False otherwise.
        """
        return self.not_(self.eq(x, y))

    def or_(self, condition1: bool, condition2: bool) -> bool:
        """
        Returns True if at least one of ``condition1`` and ``condition2`` is True.
        """
        int_1 = self.if_(condition1, if_true=lambda: 1, if_false=lambda: 0)
        int_2 = self.if_(condition2, if_true=lambda: 1, if_false=lambda: 0)
        return self.ne(self.add(int_1, int_2), 0)

    def le(self, x: int, y: int) -> bool:
        """
        Returns True if x <= y, False otherwise.
        """
        return self.or_(
            self.eq(x, y),
            self.lt(x, y)
        )

    def gt(self, x: int, y: int) -> bool:
        """
        Returns True if x > y, False otherwise.
        """
        return self.not_(self.le(x, y))

    def ge(self, x: int, y: int) -> bool:
        """
        Returns True if x >= y, False otherwise.
        """
        return self.not_(self.lt(x, y))

    def and_(self, condition1: bool, condition2: bool) -> bool:
        """
        Returns True if both ``condition1`` and ``condition2`` are True.
        """
        int_1 = self.if_(condition1, if_true=lambda: 1, if_false=lambda: 0)
        int_2 = self.if_(condition2, if_true=lambda: 1, if_false=lambda: 0)
        return self.eq(self.add(int_1, int_2), 2)

    def nand(self, condition1: bool, condition2: bool) -> bool:
        """
        Returns True if at least one of ``condition1`` and ``condition2`` are False.
        """
        return self.not_(self.and_(condition1, condition2))


if __name__ == "__main__":
    with DynamoCalculator() as calculator:
        print(calculator)

        print("")
        print("Arithmetic operations")
        print("")

        print(f"1 + 2    = {calculator.add(1, 2)}")
        print(f"5 + 3    = {calculator.add(5, 3)}")
        print(f"5 + (-1) = {calculator.add(5, -1)}")

        print("")

        print(f"1 - 2    = {calculator.subtract(1, 2)}")
        print(f"5 - 3    = {calculator.subtract(5, 3)}")
        print(f"5 - (-1) = {calculator.subtract(5, -1)}")

        print("")

        print(f"1 * 2    = {calculator.multiply(1, 2)}")
        print(f"5 * 3    = {calculator.multiply(5, 3)}")
        print(f"5 * (-1) = {calculator.multiply(5, -1)}")

        print("")

        print(f"1 / 2    = {calculator.divide(1, 2)}")
        print(f"5 / 3    = {calculator.divide(5, 3)}")
        print(f"5 / (-1) = {calculator.divide(5, -1)}")
        print(f"36 / 4   = {calculator.divide(36, 4)}")

        print("")
        print("Comparisons")
        print("")

        print(f"1 == 1?  {calculator.eq(1, 1)}")
        print(f"1 == 5?  {calculator.eq(1, 5)}")

        print("")

        print(f"1 != 1?  {calculator.ne(1, 1)}")
        print(f"1 != 5?  {calculator.ne(1, 5)}")

        print("")

        print(f"2 < 1?   {calculator.lt(2, 1)}")
        print(f"1 < 1?   {calculator.lt(1, 1)}")
        print(f"1 < 5?   {calculator.lt(1, 5)}")

        print("")

        print(f"2 <= 1?  {calculator.le(2, 1)}")
        print(f"1 <= 1?  {calculator.le(1, 1)}")
        print(f"1 <= 5?  {calculator.le(1, 5)}")

        print("")

        print(f"2 > 1?   {calculator.gt(2, 1)}")
        print(f"1 > 1?   {calculator.gt(1, 1)}")
        print(f"1 > 5?   {calculator.gt(1, 5)}")

        print("")

        print(f"2 >= 1?  {calculator.ge(2, 1)}")
        print(f"1 >= 1?  {calculator.ge(1, 1)}")
        print(f"1 >= 5?  {calculator.ge(1, 5)}")

        print("")
        print("Logical gates")
        print("")

        def display(value):
            return "T" if value else "F"

        print("P | Q | NOT(P) | AND(P, Q) | OR(P, Q) | NAND(P, Q)")
        print("--+---+--------+-----------+----------+------------")
        for (p, q) in [
            (True, True),
            (True, False),
            (False, True),
            (False, False)
        ]:
            print(
                f"{display(p)} | "
                f"{display(q)} | "
                f"{display(calculator.not_(p))}      | "
                f"{display(calculator.and_(p, q))}         | "
                f"{display(calculator.or_(p, q))}        | "
                f"{display(calculator.nand(p, q))}"
            )
```

{% enddetails %}

If you want extra fun, turn on your tracing tool of choice (I like [the q module](https://pypi.org/project/q/)) and watch how deep the recursion goes when you divide 36 by 4.

**Are there any tests?**
I'm testing the patience of everyone who works on DynamoDB.

**This code has recursion issues. How should I fix those?**
If you think the biggest issue with this code is that you might hit Python's recursion limit, I can't help you.

**I like brilliant ideas. What else can you recommend?**
In this post I've talked about using one of Amazon's compute services; other people have written about their database offerings:

*   Corey Quinn is [a fan of Route 53](https://www.lastweekinaws.com/podcast/aws-morning-brief/whiteboard-confessional-route-53-db/).
*   Kevin Kutcha [built a URL shortener with Lambda and only Lambda](https://kevinkuchta.com/2018/03/lambda-only-url-shortener/) (using Lambda functions to store the URL mappings, naturally).
    That post was an inspiration for this one.

**Can you make it <s>worse</s> better?**
Almost certainly.
if you have suggestions for how to do so, please @ me on Twitter (I'm [@alexwlchan](https://twitter.com/alexwlchan)).

---
layout: post
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
    Wikimedia Commons says this is a protest against <a href="https://commons.wikimedia.org/wiki/File:WendlandAntiNuclearProtest7.jpg">German nuclear policy</a>, but it's actually a protest about using any of my ideas in production.
  </figcaption>
</figure>



## Getting started

DynamoDB supports a wide variety of programming languages, including [Java](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Java.html), [.NET](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.NET.html) and [Python](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.html).
I'm going to use Python in this post, because that's what I'm familiar with, but these ideas can be used in other languages.

Within DynamoDB, the unit of compute is the *Table*.

---




## Initial pieces

Our calculator is going to need somewhere to do calculations, so let's assume we've already created a table where it can do stuff.
(You could create and delete a table every time you do something, but the latency would be even higher than it already is.)

Let's create a class that holds the table name:

```python
import boto3


dynamodb = boto3.resource("dynamodb")


class DynamoCalculator:
    """
    An integer calculator implemented in DynamoDB.
    """
    def __init__(self, table_name"):
        self.table = dynamodb.Table(table_name)
```

We'll do calculations in the rows of this table.
Each calculation will be assigned a UUID, which we need to clean up later.
Let's create a context manager to handle this for us:

```
import contextlib
import uuid


class DynamoCalculator:
    ...

    @contextlib.contextmanager
    def calculation_id(self):
        calc_id = str(uuid.uuid4())
        yield calc_id
        self.table.delete_item(Key={"id": calc_id})
```

This uses a hash key column `"id"` to track the calculation ID.
We'll see how this works when we implement some operations.



## Addition

![](addition.png)

DynamoDB supports numbers as a first-class type, and we can read and write numeric values with the GetItem and PutItem APIs, respectively.

The PutItem API completes replaces the existing row.
If you want to update the value in a row -- for example, incrementing a counter -- you can use the UpdateItem API and an [UpdateExpression](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.UpdateExpressions.html#Expressions.UpdateExpressions.SET).
Here's what that looks like:

```python
class DynamoCalculator:
    ...

    def add(self, x: int, y: int) -> int:
        """
        Adds two integers and returns the result.
        """
        with self.calculation_id() as calc_id:
            self.table.put_item(Item={"id": calc_id, "value": x})
            self.table.update_item(
                Key={"id": calc_id},
                UpdateExpression="SET #value = #value + :y",
                ExpressionAttributeNames={"#value": "value"},
                ExpressionAttributeValues={":y": y}
            )
            resp = self.table.get_item(Key={"id": calc_id})
            return int(resp["Item"]["value"])
```

Note that we're using the `calculation_id` to use the same ID for the row across all three API calls.
We cast the result to an `int()` because the Python SDK returns the number as a [Decimal](https://docs.python.org/3/library/decimal.html#decimal.Decimal), not an integer.

It turns out we can consolidate these three API calls into one.
The UpdateItem API can write to a row that doesn't exist yet, and we can also ask it to return the value it just wrote to the row.
Here's the improved version:

```python
class DynamoCalculator:
    ...

    def add(self, x: int, y: int) -> int:
        """
        Adds two integers and returns the result.
        """
        with self.calculation_id() as calc_id:
            resp = self.table.update_item(
                Key={"id": calc_id},
                UpdateExpression="SET #value = :x + :y",
                ExpressionAttributeNames={"#value": "value"},
                ExpressionAttributeValues={":x": x, ":y": y},
                ReturnValues="ALL_NEW"
            )
            return int(resp["Attributes"]["value"])
```

Let's check it works:

```pycon
>>> calculator = DynamoCalculator(table_name="Alex-2020-04-26-experiments")

>>> calculator.add(1, 2)
3

>>> calculator.add(5, 3)
8

>>> calculator.add(5, -1)
4
```

It even handles negative numbers!



## Subtraction

![](subtraction.png)

Subtraction is the opposite of addition.
It has the convenient property subtracting *Y* is the same as adding (negative *Y*).
This leads some people to define subtraction like so:

```python
class DynamoCalculator:
    ...

    def subtract(self, x: int, y: int) -> int:
        """
        Subtracts one integer from another and returns the result.
        """
        return self.add(x, -y)
```

Such a solution is blatantly cheating.
We're getting Python to reverse the sign of the number for us, which is a computational operation.
What's the point of having a compute platform like DynamoDB if we don't use it for computing?

Luckily, DynamoDB supports subtraction as well as addition in the UpdateItem API, and we can ask it to do the hard work:

```python
class DynamoCalculator:
    ...

    def subtract(self, x: int, y: int) -> int:
        """
        Subtracts one integer from another and returns the result.
        """
        with self.calculation_id() as calc_id:
            resp = self.table.update_item(
                Key={"id": calc_id},
                UpdateExpression="SET #value = :x - :y",
                ExpressionAttributeNames={"#value": "value"},
                ExpressionAttributeValues={":x": x, ":y": y},
                ReturnValues="ALL_NEW"
            )
            return int(resp["Attributes"]["value"])
```

Two operations down, two to go!



## Multiplication

![](multiplication.png)

This is where things start to get trickier.
A simple approach to multiplication uses a recursive algorithm:

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
               = 5 + (5 + (5 + multiple(5, 0)))
               = 5 + (5 + (5 + 0))
               = 15
```

(Let's ignore the case where `y` is negative for now.)

This requires some slightly more sophisticated logic -- how do we test for equality, or handle branching statements?

Let's start by testing if two integer values are the same.
For this, we can turn to [conditional updates](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ConditionExpressions.html).
When you Put or Update an item in DynamoDB, you can supply a condition telling it which items should be modified -- for example, I often have a `version` field on my Dynamo rows, and I use a conditional update to tell DynamoDB to prevent the version going backwards.

We try to write an item on the condition that two values are the same.
If they are the same, the operation succeeds and we can return `True`.
If they differ, the operation will fail and we can return `False`.
Like so:

```python
class DynamoCalculator:
    ...

    def eq(self, x: int, y: int) -> bool:
        """
        Returns True if two integers are equal, False otherwise.
        """
        with self.calculation_id() as calc_id:
            try:
                self.table.put_item(
                    Item={"id": calc_id},
                    ConditionExpression=":x = :y",
                    ExpressionAttributeValues={":x": x, ":y": y},
                )
            except Exception as exc:
                if type(exc).__name__ == "ConditionalCheckFailedException":
                    return False
                else:
                    raise
            else:
                return True
```

(We are using a bit of Python control flow for the `try … except` block -- I can't think of a better way to do this, but at least the equality testing is done inside DynamoDB.)

Next, let's use DynamoDB to implement some basic control flow.
We have a condition, an "if true" action an an "if false" action.
We could use the `if` statement in Python, but that would be admitting weakness and defeat.

Here's a better approach:

```python
from typing import Callable


class DynamoCalculator:
    ...

    def if_(
        self,
        condition: bool,
        if_true: Callable[[], int],
        if_false: Callable[[], int]
    ) -> int:
        """
        If ``condition`` is True, returns the output of ``if_true``.
        If ``condition`` is False, returns the output of ``if_false``.
        """
        with self.calculation_id() as calc_id:
            try:
                self.table.put_item(
                    Item={"id": calc_id},
                    ConditionExpression=":condition = :true",
                    ExpressionAttributeValues={":condition": condition, ":true": True}
                )
            except Exception as exc:
                if type(exc).__name__ == "ConditionalCheckFailedException":
                    return if_false()
                else:
                    raise
            else:
                return if_true()
```

This uses the same technique of abusing conditional update expressions as for the equality test, but this time it calls the appropriate "if true" or "if false" function, rather than returning the appropriate value.

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

This works if `y` is non-negative, but if `y` is negative it keeps decrementing forever.
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
        with self.calculation_id() as calc_id:
            try:
                self.table.put_item(
                    Item={"id": calc_id},
                    ConditionExpression=":x < :y",
                    ExpressionAttributeValues={":x": x, ":y": y},
                )
            except Exception as exc:
                if type(exc).__name__ == "ConditionalCheckFailedException":
                    return False
                else:
                    raise
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



## Division

![](division.png)

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

Which falls out of the logical operators we've already built like so:

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




## Logical operators and other comparisons functions

We could define the remaining comparison functions by writing more condition expressions, or we could compose them from the functions we've already written.

We can get "not equal to" by defining a "not" operator, and then applying that to the output of "eq()":

```python
    def not_(self, condition: bool) -> bool:
        """
        Returns the negation of ``condition``.
        """
        return self.if_(condition, if_true=lambda: False, if_false=lambda: True)

    def ne(self, x: int, y: int) -> bool:
        """
        Returns True if two integers are different, False otherwise.
        """
        return self.not_(self.eq(x, y))
```

We can define "less than or equal to" by defining an "or" operator, and applying that to the output of "lt()" and "eq()":

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

And finally, for completion's sake, let's define an "and" operator:

```python
    def and_(self, condition1: bool, condition2: bool) -> bool:
        """
        Returns True if both ``condition1`` and ``condition2`` are True.
        """
        int_1 = self.if_(condition1, if_true=lambda: 1, if_false=lambda: 0)
        int_2 = self.if_(condition2, if_true=lambda: 1, if_false=lambda: 0)
        return self.eq(self.add(int_1, int_2), 2)
```



## Closing thoughts

This post shows the potential for using DynamoDB as a cloud computing platform.
We were able to implement a simple calculator, comparison operators, and even better, a set of [logical gates](https://en.wikipedia.org/wiki/Logic_gate) (AND, OR and NOT).
This lays the foundation for building more sophisticated programs.

Performance remains an issue.
It's not clear whether the bottleneck is DynamoDB itself, or my home internet connection.
Hopefully a future update will bring the ability to run code directly inside DynamoDB itself.

It's too soon to recommend using DynamoDB for production compute workloads, but these early signs are promising.
I hope Amazon continues to work on improving DynamoDB, and I look forward to seeing how other people use it in future.



## Questions

**This is amazing.**
Not a question, but I appreciate the enthusiasm!

**This is an abomination.**
See above.

**DynamoDB isn't a compute platform, it's a database.**
Still not a question.
And it *is* a compute platform, as this experiment shows.

**Can I get all the code you've written?**
Finally, a proper question!
I've put it all together below, and it even includes some examples.

{% details %}
<summary>dynamo_calculator.py</summary>

```python
#!/usr/bin/env python
"""
What happens if you try to use DynamoDB as an integer calculator?
"""

import contextlib
import functools
from typing import Callable
import uuid

import boto3

dynamodb = boto3.resource("dynamodb")


class DynamoCalculator:
    """
    An integer calculator implemented in DynamoDB.
    """
    def __init__(self, table_name):
        self.table = dynamodb.Table(table_name)

    @contextlib.contextmanager
    def calculation_id(self):
        calc_id = str(uuid.uuid4())
        yield calc_id
        self.table.delete_item(Key={"id": calc_id})

    def add(self, x: int, y: int) -> int:
        """
        Adds two integers and returns the result.
        """
        with self.calculation_id() as calc_id:
            resp = self.table.update_item(
                Key={"id": calc_id},
                UpdateExpression="SET #value = :x + :y",
                ExpressionAttributeNames={"#value": "value"},
                ExpressionAttributeValues={":x": x, ":y": y},
                ReturnValues="ALL_NEW"
            )
            return int(resp["Attributes"]["value"])

    def subtract(self, x: int, y: int) -> int:
        """
        Subtracts one integer from another and returns the result.
        """
        with self.calculation_id() as calc_id:
            resp = self.table.update_item(
                Key={"id": calc_id},
                UpdateExpression="SET #value = :x - :y",
                ExpressionAttributeNames={"#value": "value"},
                ExpressionAttributeValues={":x": x, ":y": y},
                ReturnValues="ALL_NEW"
            )
            return int(resp["Attributes"]["value"])

    def eq(self, x: int, y: int) -> bool:
        """
        Returns True if two integers are equal, False otherwise.
        """
        with self.calculation_id() as calc_id:
            try:
                self.table.put_item(
                    Item={"id": calc_id},
                    ConditionExpression=":x = :y",
                    ExpressionAttributeValues={":x": x, ":y": y},
                )
            except Exception as exc:
                if type(exc).__name__ == "ConditionalCheckFailedException":
                    return False
                else:
                    raise
            else:
                return True

    def if_(
        self,
        condition: bool,
        if_true: Callable[[], int],
        if_false: Callable[[], int]
    ) -> int:
        """
        If ``condition`` is True, returns the output of ``if_true``.
        If ``condition`` is False, returns the output of ``if_false``.
        """
        with self.calculation_id() as calc_id:
            try:
                self.table.put_item(
                    Item={"id": calc_id},
                    ConditionExpression=":condition = :true",
                    ExpressionAttributeValues={":condition": condition, ":true": True}
                )
            except Exception as exc:
                if type(exc).__name__ == "ConditionalCheckFailedException":
                    return if_false()
                else:
                    raise
            else:
                return if_true()

    def lt(self, x: int, y: int) -> int:
        """
        Returns True if x < y, False otherwise.
        """
        with self.calculation_id() as calc_id:
            try:
                self.table.put_item(
                    Item={"id": calc_id},
                    ConditionExpression=":x < :y",
                    ExpressionAttributeValues={":x": x, ":y": y},
                )
            except Exception as exc:
                if type(exc).__name__ == "ConditionalCheckFailedException":
                    return False
                else:
                    raise
            else:
                return True

    def multiply(self, x: int, y: int) -> int:
        """
        Multiplies two integers and returns the result.
        """
        def if_y_non_negative():
            if y == 0:
                raise ValueError
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
        return self.if_(condition, if_true=lambda: False, if_false=lambda: True)

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



if __name__ == "__main__":
    table_name = "my-calculator-experiments"
    calculator = DynamoCalculator(table_name)

    print("Addition")
    print(f"1 + 2    = {calculator.add(1, 2)}")
    print(f"5 + 3    = {calculator.add(5, 3)}")
    print(f"5 + (-1) = {calculator.add(5, -1)}")

    print("")

    print("Subtraction")
    print(f"1 - 2    = {calculator.subtract(1, 2)}")
    print(f"5 - 3    = {calculator.subtract(5, 3)}")
    print(f"5 - (-1) = {calculator.subtract(5, -1)}")

    print("")

    print("Equality")
    print(f"1 == 1?  {calculator.eq(1, 1)}")
    print(f"1 == 5?  {calculator.eq(1, 5)}")

    print("")

    print("Comparison (LT)")
    print(f"2 < 1?   {calculator.lt(2, 1)}")
    print(f"1 < 1?   {calculator.lt(1, 1)}")
    print(f"1 < 5?   {calculator.lt(1, 5)}")

    print("")

    print("Multiplication")
    print(f"1 * 2    = {calculator.multiply(1, 2)}")
    print(f"5 * 3    = {calculator.multiply(5, 3)}")
    print(f"5 * (-1) = {calculator.multiply(5, -1)}")

    print("")

    print("Division")
    print(f"1 / 2    = {calculator.divide(1, 2)}")
    print(f"5 / 3    = {calculator.divide(5, 3)}")
    print(f"5 / (-1) = {calculator.divide(5, -1)}")
    print(f"36 / 4   = {calculator.divide(36, 4)}")

    print("")

    print("Comparison (NE)")
    print(f"2 != 1?  {calculator.ne(2, 1)}")
    print(f"1 != 1?  {calculator.ne(1, 1)}")
    print(f"1 != 5?  {calculator.ne(1, 5)}")

    print("")

    print("Comparison (LE)")
    print(f"2 <= 1?  {calculator.le(2, 1)}")
    print(f"1 <= 1?  {calculator.le(1, 1)}")
    print(f"1 <= 5?  {calculator.le(1, 5)}")

    print("")

    print("Comparison (GT)")
    print(f"2 > 1?  {calculator.gt(2, 1)}")
    print(f"1 > 1?  {calculator.gt(1, 1)}")
    print(f"1 > 5?  {calculator.gt(1, 5)}")

    print("")

    print("Comparison (GE)")
    print(f"2 >= 1? {calculator.ge(2, 1)}")
    print(f"1 >= 1? {calculator.ge(1, 1)}")
    print(f"1 >= 5? {calculator.ge(1, 5)}")
```

{% enddetails %}

If you want extra fun, turn on your tracing tool of choice (I like [the q module](https://pypi.org/project/q/)) and watch how deep the recursion goes when you divide 36 by 4.



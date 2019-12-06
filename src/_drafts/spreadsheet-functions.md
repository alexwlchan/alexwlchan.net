---
layout: post
title: "Some useful spreadsheet functions: FORMULATEXT, MATCH, CONCATENATE and INDIRECT"
category: Programming and code
---

I've been doing some work in spreadsheets recently, and I stumbled upon a couple of functions that let me do some neat things.
I don't do that much number crunching in Excel, so I'm leaving some notes here for my future self.

I was making a spreadsheet to track my student loan repayments, but this template could work for any sort of long-term loan.
Here's what my spreadsheet looks like:

<img src="/images/2019/spreadsheet_headings.png" alt="A row of a spreadsheet with headings 'Value at start of month', 'Interest rate', 'Interest accrued', 'Monthly repayment', 'Value at end of month'.">

The columns are as follows:

-   The *value at the start of the month* tells me how much I have to pay off at the start of the month.
-   The loan accrues [interest] every month, say at an *interest rate* of 1.25%.
    Multiply that by the current value of the loan, 1.25% of £1000 is £12.50, so that's the *interest accrued*.
-   If I pay off £100 (the *monthly repayment*), then at the end of the month I have £1000 + £12.50 &minus; £100 = £912.50 left to repay.

[interest]: https://en.wikipedia.org/wiki/Interest

This is a fairly typical loan pattern.
It doesn't always exactly match the figures from the lender (for example, if they round in a slightly different way to me), but it's close enough to be useful.
I use these spreadsheets to get a rough idea of my finances, not exact predictions.

I can use Excel formulas to calculate the values in each row automatically, rather than calculating them by hand.
Below each cell is the formula that created the result:

<img src="/images/2019/spreadsheet_onerow.png" alt="A row of a spreadsheet, with the formulae for each cell annotated in blue.">

These are standard arithmetic:

<style>
  dd:not(:last-child) {
    margin-bottom: 1em;
  }
</style>

<dl>
  <dt><code>=F2</code></dt>
  <dd>
    The value at the start of one month is the same as the value at the end of the previous month.
  </dd>

  <dt><code>=ROUND(B4*C4,2)</code></dt>
  <dd>
    The interest accrued is the current value of the loan multiplied by the interest rate.
    I round to 2 decimal places (the nearest penny) to keep the maths simple -- this avoids weird fractional pennies paying off in the background.
  </dd>

  <dt><code>=MIN(B4+D4,E2)</code></dt>
  <dd>
    I pay off the same amount as the previous month, unless the total money left in the loan is less than my regular repayment.
    If I only have £50 left to repay, I shouldn't hand over £100.
  </dd>

  <dt><code>=B4+D4-E4</code></dt>
  <dd>
    At the end of the month, the total left on the loan is what I had at the start of the month, plus any interest I've accrued, less what I've repaid that month.
  </dd>
</dl>

The blue cells contain the result of the first new function: [`FORMULATEXT`][FORMULATEXT].
This returns the text of a formula as a string, rather than the result.
For example, in cell B5 I have a formula `=FORMULATEXT(B4)`.
This looks in cell B4, then prints the formula it contains, which in this case is `=F2`.

I can imagine using this as a debugging tool, or if I wanted to show how a spreadsheet worked in a teaching example.
It's better than manually copying the formula text around, because it's guaranteed to stay up-to-date.

[FORMULATEXT]: https://support.office.com/en-us/article/FORMULATEXT-function-0A786771-54FD-4AE2-96EE-09CDA35439C8

Now suppose we let the loan run for a while.
Hopefully the total amount goes down over time, and eventually it might get to zero:

<img src="/images/2019/spreadsheet_manyrows.png" alt="The spreadsheets above, but with rows from January to December.">

Here the loan was fully paid off at the end of November.
But if the loan hung around for longer, we might not fit all the rows on the screen -- can we still find out when the loan finishes?
Could the spreadsheet say *"The loan will be fully paid off in November"*, without us having to scroll down and find that ourselves?

It turns out there are a couple of formulas that can help us:

<img src="/images/2019/spreadsheet_summary.png" alt="Some intermediate values, with their formulas shown in blue.">

Here's how they work:

<dl>
  <dt><code>=MATCH(0,F1:F13,0)</code></dt>
  <dd>
    The <a href="https://support.office.com/en-us/article/MATCH-function-E8DFFD45-C762-47D6-BF89-533F4A37673A"><code>MATCH</code> function</a> finds the first time a value appears in a collection &mdash; in this case, I&rsquo;m telling it to find the first time a cell in the range <code>F1:F13</code> has the value <code>0</code>.
    (The value Im looking for is the first argument; the third argument tells MATCH how to compare values in the cell range it&rsquo;s checking.)
    In this case, it tells us that the 12th element in the range of cells &ndash; that is, the 12th row &ndash; is the first time the value at the end of the month is 0.
    So we know the 12th row is when the loan was paid off.
  </dd>

  <dt><code>=CONCATENATE("A" & B15)</code></dt>
  <dd>
    Now we want to get the name of the month in row 12.
    The cell reference is A12, and we can build this reference with the <a href="https://support.office.com/en-us/article/CONCATENATE-function-8F8AE884-2CA8-4F7A-B093-75D702BEA31D"><code>CONCATENATE</code> function</a>.
    This function combines multiple strings &ndash; in this case, the literal string <code>"A"</code>, and the result of the MATCH function in cell B15.
  </dd>

  <dt><code>=INDIRECT(B16)</code></dt>
  <dd>
    If you have a cell reference as text, you can use the <a href="https://support.office.com/en-us/article/INDIRECT-function-474B3A3A-8A26-4F44-B491-92B6306FA261"><code>INDIRECT</code> function</a> to look up the contents of the cell.
    In this example, it first looks up the contents of cell B16 -- the literal string <code>"A12"</code>, so it means <code>=INDIRECT("A12")</code>.
    Then the contents of cell A12 is the string <code>"November"</code>, so that's what this function returns.
  </dd>
</dl>

Calling the CONCATENATE function again gets me what I want: a sentence telling me when the loan will be finished.
I can put this somewhere prominent, and the text will update as I tweak the parameters.

This has been useful for experimenting with some different repayment options -- if I pay off more each month, does it change how much I pay, or how quickly I finish the loan?
I can tweak some values, and instantly get those answers -- not go hunting to find them.

It goes beyond just loan repayments -- FORMULATEXT seems great for teaching, and CONCATENATE and INDIRECT allow a level of dynamic programming that I haven't known how to do in Excel before.
I don't know when I'll need spreadsheets again, but I'm excited to have these functions available when I do.

*If you'd like to play with the spreadsheet I used for this post, you can [download your own copy](/files/example_loan.xlsx).*

---
layout: post
title: Does Google know about the UK's election results?
summary: |
  The UK elected a new round of MPs last week, but you might not know it if you asked Google.
tags:
  - politics
colors:
  index_light: "#905422"
  index_dark:  "#bec8da"
---

{% comment %}
  Card image from https://commons.wikimedia.org/wiki/File:UK_Parliament_(Palace_of_Westminster)_(48982329356).jpg#%7B%7Bint%3Afiledesc%7D%7D, CC0
{% endcomment %}

Last week, fourteen years of Tory government came to an end with a Labour landslide.
It was a rough night for every Conservative candidate, many of whom either lost their seat or saw their majorities severely diminished.

One of those Conservative candidates was Nigel Huddleston.
First elected as the MP for Mid Worcestershire in 2015, he was re-elected with increased majorities in 2017 and 2019.
On Thursday, he was standing in the reformed constituency of Droitwich and Evesham.

I'd never heard of Nigel until yesterday, but when [one of his tweets] was heavily criticised in my timeline, I decided to look him up in Google.

[one of his tweets]: https://x.com/HuddlestonNigel/status/1810271800904819031

<figure style="width: 375px;">
  {%
    picture
    filename="nigel_huddleston.png"
    width="375"
    alt="Screenshot of Google results for ‘Nigel Huddleston’. The subtitle says ‘Former Member of Parliament of the United Kingdom’, accompanied by a large photo of him. Two more info boxes show his age (53 years) and his education."
    class="screenshot"
  %}
  <figcaption>
    Screenshot of Google search results, as retrieved 8 July 2024 at 14:08&nbsp;BST.
    No cropping.
  </figcaption>
</figure>

The one-line summary describes him as a "former Member of Parliament", so I assumed he was one of the many Conservative MPs who lost their seat.

However, that wasn't true -- he was actually re-elected.
Scrolling down the page further, I found several news articles about his victory, albeit with a reduced majority.
Via Wikipedia, I even found the [official results] on the council website through Wikipedia as further proof.

How many people will scroll down the page for the full story, and how many will stop at the one-line summary?

[official results]: https://www.wychavon.gov.uk/residents/elections

## Why is this happening?

This feels like a problem.
It's tempting to chalk it up to Google's [wayward experiments with AI], but I think there's a simpler explanation: they're working from stale data.

In the run-up to any general election, Parliament gets dissolved.
There are no Members of Parliament until after the election, because there is no Parliament.
In 2024, Parliament was dissolved on May 30th.

Both Nigel's social media pages and the Parliament website were updated to reflect this change, as we can see in Google's cached search results:

<figure style="width: 600px;">
  {%
    picture
    filename="cached_google_entries.png"
    width="600px"
    class="screenshot"
    alt="Screenshot of two links in Google search. The first is to Nigel's Facebook page with the preview text ‘Parliament has been dissolved until after the general election. As a result, I am no longer the MP for Mid Worcestershire’. The second link is to a Register of Interests on the UK Parliament website. The preview text reads ‘Nigel Huddleston is no longer a member, but was most recently the Conservative MP for Mid Worcestershire, and left the Commons on 30 May 2024’."
  %}
  <figcaption>
    Screenshot of Google search results, as retrieved 8 July 2024 at 17:21&nbsp;BST.
  </figcaption>
</figure>

But if you actually click through to the pages today, both now say he's a Member of Parliament.

Presumably, Google crawled these pages sometime in the last month, saw the phrase "no longer an MP", and updated their search summary.
They haven't recrawled the pages since Thursday, so this is the newest information they have.

With this idea in mind, I looked at the Google search results of about 100 other MPs who were standing for re-election and held their seats.
Two-thirds were described as "Member of Parliament", "politician", or some other term which looks correct.
But a third were described as "former Member of Parliament" -- mostly backbenchers or MPs who aren't as prominent on the national stage.
It's not just Nigel.

Eventually, Google will update its data and notice that these people should now be described as "Member of Parliament".
Alternatively, you can submit [search feedback] to Google, and they might fix it more quickly.
(This is what I did for Nigel and several dozen other MPs, and several of the search results were fixed within the hour.)

In the 12 hours since I started writing this post, a handful of MPs have already had their labels corrected separate from my corrections -- but plenty still remain, and the lingering inaccuracy feels uncomfortable.

[wayward experiments with AI]: https://www.wired.com/story/google-ai-overview-search-issues/
[search feedback]: https://support.google.com/websearch/answer/3338405?hl=en

## Why does this matter?

Many people still trust Google to provide quick and accurate information.
This trust is both a strength and a responsibility, especially in an era where political misinformation runs rampant.
If Google displays inaccurate or outdated information, it can mislead individuals and undermine trust in politics.

This isn't a hypothetical issue.
It came to my attention because I saw somebody on Twitter believe Google's search results over Nigel's own Twitter feed, where his display name is "Nigel Huddleston MP".
They thought he had to change his title, not Google.

Although the truth was available further down the page, we know that lots of people only read the one-line summary.
Google designs the results page to make those summaries prominent and to allow people to find key information quickly.
This saves users from clicking extra links, but it also means Google takes on the responsibility for keeping those summaries accurate.

It's concerning that a tech giant lags behind in updating such important information, when volunteer-run projects can manage much more effectively.
Wikipedia, for example, already has [a complete list of newly-elected MPs][wikipedia].
Pages for individual MPs also have a notice indicating that election-based information may be outdated, so readers are aware of potential inaccuracies:

{%
  picture
  filename="wikipedia_entry.png"
  width="567"
  class="screenshot"
%}

Hopefully this will all be fixed within a few days when Google recrawls the Parliament website and updates the rest of their one-line summaries.
But it's concerning that it happened in the first place.
Accurate, timely updates aren't a nice-to-have; they're required if we want to have informed citizens and a healthy democracy.

Given Google's pivotal role as an information provider, and the global sensitivity of political information, I'm surprised they don't have a team whose sole purpose is to follow elections and keep Google up-to-date as results are announced.

When Google tells us to [eat rocks and put glue on pizza], it's annoying but fairly harmless -- we all know to ignore it.
When Google starts giving us outdated or incorrect information about politics, it's more concerning -- we're less likely to know what the truth actually is.

It's tempting to dismiss this as an overreaction, and I almost spiked this article because I didn't think it was important enough.
I'd be less concerned if this was just a hypothetical issue, but I've seen multiple people who looked at Google and came to the wrong conclusion.
It does matter, and we shouldn't be complacent about political misinformation.

In sociology, there's a term [normalisation of deviance] which describes the way mistakes and issues can become culturally normalised.
Those mistakes become the new baseline, and allow for more serious mistakes to occur.
This repeats until there's a catastrophic failure.

It feels like something similar is happening with Google search, and information more broadly, and I don't know what to do about it.

[wikipedia]: https://en.wikipedia.org/wiki/List_of_MPs_elected_in_the_2024_United_Kingdom_general_election
[eat rocks and put glue on pizza]: https://www.wired.com/story/google-ai-overview-search-issues/
[normalisation of deviance]: https://en.wikipedia.org/wiki/Normalization_of_deviance
[Overton window]: https://en.wikipedia.org/wiki/Overton_window

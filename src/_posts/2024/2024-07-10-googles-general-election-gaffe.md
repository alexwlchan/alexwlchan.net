---
layout: post
date: 2024-07-10 08:06:34 +00:00
title: Google is showing outdated results from the UK's election
summary: |
  Dozens of MPs who were re-elected to their seats are still labelled “former Member of Parliament”, days after the election results.
tags:
  - politics
colors:
  css_light: "#13772f"
  css_dark:  "#b4c492"
card_attribution: https://www.parliament.uk/globalassets/house-of-commons/hoc-digital/news-story-images/dsc_6286.jpg
---

Last week, fourteen years of Tory government came to an end with a Labour landslide.
It was a rough night for every Conservative candidate, many of whom either lost their seat or saw their majorities severely diminished.

One of those Conservative candidates was Nigel Huddleston.
First elected as the MP for Mid Worcestershire in 2015, he was re-elected with increased majorities in 2017 and 2019.
On Thursday, he was standing in the replacement constituency of Droitwich and Evesham.

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

The subtitle describes him as a "former Member of Parliament", so I assumed he was one of the many Conservative MPs who lost their seat.

But that's not true.
He was re-elected!

Scrolling down the page further, I found two news articles about his victory, albeit with a reduced majority.
(Specifically, the local papers in [Droitwich] and [Evesham].)
And through Wikipedia, I found the [official results] on the council website as further proof.

How many people will scroll down the page for the full story, and how many will stop at the one-line summary?

[Droitwich]: https://droitwichstandard.co.uk/news/general-election-result-conservative-nigel-huddleston-re-elected-in-droitwich/
[Evesham]: https://www.eveshamjournal.co.uk/news/24432254.conservative-nigel-huddleston-keeps-droitwich-evesham/
[official results]: https://www.wychavon.gov.uk/residents/elections

## Why is this happening?

This feels like a problem.
It's tempting to chalk it up to Google's [wayward experiments with AI], but I think there's a simpler explanation: they're working from stale data.

There are no MPs in the run-up to a general election.
Shortly after an election is called, Parliament comes to an end.
The formal term is ["dissolution"][dissolved] -- every seat in the House of Commons becomes vacant and there's no more Parliamentary business until after the election.
There are no Members of Parliament, because there is no Parliament for them to be part of.

This year, Parliament was dissolved on May 30th.

MPs are given [specific guidance](https://www.parliament.uk/globalassets/about-parliament/general-election/members_standing_redacted_-1.pdf) about what to do when Parliament is dissolved, and that includes how they describe themselves on the Internet.

<figure style="width: 581px;">
  {%
    picture
    filename="mp_guidance.png"
    width="581"
    class="screenshot"
    alt="Text. ‘Websites and social media accounts must carry a disclaimer to clarify that you are no longer a Member of Parliament. Social media accounts which include the handle 'Member of Parliament' or MP' may remain as they are, as long as a disclaimer is added. Example disclaimer: Parliament has been dissolved until after the General Election and I am no longer an MP.’"
  %}
  <figcaption>
    From <a href="https://www.parliament.uk/globalassets/about-parliament/general-election/members_standing_redacted_-1.pdf"><em>Dissolution Guidance: Members standing</em></a>, House of Commons, page 20.
    This is part of a longer section <em>Use of the title ‘Member of Parliament’
or ‘MP’</em>.
    Retrieved 10 July 2024.
  </figcaption>
</figure>

Both Nigel's [Facebook page](https://www.facebook.com/NigelHuddlestonMP/) and the [Parliament website](https://members.parliament.uk/member/4407/registeredinterests) were updated to reflect this change, as we can see in Google's cached search results:

<figure style="width: 581px;">
  {%
    picture
    filename="cached_google_entries.png"
    width="581"
    class="screenshot"
    alt="Screenshot of two links in Google search. The first is to Nigel's Facebook page with the preview text ‘Parliament has been dissolved until after the general election. As a result, I am no longer the MP for Mid Worcestershire’. The second link is to a Register of Interests on the UK Parliament website. The preview text reads ‘Nigel Huddleston is no longer a member, but was most recently the Conservative MP for Mid Worcestershire, and left the Commons on 30 May 2024’."
  %}
  <figcaption>
    Screenshot of Google search results, as retrieved 8 July 2024.
  </figcaption>
</figure>

But if you actually visit either of those pages today, they now say he's a Member of Parliament.

Presumably, Google crawled these pages sometime after the dissolution of Parliament, saw the phrase "no longer an MP", and updated their search summary.
They haven't recrawled the pages since Friday, so this is the newest information they have.

With this theory in mind, I looked at the Google search results of 150 other MPs who were standing for re-election and who held their seats.

*   Two-thirds were described as "Member of Parliament", "politician", or some other term which looks correct.
    Google's search index is at least somewhat aware of the election results.
*   But the other third were described as "former Member of Parliament" -- mostly backbenchers or MPs who aren't as prominent on the national stage.
    And they come from all the parties -- it's not just Nigel, and it's not some anti-Tory bias.

Put another way, that's over 50 MPs who were incorrectly described as "former Member of Parliament" on Tuesday morning -- and I only got halfway through the list.

Eventually, Google will update its data and notice that these people should now be described as "current MP", but who knows how long that will take?

You can submit [search feedback] to Google, and that does tend to fix it pretty quickly.
I submitted a correction for Nigel's results, and it was fixed within the hour.
I submitted corrections for two dozen more MPs, and they were fixed within the day.
I included links to the [results on the BBC news site](https://www.bbc.co.uk/news/election/2024/uk/constituencies) as references.
(That covers maybe a quarter of the affected MPs -- it's a long list.
I'm working through the rest, but it's a tedious process.)

In the 48 hours since I started writing this post, a handful of other MPs have had their labels corrected independent of my corrections -- but plenty of outdated information still remains, and the lingering inaccuracy feels uncomfortable.

> **Update, 18 July 2024:** I went through and submitted corrections for every incorrectly labelled MP, and Google's search results are finally correct. I love doing free data entry for one of the world's richest companies.

[dissolved]: https://www.parliament.uk/about/how/elections-and-voting/general/dissolution/
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
It saves users from clicking extra links, but it also means Google takes on the responsibility of keeping those summaries accurate.

It's concerning that a tech giant lags behind in updating such important information, especially when volunteer-run projects can manage much more effectively.
Wikipedia, for example, already has [a complete list of newly-elected MPs][wikipedia].
And pages for individual MPs have a notice indicating that election-based information may be outdated, so readers are aware of the potential for inaccuraries:

<figure style="width: 581px;">
  {%
    picture
    filename="wikipedia_entry.png"
    width="581"
    class="screenshot"
    alt="Screenshot of a Wikipedia entry. At the top is a notice: ‘This article's subject stood for re-election to the British House of Etty Commons on 4 July. This article may be out of date during and after this period. Feel free to improve it (updates without reliable references will be removed) or discuss changes on the talk page. Remove this template once the article is no longer out of date.’"
  %}
  <figcaption>
    Screenshot of <a href="https://en.wikipedia.org/wiki/Nigel_Huddleston">Nigel Huddleston’s Wikipedia page</a>.
    Retrieved 8 July 2024.
  </figcaption>
</figure>

Hopefully this will all be fixed within a few days when Google recrawls the Parliament website and updates the rest of their one-line summaries.
But it's concerning that it happened in the first place.
Accurate, timely updates aren't a nice-to-have; they're required if we want to have informed citizens and a healthy democracy.

Given their pivotal role as an information provider, and the global sensitivity of political news, I'm surprised that Google don't have a team whose sole purpose is to follow elections and keep their search results up-to-date as election results are announced.

When Google tells us to [eat rocks and put glue on pizza], it's annoying but fairly harmless -- we all know to ignore it.
When Google starts giving us outdated or incorrect information about political news, it's more concerning -- we're less likely to know what the truth actually is.

It's tempting to dismiss this as an overreaction, and I almost spiked this article because I didn't think it was important enough.
I'm still not sure if I'm making a fuss over nothing.
I'd be less concerned if this was just a theoretical issue, but I've seen multiple people who looked at Google and came to the wrong conclusion.

But I think it does matter, and we shouldn't be complacent about political misinformation.
Bad actors thrive in a world where we can't trust what we read, and we shouldn't sweep mistakes under the carpet.

[wikipedia]: https://en.wikipedia.org/wiki/List_of_MPs_elected_in_the_2024_United_Kingdom_general_election
[eat rocks and put glue on pizza]: https://www.wired.com/story/google-ai-overview-search-issues/
[normalisation of deviance]: https://en.wikipedia.org/wiki/Normalization_of_deviance
[Overton window]: https://en.wikipedia.org/wiki/Overton_window

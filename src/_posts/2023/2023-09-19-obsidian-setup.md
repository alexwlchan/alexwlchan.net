---
layout: post
date: 2023-09-19 21:30:59 +00:00
title: How I set up my Obsidian vaults
summary: The tags, folders, and themes I use to manage information in my Obsidian vaults.
tags:
  - obsidian
  - taking notes
---

{% comment %}
  Card image based on https://www.pexels.com/photo/close-up-of-obsidian-in-rock-4775418/
{% endcomment %}

Obsidian still feels like my "new" app for managing my notes, but according to my daily journal I've been using it for nearly three years.
Time flies when you're organising information!

I've grown to really like it, and I expect to keep using it for a while to come.
Its approach to tagging and linked notes fits my mental model, and there's a lot of flexibility in the plugin architecture.
I can make it look nice, add a few basic features I want, and it syncs nicely across my Mac and my iPhone.

Inspired by [Steph Ango’s example][stephango], I thought it might be useful to write a little about how I structure my Obsidian vaults.
My setup is somewhat fluid, so consider this as more of a point-in-time snapshot than a definitive approach -- I keep tweaking it as I find better ways to organise my notes.

[stephango]: https://stephango.com/vault

---

# My vaults

I have two vaults:

*   My **work** vault has everything that's specific to my day job – meeting minutes, project plans, notes about ongoing work.
    This is scoped to my current employer and lives on my work laptop – when I change jobs, I’ll throw this vault away and create a new one.
*   My **personal** vault has everything else.

The two vaults have the same structure, but different contents.
Usually the distinction is pretty clear-cut, but occasionally there’s some overlap.
For example, I learn about AWS in the course of my work.
If I learn something which is generically useful and not specific to my employer's setup, I'll put the notes in my personal vault rather than the work vault.

<style type="x-text/scss">
  #screenshots {
    display: grid;
    grid-template-columns: auto;
    grid-gap: var(--grid-gap);

    /* This feels like it should be possible using the :nth-child selector,
     * but I couldn't get it working
     */

    .first {
      border-bottom-right-radius: 0;
      border-bottom-left-radius:  0;
    }

    .second {
      border-top-right-radius: 0;
      border-top-left-radius:  0;
    }
  }
</style>

<figure id="screenshots">
  {%
    picture
    filename="obsidian-personal-theme.png"
    width="523"
    class="screenshot first"
    alt="A screenshot of a note and the top bar in my personal vault. The top bar has a red tint, and the title of the note is a matching shade of red. The note text is in a serif font (Geneva)."
  %}
  {%
    picture
    filename="obsidian-work-theme.png"
    width="523"
    class="screenshot second"
    alt="A screenshot of a note and the top bar in my work vault. The top bar has a yellow tint, but the title of the note is a dark green. The note text is in a sans serif font (Inter)."
  %}
</figure>

I'm using the [Minimal theme], and I use the [Minimal Settings plugin] to give each vault a distinct appearance.
I'm a very visual person, and making the two vaults look different helps reinforce the distinction in my mind.
I use a similar set of colour-based themes to help me distinguish between Slack workspaces.

[Minimal theme]: https://minimal.guide/home
[Minimal Settings plugin]: https://minimal.guide/plugins/minimal-theme-settings

---

<style type="x-text/css">
  @media screen and (min-width: 500px) {
    #obsidian_tags {
      display: inline-block;
      float: right;

      margin-left:   var(--default-padding);
      margin-bottom: var(--default-padding);
      margin-top:    calc(-1 * var(--default-padding));
    }
  }
</style>

{%
  picture
  filename="obsidian-tags.png"
  width="299"
  class="screenshot"
  id="obsidian_tags"
  alt="A screenshot of my tag panel in Obsidian. There's a list of tags on the left-hand side, and counts down the right. The first few tags are daily-journal (773), books-ive-read (173), articles-to-write (124) and talks-ive-watched (97). There are also a couple of collapsed tag lists, which indicate prefixes, including 'aws', 'event' and 'python'."
%}

# Tags

I’m a [big fan of keyword tagging][tagging], and I use it in all my notes.
Every note has at least one tag; often multiple.

I tag liberally, adding all the keywords that I think I might use to search for something later -- I think of my tags as a [“search engine in reverse”][search_engine].
If I think I might look for a note in three different ways, I give it three different tags.

I create lot of different tags -- my primary vault has at least 800.
The distribution is very skewed, with maybe 50 tags that I use a lot, and then a long tail of tags that are only used a handful of times.
This might seem messy to some people, but it works for me – even if a tag is only used once or twice, it's still useful for searching.

I use prefixes as a way to namespace some of tags, like `aws/amazon-s3` and `python/pip`.
This helps keep my list of tags somewhat organised, but otherwise it’s a bit of an inconsistent mess.
e.g. I don't have any rules about singular vs plural

I have different tags in each of my vaults, but I try to use the same tag in both places if it means the same thing.

[tagging]: https://alexwlchan.net/2019/my-scanning-setup/#how-should-i-organise-my-files
[search_engine]: https://idlewords.com/talks/fan_is_a_tool_using_animal.htm

---

# Folders

I have a handful of top-level folders, and I put most notes in folders.
Both of my vaults have the same set of top-level folders.

I try not to keep too many notes in my root – it's mostly brand new notes, stuff I'm actively working on, or notes I refer to frequently.
When I'm finished working on a note, I move it into a folder.

The folders I use:

*   **Attachments** for images, audio, PDFs, and so on. Anything that isn’t a text file.
    I use my [image gallery plugin] to browse the contents of this folder.

*   **Ideas** for anything I think of that I might like to do in the future, but don’t want to do right now.
    This includes ideas for projects, books I might like to read, half-finished blog posts, and more.
    I like being able to capture my ideas and then get them out of the way, without committing to finishing them.

	  Some of these entries are very long-lived, and I’ve built them up over multiple years.
    I’ll capture the initial spark of something, then go back and add more details as I think of them.
    This accumulation of thoughts can be useful if I ever go back and actually do the thing.

*   **Journal** is for all of my journal entries, or anything I’ve done that’s bound to a particular time (DIY, craft projects, holiday plans, and so on).

	  I have per-year folders to keep it manageable, but there’s not a lot of consistency.
    I have my journal entries going back as far as 2009, and I’ve had quite a few different approaches to journaling in that time!

*   **People** is for per-person notes.
    These files are pretty small, and usually exist for easy linking rather than for in-depth notes.
    For example, it’s much easier to search for all journal entries linked to “Jane Smith” than it is to search for all instances of the word “Jane”.

	  Occasionally I do put bits of info in somebody’s note that isn’t bound to a specific journal entry – food allergies, the names of their kids, gift preferences, and so on.

*   **Reference** is for detailed notes on anything outside my vault – books I’ve read, videos I’ve watched, podcasts I’ve listened to.
    I have subfolders for the different types of media.

*   **Snippets** is for little bits of information I want to save. A cool tweet, an interesting word, some trivia fact.

At least to me, it's always obvious which of these folders a note belongs in.
This has been a constant feature of all my folder setups – I want to be able to file notes immediately, without thinking.
I don't want to be wondering where a particular note should be stored on a day-to-day basis.

[image gallery plugin]: /2022/obsidian-plugin/

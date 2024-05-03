---
layout: post
title: What is psephology?
summary: |
  It's the scientific study of elections and voting, and it comes from the Greek word for "pebble", because pebbles were used for voting in ancient Greece.
tags:
  - politics
  - naming-things
  - history
colors:
  css_light: "#b26036"
  css_dark:  "#f59a53"
---
Yesterday there were local elections in the UK, and this morning I've been catching up on the news.
As I was reading Yohannes Lowe's live coverage in the Guardian, I [spotted a word I didn't recognise][guardian] (emphasis mine):

> Labour and the Conservatives are each defending about 1,000 seats, and *psephologists* predict that the Tories may lose about 500.

A quick trip to Google cleared up my initial confusion: psephologists are experts in *psephology*, which is the scientific study of elections and voting behaviour.

I could have guessed that definition from the context, but not if I saw the word in isolation.
Although I recognise the *-ology* suffix as "the study of something", I didn't recognise the *pseph-* prefix at all, and I was curious where it came from.

[guardian]: https://www.theguardian.com/politics/live/2024/may/02/local-elections-2024-latest-results-live-tory-conservative-labour-lib-dem-green-south-blackpool-mayor-london-west-midlands-tees-valley?page=with:block-6633f9e98f08715725f7b79e#block-6633f9e98f08715725f7b79e

## Voting and counting in ancient Greece

The [Wikipedia article][wikipedia] for psephology explains that *pseph-* comes from the Greek word for pebble, because they were used for voting in ancient Greece.
It refers to [an article by Annelisa Stephan][getty]:

> Voting with pebbles? Even allowing for artistic license, it seems the Greeks really did it this way. Voters deposited a pebble into one of two urns to mark their choice; after voting, the urns were emptied onto counting boards for tabulation. […] In ancient Greece a pebble was called a *psephos*, which gives us the dubious term psephology, the scientific study of elections.

I also found a paper by Alan Boegehold [*Towards a Study of Athenian Voting Procedure*](https://www.ascsa.edu.gr/uploads/media/hesperia/147360.pdf), which describes the use of pebbles when counting votes in ancient Greece.
It talks about voting using special bronze discs as ballots, and various mechanisms for keeping ballots secret.

This includes an early example of [ballot stuffing](https://en.wikipedia.org/wiki/Electoral_fraud#Ballot_stuffing), when "thirty men somehow dropped a total of more than sixty ballots into [the urn]".

[wikipedia]: https://en.wikipedia.org/wiki/Psephology
[getty]: https://www.getty.edu/news/voting-with-the-ancient-greeks/

He also describes a scene from Greek vase paintings, in which men cast votes for Ajax and Odysseus using piles of pebbles.
One notable aspect is that there doesn't seem to be any secrecy involved in the voting -- we can see who two of the men are voting for.

<style>
  @media screen and (min-width: 700px) {
    #vases {
      display: grid;
      grid-template-columns: auto auto;
      grid-gap: var(--grid-gap);
    }

    #vases figure {
      grid-row: 1 / 1;
      grid-column: 2 / 2;
      margin-top: 0;
    }

    #vases blockquote {
      grid-row: 1 / 1;
      grid-column: 1 / 2;
      margin-top: 0;
    }
  }

  @media screen and (max-width: 700px) {
    #vases figure {
      width: calc(100% - 2 * var(--default-padding));
    }
  }

</style>

<div id="vases">
  <figure>
    {%
      picture
      filename="voting_on_vases.jpg"
      width="700"
      link_to="https://www.getty.edu/art/collection/object/103W7A?altImage=458e6e84-6c86-4b76-835a-670cfb3f416f"
    %}
    <figcaption>
      Extract from the bottom of a red-figured kylix.
      Photo from <a href="https://www.getty.edu/art/collection/object/103W7A?altImage=458e6e84-6c86-4b76-835a-670cfb3f416f">the J.&nbsp;Paul Getty Museum</a> website, 86.AE.286.
      Public domain.
    </figcaption>
  </figure>
  <blockquote>
    <p>
      Athena stands behind a low table (or altar?) which men approach from right and left. They are about to vote; two, in fact, are in the act of voting. That the others have already voted is clear from the two small piles of pebbles on the altar. The pebbles to the left appear to be about double the number of those on the right. They represent votes cast for Odysseus, the victor, while those to the right, fewer, have been cast for Ajax. The two heroes themselves appear at the extreme right and left. Athena, gesturing gracefully with her right hand, certifies Odysseus' victory, although the voting is not yet over.
    </p>
  </blockquote>
</div>

feels like a paralle of modern politics, where result is often known before voting is concluded

(Sorry Ajax.)

He also describes the use of pebbles as a counting mechanism, when fingers weren't sufficient.
Mostly he's talking about ancient Greece, but he also mentions pebbles being sealed inside clay tablets as a form of bookkeeping in ancient Mesopotamia.
They were placed inside a tablet with an inscription of a sheep (or goat), and the pebbles counted the animals involved in a transaction.
I've definitely come across this idea before, although I can't remember where.

## Other uses of *pseph-*

I'm familiar with stones being called *lithos*, and the various English words that come from that (my favourite being the whimsical [*lithobraking*](https://en.wikipedia.org/wiki/Lithobraking)), but I don't think I ever knew the word *psephos*.

Wikipedia has a list of English words [that use *pseph-* as a root](https://en.wikipedia.org/wiki/List_of_Greek_and_Latin_roots_in_English/P#pseph-), and I don't recognise any of them.
Two of the words are literally about pebbles ([*psephite*](https://en.wikipedia.org/wiki/Psephite)/*psephitic* describes sediment made of pebble-sized fragments), and a third is about their use in counting ([*isopsephy*](https://en.wikipedia.org/wiki/Isopsephy) is adding up the number values of the letters to get a single number).

The latter looks like it could be a fun Wikipedia rabbit hole about word counting methods that aren't dissimilar to Scrabble, including a similar Hebrew practice called [*gematria*](https://en.wikipedia.org/wiki/Gematria), but I really have to stop now.

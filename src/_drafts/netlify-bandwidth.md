---
layout: post
title: Adding my Netlify bandwidth usage to my analytics dashboard
summary: Am I going to run out of bandwidth on my free tier?
tags: 
  - netlify
  - blogging-about-blogging
colors:
  index_light: "#0f705f"
  index_dark:  "#14b09b"
---
I currently host this website on the [Netlify Starter plan][pricing], which doesn't charge me a monthly fee and gives me 100GB of bandwidth per month.
But if I exceed that limit, I get charged $55 per 100GB of extra bandwidth.
It [gets expensive][reddit]!

I've only gone past the 100GB monthly limit twice, both times when I had a post go unexpectedly viral.
It was annoying, not life-ruining.

I've added a new graph to my analytics dashboard, which shows how much of my Netlify bandwidth I've used.
I check this dashboard every few days (more if a post is popular), so I'm more likely to see if I'm about to hit my limit:

{%
  picture
  filename="netlify-graph.png"
  width="527"
  class="screenshot"
%}



[reddit]: https://old.reddit.com/r/webdev/comments/1b14bty/netlify_just_sent_me_a_104k_bill_for_a_simple/

---

I've gone past the 100GB limit twice, when I had posts go viral -- fortunately only slightly over the limit, so I was able to do a one-off upgrade to the Pro plan rather than pay the overage charges.

---

(When I hit the limit, it's cheaper for me to do a one-off upgrade to the Pro plan than pay the overage charges.
I get 1TB of bandwidth for $19, and I just have to remember to cancel at the end of the month.
Although)

When I do hit the limit, I typically do a one-off upgrade to the Pro plan rather than paying the overage charges.
On the $19 per month Pro plan, I get 1TB of bandwidth, which is way cheaper than buying individual bandwidth packs.
Even if I forget to downgrade and I pay for two months of Pro, I'm still better-off than paying a single overage charge.

I've gone past 100GB twice, both times when I had a post go viral (one about [screenshots], one about [big PDFs][big_pdfs]).
Fortunately I've never

[pricing]: https://www.netlify.com/pricing/
[screenshots]: {% post_url 2022/2022-07-23-screenshots %}
[big_pdfs]: {% post_url 2024/2024-01-31-big-pdf %}
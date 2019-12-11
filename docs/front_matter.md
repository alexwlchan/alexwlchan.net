# Custom front matter keys

Notes on the custom front matter keys I've defined.

<dl>
  <dt>
    index.best_of (boolean)
  </dt>
  <dd>
    Whether a post is particularly special or notable.
    These posts get a red heard next to them in the post lists.
  </dd>

  <dt>
    index.exclude (boolean)
  </dt>
  <dd>
    Whether a post should be hidden from the "all posts" list.
  </dd>

  <dt>
    theme.card_type
  </dt>
  <dd>
    How to display the preview on social media (e.g. Twitter or Slack).
    The only non-default value I've used here is <code>summary_large_image</code>.
    Also requires <code>theme.image</code>.
  </dd>

  <dt>
    theme.image
  </dt>
  <dd>
    If <code>theme.card_type = summary_large_image</code>, the path to an image to use in the image preview.
  </dd>

  <dt>
    theme.minipost (boolean)
  </dt>
  <dd>
    Whether to de-emphasise the title of a post, and hide it from "recent posts" on the front page.
    Useful for shorter posts.
  </dd>
</dl>

# Stylesheets

I write all my stylesheets in SCSS.
The component SCSS files are in [`_scss`](../src/_scss), and they're pulled together in `_main.scss`.
The output is a single, minified, CSS file.

The colours and layout variables are defined in `_settings.scss`.
Note that `$primary-color` is defined as follows:

```scss
$primary-color: #d01c11 !default;
```

The `!default` marker means this variable is defined only if it isn't already defined – and I use this to produce alt-colour versions of the stylesheet.
If I add the following front matter to a post:

```yaml
theme:
  color: 6c006c
```

then I get a version of the stylesheet that uses `#6c006c` as its primary colour, and the page loads that stylesheet instead.
You can see an example [in my docopt slides][docopt_green].

The theme colour is also used in the favicon (which has to be created manually) and in the header image (which is created automatically using [specktre][specktre]).

The heavy lifting is done in [`_plugins/theming.rb`](../src/_plugins/theming.rb).

[specktre]: https://pypi.org/project/specktre/
[docopt_green]: https://alexwlchan.net/2017/09/ode-to-docopt/

## Other theming settings

In the same vein as page colour, I can override a couple of other settings in the `theme:` front matter.
Specifically:

```yaml
theme:
  card_type: summary_large_image    # If I want to change the Twitter card type
                                    # https://dev.twitter.com/cards/overview
  image: /images/2017/P5280917_2x.jpg
                                    # If I'm using summary_large_image, a path
                                    # to the image to use
  touch_icon: docopt                # Override the apple-touch-icon setting,
                                    # and the icon used in social sharing links
```

These settings are used in the template logic.
The assets get saved in the [`theme`](../src/theme) directory, and have to be created manually.

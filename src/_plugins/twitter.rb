# This is a plugin for embedding tweets that avoids using Twitter's native
# embedding.  Rendering tweets as static HTML reduces page weight, load times,
# and is resilient against tweets being deleted.
#
# The Twitter API responses and media are cached in `src/_tweets` and
# `src/_images/twitter`, respectively.  To save a tweet, run the following
# script on a machine which has Twitter API credentials in the keychain:
#
#     python scripts/save_tweet.py 'https://twitter.com/user/status/1234567890'
#
# This will save the cached response used by this plugin.
#
# To embed a tweet, place a Liquid tag of the following form anywhere in a
# source file:
#
#     {% tweet https://twitter.com/raibgovuk/status/905355951557013506 %}
#

require "rszr"


module Jekyll
  module TwitterFilters
    def render_date_created(tweet_data)
      DateTime
        .parse(tweet_data["created_at"], "%a %b %d %H:%M:%S %z %Y")
        .strftime("%-I:%M&nbsp;%p - %-d %b %Y")
    end

    def _display_path(filename)
      return "/images/twitter/#{filename}"
    end

    def tweet_img_entity_url(entity)
      filename = entity["media_url_https"].split("/").last
      _display_path(filename)
    end

    def tweet_avatar_url(tweet_data)
      screen_name = tweet_data["user"]["screen_name"]
      tweet_id = tweet_data["id_str"]
      avatar_url = tweet_data["user"]["profile_image_url_https"]
      extension = avatar_url.split(".").last  # ick
      _display_path("avatars/#{screen_name}_#{tweet_id}.#{extension}")
    end

    def render_tweet_text(tweet_data)
      text = tweet_data["text"]
      if text == nil
        text = tweet_data["full_text"]
      end

      tweet_data["entities"]["urls"].each { |u|
        text = text.sub(
          u["url"],
          "<a href=\"#{u["expanded_url"]}\">#{u["display_url"]}</a>"
        )
      }

      # Because newlines aren't significant in HTML, we convert them to
      # <br> tags so they render correctly.
      text = text.gsub("\n", "<br>")

      # Ensure user mentions (e.g. @alexwlchan) in the body of the tweet
      # are correctly rendered as links to the user page.
      tweet_data["entities"].fetch("user_mentions", []).each { |m|
        text = text.sub(
          "@#{m["screen_name"]}",
          "<a href=\"https://twitter.com/#{m["screen_name"]}\">@#{m["screen_name"]}</a>"
        )
      }

      tweet_data["entities"].fetch("hashtags", []).each { |h|
        text = text.sub(
          "##{h["text"]}",
          "<a href=\"https://twitter.com/hashtag/#{h["text"]}\">##{h["text"]}</a>"
        )
      }

      tweet_data["entities"].fetch("media", []).each { |m|
        text = text.sub(
          m["url"],
          "<a href=\"#{m["expanded_url"]}\">#{m["display_url"]}</a>"
        )
      }

      text.strip
    end
  end

  class TwitterTag < Liquid::Tag

    def initialize(tag_name, text, tokens)
      super
      @tweet_url = text.tr("\"", "").strip
      _, @screen_name, _, @tweet_id = URI.parse(@tweet_url).path.split("/")
    end

    def images_path(name)
      return "#{@src}/_images/twitter/#{name}"
    end

    def cache_file()
      "#{@src}/_tweets/#{@screen_name}_#{@tweet_id}.json"
    end

    def avatar_path(avatar_url)
      extension = avatar_url.split(".").last  # ick
      "#{@src}/_tweets/#{@screen_name}_#{@tweet_id}.#{extension}"
    end

    def create_avatar_thumbnail(avatar_url)
      path = avatar_path(avatar_url)

      FileUtils::mkdir_p "#{@dst}/images/twitter/avatars"

      # Avatars are routinely quite large (e.g. 512x512), but they're
      # only displayed in a 36x36 square (see _tweets.scss).
      #
      # Cutting a smaller thumbnail should reduce the page weight.
      thumbnail_path = "#{@dst}/images/twitter/avatars/#{File.basename(path)}"
      if not File.exists? thumbnail_path
        image = Rszr::Image.load(path)
        image.resize(108, 108)
        image.save(thumbnail_path)
      end

      # At least one of the thumbnails (a GIF) actually gets *bigger* when
      # resized.
      #
      # The whole point is to reduce the size of served files, so if that
      # happens, just use the original file.
      if File.size(thumbnail_path) > File.size(path)
        FileUtils.cp(path, thumbnail_path)
      end
    end

    def _created_at(tweet_data)
      DateTime
        .parse(tweet_data["created_at"], "%a %b %d %H:%M:%S %z %Y")
        .strftime("%-I:%M&nbsp;%p - %-d %b %Y")
    end

    def render(context)
      site = context.registers[:site]
      @src = site.config["source"]
      @dst = site.config["destination"]

      if not File.exists? cache_file()
        puts("Missing tweet; please run 'python3 scripts/save_tweet.py #{@tweet_url}'")
        exit!
      end

      tweet_data = JSON.parse(File.read(cache_file()))

      avatar_url = tweet_data["user"]["profile_image_url_https"]
      create_avatar_thumbnail(avatar_url)

      alt_text = YAML.load(File.read("#{@src}/_tweets/alt_text.yml"))
      per_tweet_alt_text = alt_text[@tweet_url]

      tpl = Liquid::Template.parse(File.open("src/_includes/tweet.html").read)

      if !tweet_data.has_key? "extended_entities"
        tweet_data["extended_entities"] = tweet_data["entities"]
      end

      # Create a UTF-8 encoded Twitter icon suitable to include as a data URI.
      # This is a bit of a hacky approach to encoding the image that lets
      # me define it as a standalone SVG file, rather than including it
      # as an already-encoded URI.
      twitter_icon_svg =
        CGI.escape(
          File.read("#{@src}/_tweets/twitter_icon.svg")
            .gsub(/\s+</, "<")
            .strip
        ).gsub("+", "%20")

      tpl.render!(
        "tweet_data" => tweet_data,
        "alt_text" => per_tweet_alt_text,
        "twitter_icon_svg" => twitter_icon_svg
      )
    end
  end
end

Liquid::Template::register_filter(Jekyll::TwitterFilters)
Liquid::Template.register_tag('tweet', Jekyll::TwitterTag)

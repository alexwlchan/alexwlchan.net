# This is a plugin for embedding tweets that avoids using Twitter's native
# embedding.  Rendering tweets as static HTML reduces page weight, load times,
# and is resilient against tweets being deleted.
#
# Auth is with a set of Twitter API keys, in a file `_tweets/auth.yml` in
# in the root of your Jekyll site.  The file should have four lines:
#
#     consumer_key: "<CONSUMER_KEY>"
#     consumer_secret: "<CONSUMER_SECRET>"
#     access_token: "<ACCESS_TOKEN>"
#     token_secret: "<TOKEN_SECRET>"
#
# Don't check in this auth file!
#
# Tweet data will be cached in `_tweets` -- you can check in these files.
#
# To embed a tweet, place a Liquid tag of the following form anywhere in a
# source file:
#
#     {% tweet https://twitter.com/raibgovuk/status/905355951557013506 %}
#

require 'fileutils'
require 'json'
require 'open-uri'
require 'twitter'


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
      _display_path("#{screen_name}_#{tweet_id}.#{extension}")
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
      @tweet_id = @tweet_url.split("/").last
    end

    def local_path(name)
      return "#{@src}/_images/twitter/#{name}"
    end

    def cache_file()
      "#{@src}/_tweets/#{@tweet_id}.json"
    end

    def avatar_path(avatar_url, screen_name)
      extension = avatar_url.split(".").last  # ick
      local_path("#{screen_name}_#{@tweet_id}.#{extension}")
    end

    def download_avatar(tweet)
      # I should really get the original using the lookup method, but
      # it kept breaking when I tried to use it.
      avatar_url = tweet.user.profile_image_url_https().to_str.sub("_normal", "")

      File.open(avatar_path(avatar_url, tweet.user.screen_name), "wb") do |saved_file|
        # the following "open" is provided by open-uri
        open(avatar_url, "rb") do |read_file|
          saved_file.write(read_file.read)
        end
      end
    end

    def download_media(tweet)
      # TODO: Add support for rendering tweets that contain more than
      # one media entity.
      raise "Too many media entities" unless tweet.media.count <= 1 || tweet.media.count == 3

      tweet.media.each { |m|

        # TODO: Add support for rendering tweets that contain different
        # types of media entities.  And check that this is supported!
        # raise "Unsupported media type" unless m.type == "photo"

        media_url = m.media_url_https

        # TODO: Use a proper url-parsing library
        name = media_url.path.split("/").last
        FileUtils::mkdir_p local_path("")
        File.open(local_path(name), "wb") do |saved_file|
          open(media_url, "rb") do |read_file|
            saved_file.write(read_file.read)
          end
        end
      }
    end

    def setup_api_client()
      auth = YAML.load(File.read("#{@src}/_tweets/auth.yml"), :safe => true)
      Twitter::REST::Client.new do |config|
        config.consumer_key        = auth["consumer_key"]
        config.consumer_secret     = auth["consumer_secret"]
        config.access_token        = auth["access_token"]
        config.access_token_secret = auth["access_secret"]
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

      if not File.exists? cache_file()
        puts("Caching #{@tweet_url}")
        client = setup_api_client()
        tweet = client.status(@tweet_url, tweet_mode: 'extended')
        json_string = JSON.pretty_generate(tweet.attrs)
        download_avatar(tweet)
        download_media(tweet)

        FileUtils::mkdir_p "#{@src}/_tweets"
        File.open(cache_file(), 'w') { |f| f.write(json_string) }
      end

      tweet_data = JSON.parse(File.read(cache_file()))

      alt_text = YAML.load(File.read("#{@src}/_tweets/alt_text.yml"), :safe => true)
      puts @tweet_url.inspec
      puts alt_text
      puts alt_text[@tweet_url].inspect
      per_tweet_alt_text = alt_text[@tweet_url]

      tpl = Liquid::Template.parse(File.open("src/_includes/tweet.html").read)
      tpl.render!("tweet_data" => tweet_data, "alt_text" => per_tweet_alt_text)
    end
  end
end

Liquid::Template::register_filter(Jekyll::TwitterFilters)
Liquid::Template.register_tag('tweet', Jekyll::TwitterTag)

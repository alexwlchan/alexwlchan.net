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
  class TwitterTag < Liquid::Tag

    def initialize(tag_name, text, tokens)
      super
      @tweet_url = text.tr("\"", "")
      @tweet_id = @tweet_url.split("/").last.strip
    end

    def local_path(name)
      return "#{@src}/_images/twitter/#{name}"
    end

    def display_path(name)
      return "/images/twitter/#{name}"
    end

    def cache_file()
      "#{@src}/_tweets/#{@tweet_id}.json"
    end

    def avatar_path(avatar_url, screen_name)
      extension = avatar_url.split(".").last  # ick
      local_path("#{screen_name}_#{@tweet_id}.#{extension}")
    end

    def display_avatar_path(avatar_url, screen_name)
      extension = avatar_url.split(".").last  # ick
      display_path("#{screen_name}_#{@tweet_id}.#{extension}")
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
      raise "Too many media entities" unless tweet.media.count <= 1

      tweet.media.each { |m|

        # TODO: Add support for rendering tweets that contain different
        # types of media entities.  And check that this is supported!
        # raise "Unsupported media type" unless m.type == "photo"

        media_url = m.media_url_https

        # TODO: Use a proper url-parsing library
        name = media_url.path.split("/").last
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

    def render(context)
      site = context.registers[:site]
      @src = site.config["source"]

      FileUtils::mkdir_p "#{@src}/_tweets"
      FileUtils::mkdir_p local_path("")

      if not File.exists? cache_file()
        puts("Caching #{@tweet_url}")
        client = setup_api_client()
        tweet = client.status(@tweet_url, tweet_mode: 'extended')
        json_string = JSON.pretty_generate(tweet.attrs)
        download_avatar(tweet)
        download_media(tweet)
        File.open(cache_file(), 'w') { |f| f.write(json_string) }
      end

      tweet_data = JSON.parse(File.read(cache_file()))

      name = tweet_data["user"]["name"]
      screen_name = tweet_data["user"]["screen_name"]
      avatar_url = tweet_data["user"]["profile_image_url_https"]

      timestamp = DateTime
        .parse(tweet_data["created_at"], "%a %b %d %H:%M:%S %z %Y")
        .strftime("%-I:%M&nbsp;%p - %-d %b %Y")

      text = tweet_data["text"] or tweet_data["full_text"]
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
      if tweet_data["entities"]["user_mentions"] != nil
        tweet_data["entities"]["user_mentions"].each { |m|
          text = text.sub(
            "@#{m["screen_name"]}",
            "<a href=\"https://twitter.com/#{m["screen_name"]}\">@#{m["screen_name"]}</a>"
          )
        }
      end

      if tweet_data["entities"]["hashtags"] != nil
        tweet_data["entities"]["hashtags"].each { |h|
          text = text.sub(
            "##{h["text"]}",
            "<a href=\"https://twitter.com/hashtag/#{h["text"]}\">##{h["text"]}</a>"
          )
        }
      end

      media_div = ""
      if tweet_data["entities"]["media"] != nil
        tweet_data["entities"]["media"].each { |m|
          filename = m["media_url_https"].split("/").last
          text = text.sub(
            m["url"],
            "<a href=\"#{m["expanded_url"]}\">#{m["display_url"]}</a>"
          )
          media_div = <<-EOD
<div class=\"media\">
  <a href="#{m["expanded_url"]}">
    <img src=\"#{display_path(filename)}\">
  </a>
</div>
EOD
          media_div = media_div.strip
        }
      end

      text = text.strip

      tweet_html = <<-EOT
<div class="tweet">
  <blockquote>#{media_div}
    <div class="header">
      <div class="author">
        <a class="link link_blend" href="https://twitter.com/#{screen_name}">
          <span class="avatar">
            <img src="#{display_avatar_path(avatar_url, screen_name)}">
          </span>
          <span class="name" title="#{name}">#{name}</span>
          <span class="screen_name" title="@#{screen_name}">@#{screen_name}</span>
        </a>
      </div>
    </div>
    <div class="body">
      <p class="text">#{text}</p>
      <div class="metadata">
        <a class="link_blend" href="https://twitter.com/#{screen_name}/status/#{@tweet_id}">#{timestamp}</a>
      </div>
    </div>
  </blockquote>
</div>
EOT
      tweet_html.lines.map { |line| line.strip }.join("")
    end
  end
end

Liquid::Template.register_tag('tweet', Jekyll::TwitterTag)

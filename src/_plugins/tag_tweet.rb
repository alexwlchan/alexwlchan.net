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

require 'base64'
require 'rszr'

require_relative 'utils/twitter'

METADATA_SCHEMA = {
  type: 'object'
}

module Jekyll
  module TwitterFilters
    def render_date_created(tweet_data)
      DateTime
        .parse(tweet_data['created_at'], '%a %b %d %H:%M:%S %z %Y')
        .strftime('%-I:%M&nbsp;%p - %-d %b %Y')
    end

    def _display_path(filename)
      "/images/twitter/#{filename}"
    end

    def replace_twemoji(text)
      replace_twemoji_with_images(text)
    end

    # Create a data URI for this tweet avatar.
    #
    # These images are tiny when resized properly – in most cases <4KB,
    # so it's faster to embed them as base64-encoded images than serve
    # them as a separate network request.
    def tweet_avatar_url(tweet_data)
      screen_name = tweet_data['user']['screen_name']
      tweet_id = tweet_data['id_str']

      avatar_url = tweet_data['user']['profile_image_url_https']
      extension = avatar_url.split('.').last # ick

      path = "src/_tweets/avatars/#{screen_name}_#{tweet_id}.#{extension}"

      FileUtils.mkdir_p '.jekyll-cache/twitter/avatars'

      # Avatars are routinely quite large (e.g. 512x512), but they're
      # only displayed in a 36x36 square (see _tweets.scss).
      #
      # Cutting a smaller thumbnail should reduce the page weight.
      thumbnail_path = ".jekyll-cache/twitter/avatars/#{File.basename(path)}"

      unless File.exist? thumbnail_path
        image = Rszr::Image.load(path)
        image.resize(108, 108).save(thumbnail_path)
      end

      thumbnail_data = Base64.encode64(File.read(thumbnail_path))

      case extension
      when 'png'
        "data:image/png;base64,#{thumbnail_data}"
      when 'jpg', 'jpeg'
        "data:image/jpeg;base64,#{thumbnail_data}"
      else
        raise "Unrecognised avatar extension: #{avatar_url} / #{extension}"
      end
    end

    def render_tweet_text(tweet_data)
      text = tweet_data['text']
      text = tweet_data['full_text'] if text.nil?

      tweet_data['entities']['urls'].each do |u|
        text = text.sub(
          u['url'],
          "<a href=\"#{u['expanded_url']}\">#{u['display_url']}</a>"
        )
      end

      # Because newlines aren't significant in HTML, we convert them to
      # <br> tags so they render correctly.
      text = text.gsub("\n", '<br>')

      # Ensure user mentions (e.g. @alexwlchan) in the body of the tweet
      # are correctly rendered as links to the user page.
      tweet_data['entities'].fetch('user_mentions', []).each do |m|
        text = text.sub(
          "@#{m['screen_name']}",
          "<a href=\"https://twitter.com/#{m['screen_name']}\">@#{m['screen_name']}</a>"
        )
      end

      tweet_data['entities'].fetch('hashtags', []).each do |h|
        text = text.sub(
          "##{h['text']}",
          "<a href=\"https://twitter.com/hashtag/#{h['text']}\">##{h['text']}</a>"
        )
      end

      tweet_data['entities'].fetch('media', []).each do |m|
        text = text.sub(
          m['url'],
          "<a href=\"#{m['expanded_url']}\">#{m['display_url']}</a>"
        )
      end

      text.strip
    end

    def tweet_image(media)
      expanded_url = media['expanded_url']
      alt_text = media['ext_alt_text']

      filename = File.basename(media['media_url_https'])

      <<~HTML
        <a href="#{expanded_url}">
          {%
            picture
            filename="#{filename}"
            parent="/images/twitter"
            #{alt_text.nil? ? 'data-proofer-ignore' : "alt=\"#{alt_text}\""}
            width="496"
          %}
        </a>
      HTML
    end
  end

  class TwitterTag < Liquid::Tag
    def initialize(tag_name, text, tokens)
      super
      @tweet_url = text.tr('"', '').strip
      _, @screen_name, _, @tweet_id = URI.parse(@tweet_url).path.split('/')
    end

    def images_path(name)
      "#{@src}/_images/twitter/#{name}"
    end

    def cache_file
      "#{@src}/_tweets/posts/#{@screen_name}_#{@tweet_id}.json"
    end

    def _created_at(tweet_data)
      DateTime
        .parse(tweet_data['created_at'], '%a %b %d %H:%M:%S %z %Y')
        .strftime('%-I:%M&nbsp;%p - %-d %b %Y')
    end

    # Read metadata about a tweet from the `src/_tweets/data` folder.
    #
    # This method will throw an error if:
    #
    #   1. It can't find the metadata, or
    #   2. The metadata doesn't match the schema
    #
    def read_tweet_data
      unless File.exist? cache_file
        raise "Unable to find cached data for #{@tweet_url}!"
      end

      tweet_data = JSON.parse(File.read(cache_file))

      unless tweet_data.key? 'extended_entities'
        tweet_data['extended_entities'] = tweet_data['entities']
      end

      errors = JSON::Validator.fully_validate(METADATA_SCHEMA, tweet_data)

      unless errors.empty?
        raise "Tweet metadata in #{cache_file} does not match schema: #{errors}"
      end

      tweet_data
    end

    def render(context)
      site = context.registers[:site]
      @src = site.config['source']
      @dst = site.config['destination']

      tweet_data = read_tweet_data

      tpl = Liquid::Template.parse(File.read('src/_includes/tweet.html'))

      input = tpl.render!(
        'tweet_data' => tweet_data
      )

      # We have to run it through the site's Markdown converter after
      # rendering the initial HTML, so we have access to the picture plugin.
      Liquid::Template.parse(input).render!(context)
    end
  end
end

Liquid::Template.register_filter(Jekyll::TwitterFilters)
Liquid::Template.register_tag('tweet', Jekyll::TwitterTag)

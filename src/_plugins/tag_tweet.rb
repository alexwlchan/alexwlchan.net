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
  type: 'object',
  properties: {
    text: { type: 'string' },
    user: {
      type: 'object',
      properties: {
        name: { type: 'string' },
        screen_name: { type: 'string' }
      },
      required: %w[name screen_name],
      additionalProperties: false
    },
    entities: {
      description: 'Non-textual elements of the tweet',
      type: 'object',
      properties: {
        hashtags: {
          type: 'array',
          items: {
            type: 'object',
            required: %w[text],
            properties: {
              text: { type: 'string' }
            },
            additionalProperties: false
          }
        },
        media: {
          type: 'array',
          items: {
            type: 'object',
            required: %w[expanded_url display_url],
            properties: {
              expanded_url: { type: 'string' },
              display_url: { type: 'string' }
            }
          }
        },
        user_mentions: {
          type: 'array',
          items: {
            type: 'object',
            required: %w[screen_name],
            properties: {
              screen_name: { type: 'string' }
            },
            additionalProperties: false
          }
        },
        urls: {
          type: 'array',
          items: {
            type: 'object',
            required: %w[expanded_url url display_url],
            properties: {
              expanded_url: { type: 'string' },
              url: { type: 'string' },
              display_url: { type: 'string' }
            },
            additionalProperties: false
          }
        }
      }
    },
    quoted_status: {
      type: 'object',
      properties: {
        text: { type: 'string' }
      }
    }
  },
  required: %w[text user]
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
    #
    # Each avatar is identified with both the screen name and tweet ID,
    # so I capture the avatar as it looked at the time of the tweet,
    # similar to if I'd taken a tweet screenshot.
    def tweet_avatar_url(tweet_data)
      screen_name = tweet_data['user']['screen_name']
      tweet_id = tweet_data['id_str']

      # Find the matching avatar.  Each avatar should be labelled with
      # the screen name and tweet ID, but may be one of several formats.
      matching_avatars = Dir.glob("src/_tweets/avatars/#{screen_name}_#{tweet_id}.*")

      unless matching_avatars.length == 1
        raise "Could not find avatar for tweet, expected #{screen_name}_#{tweet_id}.*"
      end

      path = matching_avatars[0]
      extension = path.split('.').last # ick

      # Avatars are routinely quite large (e.g. 512x512), but they're
      # only displayed in a 36x36 square (see _tweets.scss).
      #
      # Cutting a smaller thumbnail should reduce the page weight.
      FileUtils.mkdir_p '.jekyll-cache/twitter/avatars'
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

    # Render the text of the tweet as HTML.
    #
    # This includes:
    #
    #     * Expanding any newlines
    #     * Replacing URLs and @-mentions
    #     * Replacing native emoji with Twitter's "twemoji" SVGs
    #
    def render_tweet_text(tweet_data)
      text = tweet_data['text']

      entities = tweet_data.fetch('entities', {})

      # Expand any t.co URLs in the text with the actual link, which means
      # those links don't rely on Twitter or their link shortener.
      entities.fetch('urls', []).each do |u|
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
      entities.fetch('user_mentions', []).each do |m|
        text = text.sub(
          "@#{m['screen_name']}",
          "<a href=\"https://twitter.com/#{m['screen_name']}\">@#{m['screen_name']}</a>"
        )
      end

      entities.fetch('hashtags', []).each do |h|
        text = text.sub(
          "##{h['text']}",
          "<a href=\"https://twitter.com/hashtag/#{h['text']}\">##{h['text']}</a>"
        )
      end

      entities.fetch('media', []).each do |m|
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

      # The `text` variable should contain the tweet URL, e.g.
      #
      #     https://twitter.com/NatlParkService/status/1767630582299631623
      #       ~> username = "NatlParkService", id = "1767630582299631623".
      #
      # Note that `text` may contain trailing whitespace.
      #
      # Note also that the `username` regex may be incomplete.
      #
      pattern = %r{^https://twitter\.com/(?<screen_name>[A-Za-z0-9_]+)/status/(?<id>[0-9]+)$}
      m = text.strip.match(pattern)

      if m.nil?
        raise "Unable to parse URL: #{text.inspect}"
      end

      @tweet_url = text
      @screen_name = m[:screen_name]
      @tweet_id = m[:id]
    end

    # Where is metadata about this tweet?
    #
    # Example path:
    #
    #     src/_tweets/posts/alexwlchan_924569032170397696.json
    #
    # Theoretically I could just use the numeric tweet ID because
    # they're globally unique, but having it in the filename is
    # useful when I'm trying to find a tweet.
    #
    def metadata_file_path
      "#{@src}/_tweets/posts/#{@screen_name}_#{@tweet_id}.json"
    end

    # Read metadata about a tweet from the `src/_tweets/data` folder.
    #
    # This method will throw an error if:
    #
    #   1. It can't find the metadata, or
    #   2. The metadata doesn't match the schema
    #
    def read_tweet_data
      begin
        tweet_data = JSON.parse(File.read(metadata_file_path))
      rescue Errno::ENOENT
        raise "Unable to find metadata for #{@tweet_url}! (Expected #{metadata_file_path})"
      end

      unless tweet_data.key? 'extended_entities'
        tweet_data['extended_entities'] = tweet_data['entities']
      end

      errors = JSON::Validator.fully_validate(METADATA_SCHEMA, tweet_data)

      unless errors.empty?
        raise "Tweet data in #{metadata_file_path} does not match schema: #{errors}"
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

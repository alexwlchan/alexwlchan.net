# This is a plugin for embedding tweets that avoids using Twitter's native
# embedding.  Rendering tweets as static HTML reduces page weight, load times,
# and is resilient against tweets being deleted.
#
# To embed a tweet, place a Liquid tag of the following form anywhere in a
# source file:
#
#     {% tweet https://twitter.com/raibgovuk/status/905355951557013506 %}
#
# and save the relevant images/metadata in `src/_tweets`.
#

require 'json-schema'

require_relative 'utils/create_base64_avatar'
require_relative 'utils/twitter'

METADATA_SCHEMA = {
  type: 'object',
  properties: {
    id: { type: 'string' },
    text: { type: 'string' },
    created_at: { type: 'string' },
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
            required: %w[filename expanded_url type],
            properties: {
              filename: { type: 'string' },
              expanded_url: { type: 'string' },
              ext_alt_text: { type: 'string' },
              type: { const: 'photo' }
            },
            additionalProperties: false
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
        id: { type: 'string' },
        text: { type: 'string' },
        created_at: { type: 'string' },
        user: {
          type: 'object',
          properties: {
            name: { type: 'string' },
            screen_name: { type: 'string' }
          },
          required: %w[name screen_name],
          additionalProperties: false
        }
      },
      required: %w[id text created_at user]
    }
  },
  additionalProperties: false,
  required: %w[id text created_at user]
}

module Jekyll
  module TwitterFilters
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
      tweet_id = tweet_data['id']

      Jekyll::Cache.new('TweetAvatars').getset(tweet_id) do
        screen_name = tweet_data['user']['screen_name']

        # Find the matching avatar.  Each avatar should be labelled with
        # the screen name and tweet ID, but may be one of several formats.
        matching_avatars = Dir.glob("src/_tweets/avatars/#{screen_name}_#{tweet_id}.*")

        unless matching_avatars.length == 1
          raise "Could not find avatar for tweet, expected #{screen_name}_#{tweet_id}.*"
        end

        path = matching_avatars[0]

        create_base64_avatar(path, 108)
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

      text.strip
    end

    def tweet_image(media)
      alt_text = media['ext_alt_text']

      <<~HTML
        <a href="#{media['expanded_url']}">
          {%
            picture
            filename="#{media['filename']}"
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

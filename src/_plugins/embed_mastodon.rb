# This is a plugin for embedding toots that avoids using Mastodon's native
# embedding.  Rendering toots as static HTML reduces page weight, load times,
# and is resilient against toots being deleted.
#
# To embed a toot, place a Liquid tag of the following form anywhere in a
# source file:
#
#     {% mastodon https://code4lib.social/@linguistory/113924700205617006 %}
#
# and save the relevant images/metadata in `src/_mastodon`.
#

require 'json-schema'

require_relative 'utils/create_base64_avatar'

MASTODON_METADATA_SCHEMA = {
  type: 'object',
  properties: {
    id: { type: 'string' },
    text: { type: 'string' },
    created_at: { type: 'string' },
    user: {
      type: 'object',
      properties: {
        server: { type: 'string' },
        display_name: { type: 'string' },
        username: { type: 'string' }
      },
      required: %w[server display_name username],
      additionalProperties: false
    },
    entities: {
      description: 'Non-textual elements of the tweet',
      type: 'object',
      properties: {
        hashtags: {
          type: 'array',
          items: {
            type: 'string'
          }
        },
        user_mentions: {
          type: 'array',
          items: {
            type: 'object',
            properties: {
              label: { type: 'string' },
              profile_url: { type: 'string' }
            },
            required: %w[label profile_url],
            additionalProperties: false
          }
        },
        urls: {
          type: 'array',
          items: {
            type: 'object',
            properties: {
              url: { type: 'string' },
              display_url: { type: 'string' }
            },
            required: %w[url display_url],
            additionalProperties: false
          }
        }
      }
    }
  },
  additionalProperties: false,
  required: %w[id text created_at user]
}

module Jekyll
  module MastodonFilters
    def _display_path(filename)
      "/images/mastodon/#{filename}"
    end

    # Create a data URI for this toot avatar.
    #
    # These images are tiny when resized properly – in most cases <4KB,
    # so it's faster to embed them as base64-encoded images than serve
    # them as a separate network request.
    #
    # Each avatar is identified with both the screen name and toot ID,
    # so I capture the avatar as it looked at the time of the toot,
    # similar to if I'd taken a toot screenshot.
    def toot_avatar_url(toot_data)
      toot_id = toot_data['id']

      Jekyll::Cache.new('MastodonAvatars').getset(toot_id) do
        screen_name = toot_data['user']['username']

        # Find the matching avatar.  Each avatar should be labelled with
        # the screen name and toot ID, but may be one of several formats.
        matching_avatars = Dir.glob("src/_embeds/mastodon/avatars/#{screen_name}_#{toot_id}.*")

        unless matching_avatars.length == 1
          raise "Could not find avatar for toot, expected #{screen_name}_#{toot_id}.*"
        end

        path = matching_avatars[0]

        create_base64_avatar(path, 92)
      end
    end

    # Render the text of the toot as HTML.
    #
    # This includes:
    #
    #     * Expanding any newlines
    #     * Adding hashtags
    #
    def render_toot_text(toot_data)
      text = toot_data['text']

      server = toot_data['user']['server']

      # Because newlines aren't significant in HTML, we convert them to
      # <br> tags so they render correctly.
      text = text.gsub("\n", '<br>')

      toot_data['entities'].fetch('hashtags', []).each do |h|
        text = text.sub(
          "##{h}",
          "<a href=\"https://#{server}/tags/#{h}\">##{h}</a>"
        )
      end

      toot_data['entities'].fetch('urls', []).each do |u|
        text = text.sub(
          u['url'],
          "<a href=\"#{u['url']}\">#{u['display_url']}</a>"
        )
      end

      toot_data['entities'].fetch('user_mentions', []).each do |u|
        text = text.sub(
          "@#{u['label']}",
          "<a href=\"#{u['profile_url']}\">@#{u['label']}</a>"
        )
      end

      text.strip
    end
  end

  class MastodonTag < Liquid::Tag
    def initialize(tag_name, text, tokens)
      super

      # The `text` variable should contain the toot URL, e.g.
      #
      #     https://code4lib.social/@linguistory/113924700205617006
      #       ~> server   = "code4lib.social",
      #          username = "linguistory"
      #          id       = "1767630582299631623".
      #
      # Note that `text` may contain trailing whitespace.
      #
      # Note also that the `username` regex may be incomplete.
      #
      pattern = %r{^https://(?<server>[a-z0-9\.]+)/@(?<username>[A-Za-z0-9_]+)/(?<id>[0-9]+)$}
      m = text.strip.match(pattern)

      if m.nil?
        raise "Unable to parse URL: #{text.inspect}"
      end

      @toot_url = text
      @username = m[:username]
      @toot_id = m[:id]
    end

    # Where is metadata about this toot?
    #
    # Example path:
    #
    #     src/_embeds/mastodon/data/alexwlchan_924569032170397696.json
    #
    # Theoretically I could just use the numeric toot ID because
    # they're globally unique, but having it in the filename is
    # useful when I'm trying to find a toot.
    #
    def metadata_file_path
      "#{@src}/_embeds/mastodon/data/#{@username}_#{@toot_id}.json"
    end

    # Read metadata about a toot from the `src/_toots/data` folder.
    #
    # This method will throw an error if:
    #
    #   1. It can't find the metadata, or
    #   2. The metadata doesn't match the schema
    #
    def read_toot_data
      begin
        toot_data = JSON.parse(File.read(metadata_file_path))
      rescue Errno::ENOENT
        raise "Unable to find metadata for #{@toot_url}! (Expected #{metadata_file_path})"
      end

      errors = JSON::Validator.fully_validate(MASTODON_METADATA_SCHEMA, toot_data)

      unless errors.empty?
        raise "Toot data in #{metadata_file_path} does not match schema: #{errors}"
      end

      toot_data
    end

    def render(context)
      site = context.registers[:site]
      @src = site.config['source']
      @dst = site.config['destination']

      toot_data = read_toot_data

      tpl = Liquid::Template.parse(File.read('src/_includes/embeds/mastodon.html'))

      input = tpl.render!(
        'toot_data' => toot_data
      )

      # We have to run it through the site's Markdown converter after
      # rendering the initial HTML, so we have access to the picture plugin.
      Liquid::Template.parse(input).render!(context)
    end
  end
end

Liquid::Template.register_filter(Jekyll::MastodonFilters)
Liquid::Template.register_tag('mastodon', Jekyll::MastodonTag)

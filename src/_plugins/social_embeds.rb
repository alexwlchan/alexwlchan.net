# This is a plugin for embedding social media posts that avoids using
# native embeds. Rendering posts as static HTML reduces page weight,
# load times, and is resilient against posts being deleted.
#
# To embed a post, use a Liquid tag of the form:
#
#     {% mastodon https://code4lib.social/@linguistory/113924700205617006 %}
#

require_relative 'utils/twitter'

module Jekyll
  module SocialEmbedFilters
    # Create a data URI for the avatar.
    #
    # These images are tiny when resized properly – in most cases <4KB,
    # so it's faster to embed them as base64-encoded images than serve
    # them as a separate network request.
    def avatar_url(post_data)
      # Avatars are stored in the _images/social_embeds/avatars directory,
      # combining the site, user ID, and post ID.
      case post_data['site']
      when 'mastodon'
        user_id = post_data['author']['username']
        post_id = post_data['id']
      when 'twitter'
        user_id = post_data['author']['screen_name']
        post_id = post_data['id']
      when 'bluesky'
        user_id = post_data['author']['handle']
        post_id = post_data['id']
      else
        raise "Unrecognised site: #{post_data['site']}"
      end

      avatar_id = "#{user_id}_#{post_id}"

      Jekyll::Cache.new('SocialEmbedAvatars').getset(avatar_id) do
        # Find the matching avatar, which may be one of several formats.
        matching_avatars = Dir.glob("src/_images/social_embeds/avatars/#{avatar_id}*")

        unless matching_avatars.length == 1
          raise "Could not find avatar for #{avatar_id}"
        end

        avatar_path = matching_avatars[0]
        create_base64_avatar(avatar_path, 92)
      end
    end

    # render_mastodon_text renders the text of a Mastodon post as HTML.
    #
    # This includes:
    #
    #   - Expanding newlines
    #   - Adding hashtags
    #
    def render_mastodon_text(post_data)
      # Newlines aren't significant in HTML; convert them to <br> tags.
      text = post_data['text']
      text = text.gsub("\n", '<br>')

      # Replace any hashtags with links to the server.
      server = post_data['author']['server']
      entities = post_data.fetch('entities', {})
      entities.fetch('hashtags', []).each do |h|
        text = text.sub(
          "##{h}",
          "<a href=\"https://#{server}/tags/#{h}\">##{h}</a>"
        )
      end

      # Replace any URLs with their display versions.
      entities.fetch('urls', []).each do |u|
        text = text.sub(
          u['url'],
          "<a href=\"#{u['url']}\">#{u['display_url']}</a>"
        )
      end

      # Replace any user mentions with links to the username.
      entities.fetch('user_mentions', []).each do |u|
        text = text.sub(
          "@#{u['label']}",
          "<a href=\"#{u['profile_url']}\">@#{u['label']}</a>"
        )
      end

      text.strip
    end

    # tweet_image creates a {% picture %} tag to show a media item
    # on a tweet.
    def tweet_image(media)
      alt_text = media['ext_alt_text']

      <<~HTML
        <a href="#{media['url']}">
          {%
            picture
            filename="#{media['filename']}"
            parent="/images/social_embeds/twitter"
            #{alt_text.nil? ? 'data-proofer-ignore' : "alt=\"#{alt_text}\""}
            width="585"
          %}
        </a>
      HTML
    end

    # render_tweet_text renders the text of a tweet as HTML.
    #
    # This includes:
    #
    #     * Expanding any newlines
    #     * Replacing URLs and @-mentions
    #     * Replacing native emoji with Twitter's "twemoji" SVGs
    #
    def render_tweet_text(post_data)
      text = post_data['text']

      entities = post_data.fetch('entities', {})

      # Expand any t.co URLs in the text with the actual link, which means
      # those links don't rely on Twitter or their link shortener.
      entities.fetch('urls', []).each do |u|
        text = text.sub(
          u['url'],
          "<a href=\"#{u['url']}\">#{u['display_url']}</a>"
        )
      end

      # Because newlines aren't significant in HTML, we convert them to
      # <br> tags so they render correctly.
      text = text.gsub("\n", '<br>')

      # Ensure user mentions (e.g. @alexwlchan) in the body of the tweet
      # are correctly rendered as links to the user page.
      entities.fetch('user_mentions', []).each do |um|
        text = text.sub(
          "@#{um}",
          "<a href=\"https://twitter.com/#{um}\">@#{um}</a>"
        )
      end

      entities.fetch('hashtags', []).each do |h|
        text = text.sub(
          "##{h}",
          "<a href=\"https://twitter.com/hashtag/#{h}\">##{h}</a>"
        )
      end

      text.strip
    end

    def replace_twemoji(text)
      replace_twemoji_with_images(text)
    end
  end
end

def create_base64_avatar(path, size)
  require 'base64'
  require 'vips'

  im = Vips::Image.new_from_file path

  if im.width != im.height
    raise "Avatar is not square: #{path}"
  end

  # Resize the image to match the target size
  scale = size.to_f / im.width
  resized = im.resize(scale)

  # Now write the image to a buffer, and convert it to base64.
  #
  # We preserve the original format, which is likely to be the most
  # efficient encoding for this image.
  case im.get 'vips-loader'
  when 'jpegload'
    jpeg_bytes = resized.write_to_buffer('.jpg')
    base64_string = Base64.strict_encode64(jpeg_bytes)
    "data:image/jpeg;base64,#{base64_string}"
  when 'pngload'
    png_bytes = resized.write_to_buffer('.png')
    base64_string = Base64.strict_encode64(png_bytes)
    "data:image/png;base64,#{base64_string}"
  else
    raise "Unrecognised vips loader for #{path}: #{im.get 'vips-loader'}"
  end
end

class SocialMedia < Liquid::Tag
  def initialize(_tag_name, text, _tokens)
    # The `text` variable should contain the URL of the post.
    @post_url = text.strip.delete_prefix('"').delete_suffix('"')
  end

  def render(context)
    # Look up the data for this post in `src/_data/social_embeds.json`,
    # which is keyed by the URL.
    site = context.registers[:site]
    post_data = site.data['social_embeds'][@post_url]

    if post_data.nil?
      raise "Could not find data for URL: #{@post_url}"
    end

    tpl = Liquid::Template.parse(
      File.read("src/_includes/embeds/#{post_data['site']}.html")
    )

    input = tpl.render!(
      'post_url' => @post_url,
      'post_data' => post_data
    )

    # Run it through the site's Markdown converter after rendering
    # the initial HTML, so we have access to the picture plugin.
    Liquid::Template.parse(input).render!(context)
  end
end

Liquid::Template.register_filter(Jekyll::SocialEmbedFilters)
Liquid::Template.register_tag('bluesky', SocialMedia)
Liquid::Template.register_tag('mastodon', SocialMedia)
Liquid::Template.register_tag('tweet', SocialMedia)
Liquid::Template.register_tag('youtube', SocialMedia)

require 'base64'

def replace_twemoji_with_images(text)
  # This replaces emoji in tweets with their "twemoji" counterparts.
  #
  # Rather than record the entire twemoji set here, I just have a
  # hard-coded set of rules for the twemoji I know I'm using.
  twemoji = {
    '😎' => '1f60e.svg',
    '👌' => '1f44c.svg',
    '🐦' => '1f426.svg',
    '💻' => '1f4bb.svg',
    '🥳' => '1f973.svg',
    # NOTE: this is a surfer emoji with skin tone/gender modifiers
    '🏄🏻‍♂️' => '1f3c4-1f3fb-200d-2642-fe0f.svg',
    '📈' => '1f4c8.svg',
    '💞' => '1f49e.svg',
    '🧵' => '1f9f5.svg',
    '✨' => '2728.svg'
  }

  twemoji.each do |orig, svg_name|
    base64_string = Base64.encode64(
      File.binread("src/_images/social_embeds/twemoji/#{svg_name}")
    ).strip
    data_uri = "data:image/svg+xml;base64,#{base64_string}"

    # Construct the <img> tag.  Notes:
    #
    #   - the `twemoji` class is used for styling
    #   - the `width`/`height` attributes are meant for when styles don't load
    #     properly -- they stop the emoji completely blowing up in size.
    #
    text = text.gsub(
      orig,
      <<~HTML
        <img class="twemoji" width="20px" height="20px" alt="#{orig}" src="#{data_uri}"/>
      HTML
    ).strip
  end

  text
end

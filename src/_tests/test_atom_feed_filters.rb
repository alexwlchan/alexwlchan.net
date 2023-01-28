require 'test/unit'

require 'nokogiri'

require_relative '../_plugins/atom_feed_filters'

class HtmlModifiersTest < Test::Unit::TestCase
  def test_fix_tweets_for_rss
    html = <<~HTML
      <p>Yesterday evening, Kate posted this tweet:</p>
      <div class="tweet">
        <blockquote>
          <div class="header">
            <div class="twitter_birb" role="presentation">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" width="20px" height="20px">
                <path fill="none" d="M0 0h72v72H0z" />
                <path class="icon" fill="#1da1f2" d="M68.812 15.14c-2.348 1.04-4.87 1.744-7.52 2.06 2.704-1.62 4.78-4.186 5.757-7.243-2.53 1.5-5.33 2.592-8.314 3.176C56.35 10.59 52.948 9 49.182 9c-7.23 0-13.092 5.86-13.092 13.093 0 1.026.118 2.02.338 2.98C25.543 24.527 15.9 19.318 9.44 11.396c-1.125 1.936-1.77 4.184-1.77 6.58 0 4.543 2.312 8.552 5.824 10.9-2.146-.07-4.165-.658-5.93-1.64-.002.056-.002.11-.002.163 0 6.345 4.513 11.638 10.504 12.84-1.1.298-2.256.457-3.45.457-.845 0-1.666-.078-2.464-.23 1.667 5.2 6.5 8.985 12.23 9.09-4.482 3.51-10.13 5.605-16.26 5.605-1.055 0-2.096-.06-3.122-.184 5.794 3.717 12.676 5.882 20.067 5.882 24.083 0 37.25-19.95 37.25-37.25 0-.565-.013-1.133-.038-1.693 2.558-1.847 4.778-4.15 6.532-6.774z" />
              </svg>
            </div>
            <div class="author">
              <a class="link link_blend" href="https://twitter.com/thingskatedid">
                <span class="avatar">
                  <img src="/images/twitter/avatars/thingskatedid_1573017572022571009.jpg" alt="Profile picture for @thingskatedid">
                </span>
                <span class="name" title="Kate">Kate</span>
                <span class="screen_name" title="@thingskatedid">@thingskatedid</span>
              </a>
            </div>
          </div>
          <div class="body">
            <p class="text">i don't *care* how maths works, half of zero should be 0.5</p>
            <div class="metadata">
              <a class="link_blend" href="https://twitter.com/thingskatedid/status/1573017572022571009">6:33&nbsp;PM - 22 Sep 2022</a>
            </div>
          </div>
        </blockquote>
      </div>
    HTML

    expected = <<~HTML
      <p>Yesterday evening, Kate posted this tweet:</p>
      <div class="tweet">
        <blockquote>
          <div class="header">
            <div class="author">
              <a class="link link_blend" href="https://twitter.com/thingskatedid">
                <span class="name" title="Kate">Kate</span>
                <span class="screen_name" title="@thingskatedid">@thingskatedid</span>
              </a>
            </div>
          </div>
          <div class="body">
            <p class="text">i don't *care* how maths works, half of zero should be 0.5</p>
            <div class="metadata">
              <a class="link_blend" href="https://twitter.com/thingskatedid/status/1573017572022571009">6:33&nbsp;PM - 22 Sep 2022</a>
            </div>
          </div>
        </blockquote>
      </div>
    HTML

    doc = Nokogiri::HTML.fragment(html)
    HtmlModifiers.fix_tweets_for_rss(doc)

    assert_equal_html(doc, expected)
  end

  def assert_equal_html(doc, html)
    assert_equal(doc.to_s.gsub(/\n\s*\n/, "\n"), Nokogiri::HTML.fragment(html).to_s.gsub(/\n\s*\n/, "\n"))
  end
end

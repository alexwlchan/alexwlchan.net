# frozen_string_literal: true

require 'test/unit'

require_relative '../_plugins/cleanup_text'

class TextCleanupText < Test::Unit::TestCase
  def test_it_adds_non_breaking_spaces_after_words
    text = 'Apollo 11 launched in 1969'
    expected = 'Apollo&nbsp;11 launched in 1969'
    assert_equal(add_non_breaking_spaces(text), expected)
  end

  def test_it_adds_non_breaking_spaces_before_words
    text = 'It takes 2 minutes'
    expected = 'It takes 2&nbsp;minutes'
    assert_equal(add_non_breaking_spaces(text), expected)
  end

  def test_non_breaking_space_at_start_of_anchor
    text = '<a href="https://kottke.org/">a different set of circles</a>'
    expected = '<a href="https://kottke.org/">a&nbsp;different set of circles</a>'
    assert_equal(add_non_breaking_spaces(text), expected)
  end

  def test_preserves_language_console
    text = '<div class="language-console highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="gp">$</span><span class="w"> </span>youtube-dl <span class="nt">--write-auto-sub</span> <span class="nt">--skip-download</span> <span class="s2">"https://www.youtube.com/watch?v=XyGVRlRyT-E"</span>
</code></pre></div></div>'
    expected = '<div class="language-console"><div class="highlight"><pre class="highlight"><code><span class="gp">$</span><span class="w"> </span>youtube-dl <span class="nt">--write-auto-sub</span> <span class="nt">--skip-download</span> <span class="s2">"https://www.youtube.com/watch?v=XyGVRlRyT-E"</span>
</code></pre></div></div>'
    assert_equal(cleanup_syntax_highlighter_classes(text), expected)
  end

  def test_preserves_language_go
    text = '<div class="language-go highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">package</span> <span class="n">main</span></code></pre></div></div>'
    expected = '<div class="language-go"><div class="highlight"><pre class="highlight"><code><span class="k">package</span> <span class="n">main</span></code></pre></div></div>'
    assert_equal(cleanup_syntax_highlighter_classes(text), expected)
  end

  def test_discards_other_language_tags
    text = '<code class="language-plaintext highlighter-rouge">number_of_sides</code>'
    expected = '<code>number_of_sides</code>'
    assert_equal(cleanup_syntax_highlighter_classes(text), expected)
  end
end

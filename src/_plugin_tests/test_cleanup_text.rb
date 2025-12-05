# frozen_string_literal: true

require 'test/unit'

require_relative '../_plugins/cleanup_text'

class TextCleanupText < Test::Unit::TestCase
  def test_it_adds_non_breaking_spaces_after_words
    text = 'Apollo 11 launched in 1969'
    expected = 'Apollo&nbsp;11 launched in 1969'
    assert_equal(cleanup_whitespace(text), expected)
  end

  def test_it_adds_non_breaking_spaces_before_words
    text = 'It takes 2 minutes'
    expected = 'It takes 2&nbsp;minutes'
    assert_equal(cleanup_whitespace(text), expected)
  end

  def test_non_breaking_space_at_start_of_anchor
    text = '<a href="https://kottke.org/">a different set of circles</a>'
    expected = '<a href="https://kottke.org/">a&nbsp;different set of circles</a>'
    assert_equal(cleanup_whitespace(text), expected)
  end

  def test_thinsp_around_times
    text = '100×200'
    expected = '100&#8239;×&#8239;200'
    assert_equal(cleanup_whitespace(text), expected)
  end

  def test_preserves_language_console
    text = '<div class="language-console highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="gp">$</span><span class="w"> </span>youtube-dl <span class="nt">--write-auto-sub</span> <span class="nt">--skip-download</span> <span class="s2">"https://www.youtube.com/watch?v=XyGVRlRyT-E"</span>
</code></pre></div></div>'
    expected = '<pre class="language-console"><code><span class="gp">$</span><span class="w"> </span>youtube-dl <span class="nt">--write-auto-sub</span> <span class="nt">--skip-download</span> <span class="s2">"https://www.youtube.com/watch?v=XyGVRlRyT-E"</span>
</code></pre>'
    assert_equal(cleanup_syntax_highlighter_classes(text), expected)
  end

  def test_preserves_language_go
    text = '<div class="language-go highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">package</span> <span class="n">main</span></code></pre></div></div>'
    expected = '<pre class="language-go"><code><span class="k">package</span> <span class="n">main</span></code></pre>'
    assert_equal(cleanup_syntax_highlighter_classes(text), expected)
  end

  def test_discards_other_language_tags_in_pre
    text = '<div class="language-python highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="nx">module</span> <span class="s2">"important_bukkit"</span> <span class="p">{</span></pre></div></div>'
    expected = '<pre><code><span class="nx">module</span> <span class="s2">"important_bukkit"</span> <span class="p">{</span></pre>'
    assert_equal(cleanup_syntax_highlighter_classes(text), expected)
  end

  def test_discards_other_language_tags_in_code
    text = '<code class="language-plaintext highlighter-rouge">number_of_sides</code>'
    expected = '<code>number_of_sides</code>'
    assert_equal(cleanup_syntax_highlighter_classes(text), expected)
  end

  def test_handles_highlight_inside_list
    text = <<HTML
    <ul>
      <li>
        <p>To get the filename that curl will write a file to, use <code class="language-plaintext highlighter-rouge">--write-out</code> with the <code class="language-plaintext highlighter-rouge">filename_effective</code> variable:</p>

        <div class="language-console highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="gp">$</span><span class="w"> </span>curl <span class="nt">--head</span> <span class="nt">--remote-name</span> <span class="nt">--write-out</span> <span class="s1">'%{filename_effective}'</span> <span class="s2">"</span><span class="nv">$url</span><span class="s2">"</span>
    </code></pre></div>    </div>
      </li>
      <li>
        <p>To get the final size of the file that will be downloaded, use <code class="language-plaintext highlighter-rouge">--write-out</code> and log the <a href="https://everything.curl.dev/usingcurl/verbose/writeout.html#http-headers">value of the Content-Length header</a>:</p>

        <div class="language-console highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="gp">$</span><span class="w"> </span>curl <span class="nt">--head</span> <span class="nt">--write-out</span> <span class="s1">'%header{content-length}'</span> <span class="s2">"</span><span class="nv">$url</span><span class="s2">"</span>
    </code></pre></div>    </div>
      </li>
    </ul>
HTML
    actual = cleanup_syntax_highlighter_classes(text)
    refute(actual.include?('</div>'))
  end
end

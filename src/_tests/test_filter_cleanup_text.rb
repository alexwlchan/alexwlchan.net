# frozen_string_literal: true

require 'test/unit'

require_relative '../_plugins/filter_cleanup_text'

class TextCleanupText < Test::Unit::TestCase
  def test_it_adds_non_breaking_spaces_after_words
    text = 'Apollo 11 launched in 1969'
    expected = 'Apollo&nbsp;11 launched in 1969'
    assert_equal(AddNonBreakingSpaces.add_non_breaking_spaces(text), expected)
  end

  def test_it_adds_non_breaking_spaces_before_words
    text = 'It takes 2 minutes'
    expected = 'It takes 2&nbsp;minutes'
    assert_equal(AddNonBreakingSpaces.add_non_breaking_spaces(text), expected)
  end
end

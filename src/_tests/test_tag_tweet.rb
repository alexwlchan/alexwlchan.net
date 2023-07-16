require 'test/unit'

require_relative '../_plugins/utils/twitter'

class TestTwitterFilters < Test::Unit::TestCase
  def test_it_replaces_all_instances_of_twemoji
    text = "🧵 Make yours and everybody else's lives slightly less terrible by having all your programs print out their internal stuff as pictures; ✨ a thread ✨ pic.twitter.com/NjQ42bXN2E"
    output = replace_twemoji_with_images(text)
    assert_equal(output.scan('<img').length, 3)
  end

  def test_it_adds_dimensions_to_twemoji
    text = "🧵 Make yours and everybody else's lives slightly less terrible by having all your programs print out their internal stuff as pictures; ✨ a thread ✨ pic.twitter.com/NjQ42bXN2E"
    output = replace_twemoji_with_images(text)
    assert_equal(output.scan('<img class="twemoji" width="20px" height="20px"').length, 3)
  end
end

# frozen_string_literal: true

require 'test/unit'

require_relative '../_plugins/utils/attrs'

class TestParseAttrs < Test::Unit::TestCase
  def test_it_parses_a_simple_string
    input = 'sides="5" colour="red"'
    assert_equal(parse_attrs(input), { 'sides' => '5', 'colour' => 'red' })
  end

  def test_it_allows_bare_attributes
    input = 'sides="5" colour="red" data-proofer-ignore'
    assert_equal(parse_attrs(input), { 'sides' => '5', 'colour' => 'red', 'data-proofer-ignore' => nil })
  end

  def test_it_rejects_unexpected_bare_attributes
    input = 'sides="5" colour="red" unrecognised-attribute'
    assert_raise SyntaxError do
      parse_attrs(input)
    end
  end
end

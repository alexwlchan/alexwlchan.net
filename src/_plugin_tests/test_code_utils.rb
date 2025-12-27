# frozen_string_literal: true

require 'test/unit'

require_relative '../_plugins/utils/code'

class TestCodeUtils < Test::Unit::TestCase
  def test_parse_line_numbers
    linenos = '1-3,_,7-9,_,11'
    expected = %w[1 2 3 _ 7 8 9 _ 11]
    assert_equal(Alexwlchan::CodeUtils.parse_line_numbers(linenos), expected)
  end
end

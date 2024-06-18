# frozen_string_literal: true

require 'test/unit'

require_relative '../_plugins/utils/add_utm_source'

class TestAddUtmSource < Test::Unit::TestCase
  def test_adds_utm_source_param_to_basic_url
    assert_equal(
      add_utm_source_to_url('https://example.com'),
      'https://example.com?utm_source=alexwlchan'
    )
  end

  def test_adds_utm_source_param_to_url_with_query_params
    assert_equal(
      add_utm_source_to_url('https://example.com?id=1'),
      'https://example.com?id=1&utm_source=alexwlchan'
    )
  end

  def test_adds_utm_source_param_to_url_with_query_params_and_fragment
    assert_equal(
      add_utm_source_to_url('https://example.com?id=1#anchor-link'),
      'https://example.com?id=1&utm_source=alexwlchan#anchor-link'
    )
  end
end

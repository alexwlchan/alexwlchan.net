# frozen_string_literal: true

require 'test/unit'

require_relative '../_plugins/inline_styles'

class TestInlineStylesFilters < Test::Unit::TestCase
  def test_it_leaves_html_with_no_style_alone
    html = '<p>Hello world!</p>'
    assert_equal(
      InlineStylesFilters.get_inline_styles(html, nil),
      { 'html' => html, 'inline_styles' => '' }
    )
  end

  def test_it_removes_style_tags
    input = <<~HTML
      <p>Hello world!</p><style> p { color: red; }</style><p>Goodbye world!</p>
    HTML

    output = <<~HTML
      <p>Hello world!</p><p>Goodbye world!</p>
    HTML

    assert_equal(
      InlineStylesFilters.get_inline_styles(input, nil),
      { 'html' => output, 'inline_styles' => 'p { color: red; }' }
    )
  end

  # def test_it_removes_style_tags_with_attributes
  #   input = <<~HTML
  #     <p>Hello world!</p><style type="x-text/scss"> p { color: red; }</style><p>Goodbye world!</p>
  #   HTML
  #
  #   output = <<~HTML
  #     <p>Hello world!</p><p>Goodbye world!</p>
  #   HTML
  #
  #   assert_equal(
  #     InlineStylesFilters.get_inline_styles(input),
  #     { html: output, inline_styles: 'p { color: red; }' }
  #   )
  # end

  def test_it_preserves_source_tags
    input = <<~HTML
      <source srcset="/example.jpg"><style> p { color: red; }</style><p>Goodbye world!</p>
    HTML

    output = <<~HTML
      <source srcset="/example.jpg"><p>Goodbye world!</p>
    HTML

    assert_equal(
      InlineStylesFilters.get_inline_styles(input, nil),
      { 'html' => output, 'inline_styles' => 'p { color: red; }' }
    )
  end
end

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

  def test_it_deduplicates_style_tags
    input = <<~HTML
      <style> p { color: red; }</style>
      <style> p { color: red; }</style>
      <style> div { color: green; }</style>
      <p>Hello world!</p>
    HTML

    result = InlineStylesFilters.get_inline_styles(input, nil)

    assert_equal(
      result['inline_styles'], 'p { color: red; } div { color: green; }'
    )
  end

  def test_it_removes_empty_def_tags
    # This <defs> tag will be empty when we remove the <style> tag, so
    # we can remove it also.  This is fairly common in inline SVGs.
    input = <<~HTML
      <svg>
        <defs>
          <style> line { stroke: black; }</style>
        </defs>
        <line x1="0" y1="0" x2="10" y2="10"/>
      </svg>
    HTML

    output = <<~HTML
      <svg>
        <line x1="0" y1="0" x2="10" y2="10"/>
      </svg>
    HTML

    result = InlineStylesFilters.get_inline_styles(input, nil)
    assert_equal(result['html'], output)
  end
end

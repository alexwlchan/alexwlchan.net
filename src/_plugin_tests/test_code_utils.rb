# frozen_string_literal: true

require 'test/unit'

require 'rouge'

require_relative '../_plugins/utils/code'

class TestCodeUtils < Test::Unit::TestCase
  def test_parse_line_numbers
    linenos = '1-3,_,7-9,_,11'
    expected = %w[1 2 3 _ 7 8 9 _ 11]
    assert_equal(Alexwlchan::CodeUtils.parse_line_numbers(linenos), expected)
  end

  # Braces and selectors in nested CSS are highlighted correctly.
  def test_nested_css
    source = '#movies a:hover { figcaption { text-decoration-line: underline; } }'
    formatter = Rouge::Formatters::HTML.new
    lexer = Rouge::Lexers::CSS.new
    html = formatter.format(lexer.lex(source))

    # Check the code formatted by Rouge includes "err" tokens
    assert_include(html, '<span class="err">')

    # Apply manual fixes, and check the "err" tokens have been removed
    html = Alexwlchan::CodeUtils.apply_manual_fixes(html, 'nested_css', 'css')
    assert_not_include(html, '<span class="err">')
  end

  # A nested a:hover selector is highlighted correctly
  def test_nested_css_with_a_hover
    source = '#movies { a:hover { color: red; } }'
    formatter = Rouge::Formatters::HTML.new
    lexer = Rouge::Lexers::CSS.new
    html = formatter.format(lexer.lex(source))

    # Check the code formatted by Rouge includes "a" highlighted as
    # a property.
    assert_include(html, '<span class="py">a</span>')

    # Apply the fixes, and check that <a> is now highlighted as a name
    html = Alexwlchan::CodeUtils.apply_manual_fixes(html, 'nested_css', 'css')
    assert_not_include(html, '<span class="py">a</span>')
    assert_include(html, '<span class="nt">a</span>')
  end

  # A nested class selector is highlighted properly
  def test_nested_class_selector
    source = '#movies { .wrapper { color: red; } }'
    formatter = Rouge::Formatters::HTML.new
    lexer = Rouge::Lexers::CSS.new
    html = formatter.format(lexer.lex(source))

    # Check the code formatted by Rouge includes "err" tokens
    assert_include(html, '<span class="err">')

    # Apply manual fixes, and check the "err" tokens have been removed
    html = Alexwlchan::CodeUtils.apply_manual_fixes(html, 'nested_css', 'css')
    assert_not_include(html, '<span class="err">')
    assert_include(html, '<span class="nt">.wrapper</span>')
  end
end

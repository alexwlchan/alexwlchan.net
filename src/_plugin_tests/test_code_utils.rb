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

  def format_css(source)
    formatter = Rouge::Formatters::HTML.new
    lexer = Rouge::Lexers::CSS.new
    formatter.format(lexer.lex(source))
  end

  def format_shell(source)
    formatter = Rouge::Formatters::HTML.new
    lexer = Rouge::Lexers::Shell.new
    formatter.format(lexer.lex(source))
  end

  # Braces and selectors in nested CSS are highlighted correctly.
  def test_nested_css
    html = format_css(
      '#movies a:hover { figcaption { text-decoration-line: underline; } }'
    )

    # Check the code formatted by Rouge includes "err" tokens
    assert_include(html, '<span class="err">')

    # Apply manual fixes, and check the "err" tokens have been removed
    html = Alexwlchan::CodeUtils.apply_manual_fixes(html, 'nested_css', 'css')
    assert_not_include(html, '<span class="err">')
  end

  # A nested a:hover selector is highlighted correctly
  def test_nested_css_with_a_hover
    html = format_css('#movies { a:hover { color: red; } }')

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
    html = format_css('#movies { .wrapper { color: red; } }')

    # Check the code formatted by Rouge includes "err" tokens
    assert_include(html, '<span class="err">')

    # Apply manual fixes, and check the "err" tokens have been removed
    html = Alexwlchan::CodeUtils.apply_manual_fixes(html, 'nested_css', 'css')
    assert_not_include(html, '<span class="err">')
    assert_include(html, '<span class="nt">.wrapper</span>')
  end

  # The shebang in a bash script isn't highlighted
  def test_bash_shebang_is_punctuation
    html = format_shell("#!/usr/bin/env bash\n\nset -o errexit\nset -o nounset\n")

    # Check the code formatted by Rouge doesn't include punctuation
    assert_not_include(html, '<span class="p">')

    # Apply manual fixes, and check the snippet contains punctuation
    html = Alexwlchan::CodeUtils.apply_manual_fixes(html, 'shell', 'shell')
    assert_include(html, '<span class="p">#!/usr/bin/env bash</span>')
  end

  def test_bash_functions
    html = format_shell("#!/usr/bin/env bash\n\nprint_greeting() {\n  echo \"hello world\"\n}\n")

    # Check the code formatted by Rouge doesn't a named function
    assert_not_include(html, '<span class="nf">')

    # Apply manual fixes, and check the snippet contains a named function
    html = Alexwlchan::CodeUtils.apply_manual_names(html, 'bash', 'shell')
    assert_include(html, '<span class="nf">print_greeting</span>')
  end
end

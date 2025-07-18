# This reverts a change in Rouge 3.28 which broke multi-line syntax
# highlighting for console snippets.
#
# See https://github.com/rouge-ruby/rouge/pull/1779
# See https://github.com/docker/docs/pull/14825#issue-1247204553

require 'rouge'

module Rouge
  module Lexers
    class ConsoleLexer < Lexer
      def line_regex
        /(\\.|[^\\])*?(\n|$)/m
      end
    end
  end
end

#!/usr/bin/env ruby
# A kinda working upward-assignment operator for Ruby.
#
#     Uequals.enable
#
#     x
#     ⇑
#     4
#
# For an explanation of how this works, see https://alexwlchan.net/2023/upward-assignment/
#
# Inspired by a similar project by Kevin Kuchta:
# https://github.com/kkuchta/vequals
#
# By Alex Chan. MIT license.

require 'ripper'

# This can't live in the body of the Uequals class, or something goes
# wrong in the eval that I haven't


# This is a wrapper that allows us to write Uequals.enable to turn on
# upwards assignment.
class Uequals
  def self.enable
    uequals = Uequals.new
    uequals.enable
  end

  # Find all the identifiers in a line of source code.
  #
  #     find_identifiers_in_line('x = y + 1')
  #         [{:token=>'x', :range=>0..1},
  #          {:token=>'y', :range=>4..5}]
  #
  #     find_identifiers_in_line('name = "Alex"')
  #         [{:token=>'name', :range=>0..4}]
  #
  def find_identifiers_in_line(source_code)
    lexed_line = Ripper.lex(source_code)

    column = 0
    result = []

    lexed_line.each do |_positions, type, token, _state|
      if type == :on_ident
        result << {
          token: token,
          range: (column..column + token.length)
        }
      end

      # We have to track the column manually, because Ripper counts tokens
      # based on their byte width, but we care about character width
      # e.g. 'Münze' is 6 bytes, but 5 characters in a text editor
      column += token.length
    end

    result
  end

  # Find all the values in a line of source code.
  #
  # This only finds a couple of value types (string/int/variable), and
  # not more complex types (e.g. arrays, hashes).
  #
  #     find_values_in_line('x = y + 1').inspect
  #         [{:type=>:on_ident, :token=>'x', :range=>0..1},
  #          {:type=>:on_ident, :token=>'y', :range=>4..5},
  #          {:type=>:on_int,   :token=>'1', :range=>8..9}]
  #
  #     find_values_in_line('name = "Alex"').inspect
  #         [{:type=>:on_ident,           :token=>'name', :range=>0..4},
  #          {:type=>:on_tstring_content, :token=>'Alex', :range=>8..12}]
  #
  def find_values_in_line(source_code)
    lexed_line = Ripper.lex(source_code)

    column = 0
    result = []

    lexed_line.each do |_positions, type, token, _state|
      if type == :on_ident || type == :on_tstring_content || type == :on_int

        result << {
          :type => type,
          :token => token,
          :range => (column..column + token.length)
        }
      end

      # Track the column manually; see comment above.
      column += token.length
    end

    result
  end

  def enable
    tracepoint = TracePoint.new(:line) { |tp|
      if File.exist? tp.path
        line = File.readlines(tp.path)[tp.lineno - 1]
        identifiers = find_identifiers_in_line(line)

        arrow_line = File.readlines(tp.path)[tp.lineno]

        # if there's no next line, we're at the end of the file
        # there definitely isn't an arrow below us!
        unless arrow_line.nil?
          arrows =
            find_identifiers_in_line(arrow_line)
              .filter { |id| id[:token] == '⇑' }

          identifiers.each { |var|
            arrow_below =
              arrows
                .filter { |id| var[:range].cover? id[:range] }
                .last

            # If there's no arrow below us, we can move on to the next identifier
            unless arrow_below.nil?
              value_line = File.readlines(tp.path)[tp.lineno + 1]
              unless value_line.nil?
                values = find_values_in_line(value_line)

                value_below =
                  values.find { |v| v[:range].cover? arrow_below[:range] }

                unless value_below.nil?
                  # If we're assigning to a variable that doesn't exist
                  # yet, create it as a local variable in the binding so
                  # we don't throw a NameError; trust it will be defined later.
                  #
                  # This enables the chain of uequals operators in the
                  # second example.
                  if value_below[:type] == :on_ident
                    tp.binding.receiver.define_singleton_method(value_below[:token]) {
                      |*_| nil
                    }
                  end

                  tp.binding.receiver.define_singleton_method(var[:token]) {
                    |*_| convert_to_value(value_below)
                  }
                end
              end
            end
          }
        end
      end
    }

    # Define the uequals operator as a globally-available method.
    #
    # This prevents Ruby throwing a NameError when it encounters
    # a uequals operator somewhere in the code.
    Object.define_method(:⇑) { |*_| }

    tracepoint.enable
  end
end

# Given a value token lexed from a line, convert this to a value which
# can be assigned to a variable.
#
# This has to live outside the Uequals class so `eval()` can use the
# main scope, which enables the vertical chain of arrows.
def convert_to_value(token)
  case token[:type]
  when :on_int
    token[:token].to_i
  when :on_tstring_content
    token[:token]
  when :on_ident
    eval("#{token[:token]}")
  end
end

Uequals.enable

x
⇑
4

puts "x = #{x}"

x
⇑
y
⇑
3

puts "x = #{x}, y = #{y}"

  x
y ⇑
⇑ 5
6

puts "x = #{x}, y = #{y}"

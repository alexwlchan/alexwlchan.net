# frozen_string_literal: true

module Alexwlchan
  module CodeUtils
    # Parse a range like 1-3,7-9 as a complete list of line numbers,
    # i.e. [1,2,3,7,8,9]
    #
    # The line numbers can include an _ character, which indicates the
    # line should not be numbered.
    def self.parse_line_numbers(linenos)
      linenos.split(',').map do |r|
        if r.include? '-'
          line_start, line_end = r.split('-')
          (line_start..line_end).to_a
        else
          r
        end
      end
      .flatten
    end
  end
end

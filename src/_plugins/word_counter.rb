# This plugin gets an approximate word count for each post, then summarises
# that into the amount of writing I did each month.
#
# This gets displayed as a graph at /word-count
#

require "csv"
require "date"

module Reading
  class WordCounter < Jekyll::Generator
    def generate(site)
      markdown_converter = site.find_converter_instance(::Jekyll::Converters::Markdown)

      per_date_word_count = Hash::new(0)

      site.posts.docs.each do |post|
        word_count = 0
        in_code_block = false

        post.content.each_line do |line|
          line.strip!

          # If we're currently in a code block and this line is the closing three
          # backticks to end a code block, remove the code block context and go
          # to the next line.
          if in_code_block and line == "```"
            in_code_block = false
            next
          end

          if line.start_with? "```"
            in_code_block = true
          end

          # Skip code blocks and block quotes in the word count
          if in_code_block or line.start_with? "> "
            next
          end

          word_count += line.scan(/\S+/).count
        end

        per_date_word_count[post.data["date"].to_date] += word_count
      end

      site.data["per_date_word_count"] = per_date_word_count
      site.data["per_month_word_count"] = get_per_month_word_count(per_date_word_count)
      site.data["total_word_count"] = per_date_word_count.values.inject(0, :+)

      csv_path = "#{site.config["destination"]}/word-count.csv"

      CSV.open(csv_path, "w") do |csv|
        csv << ["month", "word count (approximate)"]
        get_per_month_word_count(per_date_word_count).each do |row|
          csv << row
        end
      end
    end

    def get_per_month_word_count(per_date_word_count)
      result = []

      curr_date = per_date_word_count.keys.min

      while true
        matching_word_counts =
          per_date_word_count
            .select { |date, _|
              date.year == curr_date.year and date.month == curr_date.month
            }
            .values

        word_count = matching_word_counts.inject(0, :+)
        result << [curr_date.strftime("%B %Y"), word_count]

        if curr_date.year == Date.today.year and curr_date.month == Date.today.month
          break
        end

        curr_date = curr_date.next_month
      end

      result
    end
  end
end

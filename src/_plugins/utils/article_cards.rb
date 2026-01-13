# frozen_string_literal: true

require 'abbrev'

module Alexwlchan
  module ArticleCardUtils
    # Choose unique short names for each card.
    #
    # These filenames are repeated many times on the global articles page,
    # so they should be as short as possible.
    #
    # Add a `short_name` attribute to each post.card which can be used
    # to uniquely identify this card.
    #
    # For example, "digital-decluttering" could become "di".
    def self.choose_card_names(posts_with_cards)
      long_names = posts_with_cards.map do |p|
        year = p.data['card']['year']
        name = p.data['card']['name']
        "#{year}/#{name}"
      end

      # A map from full card name to short name,
      # e.g. "2025/cool-to-care.jpg" => "2025/c"
      #
      # Note we need to ignore abbreviations which are too short,
      # e.g. "20" or "2026/" are not allowed!
      short_names = Abbrev.abbrev(long_names)
                          .select { |ab, _full_name| ab.include? '/' }
                          .reject { |ab, _full_name| ab.end_with? '/' }
                          .group_by { |_, v| v }
                          .transform_values { |v| v.flatten.min_by(&:length) }

      posts_with_cards.each do |p|
        year = p.data['card']['year']
        name = p.data['card']['name']
        long_name = "#{year}/#{name}"

        p.data['card']['short_name'] = short_names[long_name].gsub("#{year}/", '')
      end
    end
  end
end

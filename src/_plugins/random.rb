# Plugin to let me randomly shuffle entries in a collection.
#
# See https://stackoverflow.com/a/27179386/1558022

module Jekyll
  module ShuffleFilter
    def shuffle(array)
      array.shuffle
    end
  end
end

Liquid::Template.register_filter(Jekyll::ShuffleFilter)

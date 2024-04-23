# frozen_string_literal: true

# This wraps Jekyll's built-in `smartify` plugin with a Jekyll Cache.
#
# This makes a significant impact on the speed of the site build,
# cutting it roughly in half!

module Jekyll
  module Filters
    alias builtin_smartify smartify

    def smartify_cache
      @@smartify_cache ||= Jekyll::Cache.new('Smartify')
    end

    # Like the builtin smartify filter, but faster.
    def smartify(input)
      smartify_cache.getset(input) do
        builtin_smartify(input)
      end
    end
  end
end

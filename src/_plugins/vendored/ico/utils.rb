module ICO
  module Utils
    APPEND_FILE_FORMAT = '-%<x>dx%<y>d'

    module_function

    # @see https://ruby-doc.org/core-2.2.3/Enumerable.html#method-i-select
    # @see https://ruby-doc.org/core-2.2.3/Enumerable.html#method-i-reject
    # @param filename_array [Array<String>] array of filenames with expanded paths
    # @param enum           [String,Symbol] accepts: `:select` or `:reject`
    # @return               [Array]
    def filter_dir(filename_array, enum)
      raise ArgumentError unless filename_array.is_a? Array
      raise ArgumentError unless enum.is_a?(String) || enum.is_a?(Symbol)
      raise ArgumentError unless enum.to_s =~ /reject|select/

      filename_array.send(enum).each { |fn| Dir.exist?(fn) }
    end

    def filter_ext(filename_array, enum, extname, include_dirs = false)
      raise ArgumentError unless filename_array.is_a? Array
      raise ArgumentError unless enum.is_a?(String) || enum.is_a?(Symbol)
      raise ArgumentError unless enum.to_s =~ /reject|select/
      raise ArgumentError unless extname.is_a?(String) || extname.is_a?(Symbol)

      # reject dirs for accuracy
      tmp_array = filter_dir(filename_array, :reject)

      # operation on array
      tmp_array = tmp_array.send(enum).each { |fn| format_ext(File.extname(fn)) == format_ext(extname) }

      include_dirs ? tmp_array + filter_dir(filename_array, :select) : tmp_array
    end

    def format_ext(extname, overwrite = false)
      raise ArgumentError unless extname.is_a?(String) || extname.is_a?(Symbol)

      temp_str = extname.to_s.sub(/\A\.?/, '.').downcase

      tmp_str if overwrite

      temp_str
    end

    def format_ext!(extname)
      format_ext(extname, true)
    end

    def contains_other_than_ext?(filename_array, extname)
      filter_ext(filename_array, :reject, extname, true).any?
    end

    # http://stackoverflow.com/questions/2450906/is-there-a-simple-way-to-get-image-dimensions-in-ruby#2450931
    def get_size(image_filename)
      File.read(image_filename)[0x10..0x18].unpack('NN')
    end

    def sizes_hash(filename_array, sort = false, reverse = false)
      raise ArgumentError unless filename_array.is_a? Array

      tmp_hash = filename_array.each_with_object({}) do |fn, h|
        h[get_size(fn)] = fn
      end

      if sort && !reverse
        tmp_hash.sort.to_h

      elsif reverse && !sort
        tmp_hash.to_a.reverse.to_h

      elsif sort && reverse
        tmp_hash.sort.reverse.to_h

      else
        tmp_hash
      end
    end
  end
end

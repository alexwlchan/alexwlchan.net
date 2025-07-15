# frozen_string_literal: true

# Validate the YAML front matter by checking that:
#
#   1. I'm not using undocumented fields
#   2. Fields have appropriate values
#
def check_yaml_front_matter(src_dir)
  errors = Hash.new { [] }

  info('Checking YAML front matter...')

  schema = JSON.parse(File.read('front-matter.json'))

  get_markdown_paths(src_dir).each do |md_path|
    if md_path.start_with?('src/_plugins/')
      next
    end

    # The YAML loader will try to be "smart" (e.g. reading dates as
    # proper Ruby date types), which is unhelpful for json-schema checking.
    #
    # Make sure everything is JSON-esque (i.e. strings/numbers/bools)
    # before passing to the json-schema gem.
    front_matter = YAML.load(
      File.read(md_path).split("\n---\n")[0],
      permitted_classes: [Date, Time]
    )
    front_matter = JSON.parse(JSON.dump(front_matter))

    md_errors = [
      validate_json_schema(front_matter, schema),
      validate_layout(front_matter, md_path),
      validate_color_pairs(front_matter)
    ].flatten

    errors[md_path] = md_errors unless md_errors.empty?
  end

  report_errors(errors)
end

def validate_json_schema(front_matter, schema)
  JSON::Validator.fully_validate(schema, front_matter)
end

# Check whether the `layout` matches the location in the directory tree.
#
# e.g. every Markdown file which is under `src/_posts` should have the
# layout `post`, and seeing an unexpected layout there would be an error.
def validate_layout(front_matter, md_path)
  expected_layout =
    if md_path.start_with?('src/_posts') || md_path.start_with?('src/_drafts')
      'post'
    elsif md_path.start_with?('src/_til')
      'til'
    else
      'page'
    end

  if front_matter['layout'] == expected_layout
    []
  else
    ["layout should be '#{expected_layout}'; got #{front_matter['layout']}"]
  end
end

# Check the `colors` always appear in light/dark pairs.
#
# e.g. if a file specifies an `index_light`, it must also specify
# an `index_dark`.  Only specifying one color is an error.
def validate_color_pairs(front_matter)
  errors = []

  has_css_light = front_matter.fetch('colors', {}).key?('css_light')
  has_css_dark = front_matter.fetch('colors', {}).key?('css_dark')

  if (has_css_light && !has_css_dark) || (!has_css_light && has_css_dark)
    errors <<= 'css colors must have both light and dark variants'
  end

  has_index_light = front_matter.fetch('colors', {}).key?('index_light')
  has_index_dark = front_matter.fetch('colors', {}).key?('index_dark')

  if (has_index_light && !has_index_dark) || (!has_index_light && has_index_dark)
    errors <<= 'index colors must have both light and dark variants'
  end

  errors
end

def report_errors(errors)
  # This is meant to look similar to the output from HTMLProofer --
  # errors are grouped by filename, so they can be easily traced
  # back to the problem file.
  return if errors.empty?

  errors.each do |display_path, messages|
    error("- #{display_path}")
    messages.each do |m|
      error("  *  #{m}")
    end
  end
  exit!
end

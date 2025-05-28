def apply_markdownify_oneline(site, input)
  site.find_converter_instance(Jekyll::Converters::Markdown)
      .convert(input)
      .sub('<p>', '')
      .sub('</p>', '')
      .strip
end

# This hook allows me to use "pycon" as a language name in Rouge.
#
# These options come from a GitHub discussion about using the
# console lexer to highlight sessions from the Python console.
# See https://github.com/rouge-ruby/rouge/issues/919
#
# This allows me to write blocks like:
#
#     ```pycon
#     >>> print("hello world")
#     hello world
#     ```
#
# and get the behaviour I expect.
#
# (It took me years to notice these weren't rendering correctly -- this
# is preferable to custom syntax I'd forget to add.)

Jekyll::Hooks.register :documents, :pre_render do |doc|
  # How this works: you capture any whitespace up to the ```pycon,
  # which must include a newline, then the `\K` escape sequence
  # resets the starting point of the reported match.
  #
  # The whitespace is for places where the ```pycon block is indented,
  # e.g. in a list.
  doc.content = doc.content.gsub(
    /\n\s*\K```pycon\n/,
    "```console?lang=python&prompt=>>>,...\n"
  )
end

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

Jekyll::Hooks.register(%i[pages posts], :pre_render) do |p|
  p.content = p.content.gsub("\n```pycon\n", "\n```console?lang=python&prompt=>>>,...\n")
end

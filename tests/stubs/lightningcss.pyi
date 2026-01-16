# Note(2026-01-16): I wrote this with lightningcss 0.3.1, which doesn't
# include type hints for the bundle_css function.
#
# When the library author releases a new version and includes type hints,
# I can delete this file.
def bundle_css(path: str, minify: bool) -> str: ...

from pygments.lexers import Lexer
from pygments.formatters import HtmlFormatter

def highlight(src: str, lexer: Lexer, formatter: HtmlFormatter) -> str: ...

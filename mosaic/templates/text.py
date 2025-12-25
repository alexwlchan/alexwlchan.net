from markdown import markdown


def markdownify(text: str) -> str:
    """
    Format some text using Markdown.
    """
    return markdown(text, extensions=["codehilite", "fenced_code", "smarty"])


def markdownify_oneline(text: str) -> str:
    """
    Format a single line of text using Markdown, but don't wrap it
    in <p> tags.
    """
    return markdownify(text).replace("<p>", "").replace("</p>", "")
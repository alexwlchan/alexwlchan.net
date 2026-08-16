"""
A breadcrumb trail helps people navigate the hierarchy of the site.
"""

from pydantic import BaseModel


class BreadcrumbEntry(BaseModel):
    """
    A breadcrumb entry that helps you see this page in my broader site.
    """

    label: str
    href: str

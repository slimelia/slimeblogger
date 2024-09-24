#!/usr/bin/env python3
"""Module for parsing a Slimeblogger blog header string.
If run directly, gives an example of usage.
"""


from datetime import datetime
import re


class BlogAttributes:
    """Takes Slimeblogger blog header string, find attributes via RegEx,
    then assigns them to attributes.
    """

    def __init__(self, string_to_split: str):
        self.title: str = self.parse_title(string_to_split)
        self.author: str = self.parse_author(string_to_split)
        self.date: datetime = self.parse_date(string_to_split)

    def parse_title(self, string_to_search: str) -> str:
        """Returns Title as denoted by @title tag.
        """
        if title := re.search(r'(?<=@title ).*?(?=\s@|$)', string_to_search):
            return title.group()
        raise ValueError("@title field missing in one or more blog posts.")

    def parse_author(self, string_to_search: str) -> str:
        """Returns Author as denoted by @author tag.
        """
        if author := re.search(r'(?<=@author ).*?(?=\s@|$)', string_to_search):
            return author.group()
        raise ValueError("@author field missing in one or more blog posts.")

    def parse_date(self, string_to_search: str) -> datetime:
        """Returns date as denoted by @date tag.
        """
        if date := re.search(r'(?<=@date )[0-9]{4}-[0-9]{2}-[0-9]{2}'
                             r'(T[0-9]{2}:[0-9]{2})?(?=\s@|$)',
                             string_to_search):
            return datetime.fromisoformat(date.group())
        raise ValueError("@date field missing in one or more blog posts.")


if __name__ == "__main__":
    exampleString: str = "@title Example Title @author slimelia"\
                         " @date 2024-01-01T11:59"
    exampleBlogAttrs: BlogAttributes = BlogAttributes(exampleString)
    print(f"Title: {exampleBlogAttrs.title}\nAuthor:"
          f" {exampleBlogAttrs.author}\n"
          f"Date: {exampleBlogAttrs.date:%Y-%m-%d}")

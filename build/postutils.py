#!/usr/bin/env python3
"""Assorted utilities relating to fetching, parsing and styling
Slimeblogger posts.
"""

from collections.abc import Mapping
from datetime import datetime
from pathlib import Path
from operator import itemgetter
from markdown import markdown
from blog_attributes import BlogAttributes


def blog_post_dict(filename: str, title: str, author: str,
                   date: datetime, body: str) -> Mapping[str, str | datetime]:
    """Return a standard Slimeblogger blog post dict."""
    return {
        "filename": filename,
        "title": title.title(),
        "author": author,
        "date": f"{date:%Y-%m-%d}",
        "true_date": date,
        "body": body
    }


def get_post_dicts(post_path: str) -> list[Mapping[str, str | datetime]]:
    """Fetch Markdown files from directory, store in a dict,
    then append to a list. Returns list of dicts.
    """
    directory: Path = Path(post_path)
    post_list: list[Mapping[str, str | datetime]] = []
    file: Path
    for file in directory.iterdir():
        if file.suffix == ".md":
            with open(file.resolve(), 'r', encoding='utf-8') as doc:
                first_line: str = doc.readline()
                post_body: str = markdown(doc.read())
            attributes: BlogAttributes = BlogAttributes(first_line)
            filename: str = file.stem + ".html"
            post: Mapping[str, str | datetime] = \
                blog_post_dict(filename, attributes.title,
                               attributes.author, attributes.date,
                               post_body)
            post_list.append(post)
    post_list.sort(key=itemgetter("true_date"), reverse=True)
    return post_list


def package_post(post: str | None) -> dict[str, str | None]:
    """Take blog post and return in dict format required for site template."""
    return {"post": post}

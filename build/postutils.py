#!/usr/bin/env python3

from pathlib import Path
from blog_attributes import BlogAttributes
from markdown import markdown
from collections.abc import Mapping
from datetime import datetime
from operator import itemgetter


class BlogPost(Mapping):
    filename: str
    title: str
    author: str
    date: str
    true_date: datetime

def blog_post_dict(filename: str, title: str, author: str,
                   date: datetime, body: str) -> BlogPost:
    return {
        "filename": filename,
        "title": title.title(),
        "author": author,
        "date": f"{date:%Y-%m-%d}",
        "true_date": date,
        "body": body
    }

def get_post_dicts(post_path: str) -> list[dict[str,str]]:
    directory: Path = Path(post_path)
    post_list: list[dict] = list()
    file: Path
    for file in directory.iterdir():
        if file.suffix  == ".md":
            with open(file.resolve(),'r',encoding='utf-8') as doc:
                first_line: str = doc.readline()
                post_body: str = markdown(doc.read())
            attributes: BlogAttributes  = BlogAttributes(first_line)
            filename: str = file.stem + ".html"
            post: BlogPost = blog_post_dict(filename, attributes.title,
                                            attributes.author, attributes.date,
                                            post_body)
            post_list.append(post)
    post_list.sort(key=itemgetter("true_date"), reverse=True)
    return post_list

def package_post(post: str) -> dict[str, str]:
    return {"post":post}

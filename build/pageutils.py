#!/usr/bin/env python3

from collections.abc import Mapping


class PageDict(Mapping):
    relativelink: str
    rootURL: str
    feedtitle: str
    content: list[str]

def page_dict(relative_link: str, root_url: str, feed_title:str,
              content: list[str] | None = None) -> PageDict:
    if content:
        return { "relativelink":relative_link,
                 "rootURL":root_url,
                 "feedtitle":feed_title,
                 "content":[content]
        }
    return { "relativelink":relative_link,
             "rootURL":root_url,
             "feedtitle":feed_title,
             "content":[]
    }

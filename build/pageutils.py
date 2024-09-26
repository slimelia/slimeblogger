#!/usr/bin/env python3
"""Utilities relating to generating Slimeblogger webpages"""


def page_dict(relative_link: str, root_url: str | None, feed_title: str | None,
              content: dict[str, str] | None = None
              ) -> dict[str, str | None | list[dict[str, str]]]:
    """Return a Slimeblogger webpage dict. If content parameter is not
    provided, an empty List will be returned in the dict's content field."""
    if content:
        return {"relativelink": relative_link,
                "rootURL": root_url,
                "feedtitle": feed_title,
                "content": [content]
                }
    return {"relativelink": relative_link,
            "rootURL": root_url,
            "feedtitle": feed_title,
            "content": []
            }

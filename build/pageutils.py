#!/usr/bin/env python3
"""Utilities relating to generating Slimeblogger webpages"""


def page_dict(relative_link, root_url, feed_title, content=None):
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

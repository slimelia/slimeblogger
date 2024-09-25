#!/usr/bin/env python3

import os
import chevron
from markdown import markdown
from feedgen.feed import FeedGenerator
from feedgen.entry import FeedEntry
from datetime import datetime
from collections.abc import Mapping, Callable
from operator import attrgetter
from functools import partial
import tomllib
import constants as c
import postutils as p
import renderutils as rn

def prepare_post(template: str, post: dict[str, str]) -> dict[str, str]:
    rendered_post: str = rn.render(template, post)
    return p.package_post(rendered_post)

def prepare_page(template: str, content:dict[str, str]) -> str:
    rendered_page: str = rn.render(template, post)





def generateBlogPages(dirToWriteTo,blogpostList,templates,rootURL,feedtitle):
    POST_TEMPLATE = templates[0]
    SITE_TEMPLATE = templates[1]

    for blogpostObj in blogpostList:
        blogpost = generateBlogpostObj(POST_TEMPLATE,blogpostObj)
        siteContent = {
        "relativelink":"../",
        "rootURL":rootURL,
        "feedtitle":feedtitle,
        "content":[blogpost]
        }
        siteHtml = generateSite(SITE_TEMPLATE,siteContent)
#       parsedSiteHtml = bs4.BeautifulSoup(siteHtml, 'html.parser')

        fileHandler = open(f"{dirToWriteTo}/{blogpostObj['filename']}","w")
#       fileHandler.write(parsedSiteHtml.prettify())
        fileHandler.write(siteHtml)
        fileHandler.close()

def generateAtomFeed(blogpostList,rootURL,title):
    feedGen  = FeedGenerator()
    feedGen.title(title)
    feedGen.link(href=f"{rootURL}/atom.xml", rel='alternate')
    feedGen.id(rootURL)
    feedGen.updated(f'{blogpostList[0]["date"]}{TIMESTAMP_STRING}')
    for post in blogpostList:
        atomFeedEntry  = feedGen.add_entry()
        atomFeedEntry.title(post['title'])
        atomFeedEntry.link(href=f'{rootURL}/pages/{post["filename"]}', rel='alternate')
        atomFeedEntry.updated(f'{post["date"]}{TIMESTAMP_STRING}')
        atomFeedEntry.id(f'{rootURL}/pages/{post["filename"]}')
        atomFeedEntry.content(post['body'],type="html")

    return feedGen


def main() -> None:
    with open(c.CONFIG_TOML,"rb") as file:
        config: str = tomllib.load(file)

    inner_posts: list[dict[str,str]] = p.get_post_dicts(c.POST_DIR)
    rendered_posts = [prepare_post(ip) for ip in inner_posts]







if __name__ == "__main__":
    postDir = "posts"
    dirForPages = "../public_html/pages"
    dirForFeed = "../public_html"
    post_template = "templates/blogpost.mustache"
    site_template = "templates/site.mustache"

    postList = getBlogpostsFromDir(postDir)

    with open("config.toml","rb") as file:
        config = tomllib.load(file)

    rootURL = config.get("rootURL","")
    feedtitle = config.get("title","My Cool Blog")
    feedIncluded = False
    if len(rootURL) > 0:
        feed = generateAtomFeed(postList,rootURL,feedtitle)
        feedIncluded = True
        feed.atom_file(f'{dirForFeed}/atom.xml')

    generateBlogPages(dirForPages,postList,templates,rootURL,feedtitle)

    index_content = {
    "relativelink":"",
    "rootURL":rootURL,
    "feedtitle":feedtitle,
    "content":[]
    }
    for post in postList:
        index_content["content"].append(generateBlogpostObj(post_template,post))

    siteHtml = generateSite(site_template,index_content)
#   parsedSiteHtml = bs4.BeautifulSoup(siteHtml, 'html.parser')

    index_html = open('../public_html/index.html',"w")
#   index_html.write(parsedSiteHtml.prettify())
    index_html.write(siteHtml)
    index_html.close()

#!/usr/bin/env python3

import os
import chevron
from markdown import markdown
from feedgen.feed import FeedGenerator
from feedgen.entry import FeedEntry
from datetime import datetime
from operator import attrgetter
from functools import partial
from collections.abc import Iterator
import tomllib
import constants as c
import postutils as p
from pageutils import page_dict,PageDict
import renderutils as rn

TIMESTAMP_STRING: str = 'T12:00'

def prepare_post(template: str, post: dict[str, str]) -> dict[str, str]:
    rendered_post: str = rn.render(template, post)
    return p.package_post(rendered_post)

def create_post_pages(posts: Generator[dict[str,str]], config: dict[str, str], template: str, pages_dir: str) -> list[str]:
    rendered_posts: list[str] = []
    for post in posts:
        rendered_posts.append(post)
        prepared_post: dict[str, str] = prepare_post(post)
        page_content: dict[str, str] = page_dict("../",config.get("rootURL"),config.get("title"),prepared_post)
        webpage = rn.render(template, page_content)
        with open(f"{pages_dir}/{post.get("filename")}","w", encoding="utf-8") as html_page:
            html_page.write(webpage)
    return rendered_posts



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
    rendered_posts: list[str] = create_post_pages(ip for ip in inner_posts)
    #TODO: Atom feed generation here










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

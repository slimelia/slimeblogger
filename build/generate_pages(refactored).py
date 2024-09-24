#!/usr/bin/env python3

import os
import chevron
from markdown import markdown
from blog_attributes import BlogAttributes
from feedgen.feed import FeedGenerator
from feedgen.entry import FeedEntry
from datetime import datetime
from collections.abc import Mapping
from pathlib import Path
from operator import attrgetter
import tomllib

TIMESTAMP_STRING: str = 'T12:00:00Z'

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

def get_posts(post_path: str) -> list[dict[str,str]]:
    directory: Path = Path(post_path)
    post_list: list[dict] = list()
    file: Path
    for file in directory.iterdir():
        if file.suffix  == ".md":
            with open(file.resolve(),'r',encoding='utf-8') as doc:
                first_line: str = doc.readline()
                post_body:  = markdown(doc.read())
            attributes: BlogAttributes  = BlogAttributes(first_line)
            filename = file.stem + ".html"
            post: BlogPost = blog_post_dict(filename, attributes.title,
                                            attributes.author, attributes.date,
                                            post_body)
            post_list.append(post)
    post_list.sort(key=attrgetter("true_date"), reverse=True)
    return post_list


def generateBlogpostObj(blogpostTemplateLocation,blogpost):
    posts = []
    content = {}

    fileHandler = open(blogpostTemplateLocation,"r")
    blogpostTemplate = fileHandler.read()
    fileHandler.close()

    generatedBlogpost = chevron.render(blogpostTemplate,blogpost)
    blogpostObj = {"post":generatedBlogpost}

    return blogpostObj

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

def generateSite(siteTemplateLocation,content):
    fileHandler = open(siteTemplateLocation,"r")
    siteTemplate = fileHandler.read()
    fileHandler.close()

    generatedSite = chevron.render(siteTemplate,content)

    return generatedSite

def main() -> None:
    POST_DIR  = "posts"
    PAGES_DIR = "../public_html/pages"
    FEED_DIR = "../public_html"
    POST_TEMPLATE = "templates/blogpost.mustache"
    SITE_TEMPLATE = "templates/site.mustache"

if __name__ == "__main__":
    postDir = "posts"
    dirForPages = "../public_html/pages"
    dirForFeed = "../public_html"
    postTemplate = "templates/blogpost.mustache"
    siteTemplate = "templates/site.mustache"

    templates = [postTemplate,siteTemplate]

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
        index_content["content"].append(generateBlogpostObj(postTemplate,post))

    siteHtml = generateSite(siteTemplate,index_content)
#   parsedSiteHtml = bs4.BeautifulSoup(siteHtml, 'html.parser')

    index_html = open('../public_html/index.html',"w")
#   index_html.write(parsedSiteHtml.prettify())
    index_html.write(siteHtml)
    index_html.close()

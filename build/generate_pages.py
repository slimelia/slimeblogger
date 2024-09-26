#!/usr/bin/env python3
"""Generate static blog and optional Atom XML feed from Markdown documents."""

import tomllib
from feedgen.feed import FeedGenerator  # type: ignore
import constants as c
import postutils as p
from pageutils import page_dict
from renderutils import render


def prepare_post(template, post):
    """Render blog post and return as a dict compatible with the
    site template."""
    rendered_post = render(template, post)
    return p.package_post(rendered_post)


def create_post_pages(posts, config, post_template, site_template, pages_dir):
    """Create individual web pages for each blog post and save them in
    the given directory. Returns a list of blog post dicts with both
    inner HTML stored in 'body' and whole `article` tag section in 'post'."""
    rendered_posts = []
    for post in posts:
        prepared_post = prepare_post(post_template, post)
        rendered_post = post.copy()
        rendered_post["post"] = prepared_post.get("post", "")
        rendered_posts.append(rendered_post)
        page_content = page_dict("../", config.get("rootURL", ""),
                                 config.get("title", ""), prepared_post)
        webpage = render(site_template, page_content)
        with open(f"{pages_dir}/{post.get('filename', '')}", "w",
                  encoding="utf-8") as html_page:
            html_page.write(webpage)
    return rendered_posts


def generate_index(index_path, template, config, posts):
    """Create the index.html file in the given directory.
    """
    index = page_dict("", config.get("rootURL", ""), config.get("title", ""))
    index["content"] = posts.copy()
    index_html = render(template, index)
    with open(index_path, "w", encoding="utf-8") as index_file:
        index_file.write(index_html)


def generate_atom_feed(posts, config):
    """produce Atom XML feed for posts and config given. Returns
    a FeedGenerator object."""
    feed_gen = FeedGenerator()
    title = config.get("title", "My Cool Blog")
    root_url = config.get("rootURL", "")
    feed_gen.title(title)
    feed_gen.link(href=f"{root_url}/atom.xml", rel='alternate')
    feed_gen.id(root_url)
    for post in posts:
        feed_entry = feed_gen.add_entry()
        feed_entry.title(post.get("title", ""))
        filename = post.get("filename", "")
        feed_entry.link(href=f"{root_url}/pages/{filename}", rel="alternate")
        date = post.get("true_date")
        feed_entry.updated(f"{date:%Y-%m-%dT%H:%M}Z")
        feed_entry.id(f"{root_url}/page/{filename}")
        feed_entry.content(post.get("body", ""), type="html")
    return feed_gen


def main():
    """Main"""
    with open(c.CONFIG_TOML, "rb") as file:
        config = tomllib.load(file)
    inner_posts = p.get_post_dicts(c.POST_DIR)
    rendered_posts = create_post_pages((ip for ip in inner_posts),
                                       config, c.POST_TEMPLATE,
                                       c.SITE_TEMPLATE, c.PAGES_DIR)
    if len(config.get("rootURL", "")) > 0:
        feed = generate_atom_feed(rendered_posts, config)
        feed.atom_file(f"{c.FEED_DIR}/atom.xml")
    generate_index(c.INDEX_PATH, c.SITE_TEMPLATE, config, rendered_posts)


if __name__ == "__main__":
    main()

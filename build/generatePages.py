#!/usr/bin/env python3
"""Generate static blog and optional Atom XML feed from Markdown documents."""

from feedgen.feed import FeedGenerator
from feedgen.entry import FeedEntry
from collections.abc import Iterator
import tomllib
import constants as c
import postutils as p
from pageutils import page_dict
from renderutils import render


def prepare_post(template: str, post: dict[str, str]) -> dict[str, str]:
    rendered_post: str = render(template, post)
    return p.package_post(rendered_post)


def create_post_pages(posts: Iterator[dict[str, str]], config: dict[str, str],
                      post_template: str, site_template: str, pages_dir: str
                      ) -> list[dict[str, str]]:
    rendered_posts: list[dict[str, str]] = []
    for post in posts:
        prepared_post: dict[str, str] = prepare_post(post_template, post)
        rendered_post = post.copy()
        rendered_post["post"] = prepared_post.get("post")
        rendered_posts.append(rendered_post)
        page_content: dict[str, str] = page_dict("../", config.get("rootURL"),
                                                 config.get("title"),
                                                 prepared_post)
        webpage = render(site_template, page_content)
        with open(f"{pages_dir}/{post.get('filename')}", "w", encoding="utf-8"
                  ) as html_page:
            html_page.write(webpage)
    return rendered_posts


def generate_index(index_path: str, template: str, config: dict[str, str],
                   posts: list[dict[str, str]]) -> None:
    index = page_dict("", config.get("rootURL"), config.get("title"))
    index["content"] = posts.copy()
    index_html = render(template, index)
    with open(index_path, "w", encoding="utf-8") as index_file:
        index_file.write(index_html)


def generate_atom_feed(posts: list[str], config: dict[str, str]
                       ) -> FeedGenerator:
    feed_gen: FeedGenerator = FeedGenerator()
    title: str = config.get("title", "My Cool Blog")
    filename: str = config.get("filename")
    root_url: str = config.get("rootURL")
    feed_gen.title(title)
    feed_gen.link(href=f"{root_url}/atom.xml", rel='alternate')
    feed_gen.id(root_url)
    for post in posts:
        feed_entry = feed_gen.add_entry()
        feed_entry.title(post.get("title"))
        feed_entry.link(href=f"{root_url}/pages/{filename}", rel="alternate")
        date = post.get("true_date")
        feed_entry.updated(f"{date:%Y-%m-%dT%H:%M}Z")
        feed_entry.id(f"{root_url}/page/{filename}")
        feed_entry.content(post.get("body"), type="html")
    return feed_gen


def main() -> None:
    with open(c.CONFIG_TOML, "rb") as file:
        config: str = tomllib.load(file)
    inner_posts: list[dict[str, str]] = p.get_post_dicts(c.POST_DIR)
    rendered_posts: list[dict[str, str]] \
        = create_post_pages((ip for ip in inner_posts), config,
                            c.POST_TEMPLATE, c.SITE_TEMPLATE,
                            c.PAGES_DIR)
    if len(config.get("rootURL")) > 0:
        feed = generate_atom_feed(rendered_posts, config)
        feed.atom_file(f"{c.FEED_DIR}/atom.xml")
    generate_index(c.INDEX_PATH, c.SITE_TEMPLATE, config, rendered_posts)


if __name__ == "__main__":
    main()

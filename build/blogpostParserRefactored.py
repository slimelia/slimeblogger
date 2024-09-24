#!/usr/bin/env python3

from datetime import datetime
import re

class blogAttributes:
    def __init__(self,stringToSplit: str):
        self.title: str = self.parseTitle(stringToSplit)
        self.author: str = self.parseAuthor(stringToSplit)
        self.date: datetime = self.parseDate(stringToSplit)

    def parseTitle(self, stringToSearch: str):
            if title := re.search(r'(?<=@title ).*?(?=\s@|$)',stringToSearch):
                return title.group()
            else:
                raise ValueError("@title field missing in one or more blog posts.")

    def parseAuthor(self, stringToSearch: str):
            if author := re.search(r'(?<=@author ).*?(?=\s@|$)',stringToSearch):
                return author.group()
            else:
                raise ValueError("@author field missing in one or more blog posts.")

    def parseDate(self, stringToSearch: str):
            if date := re.search(r'(?<=@date )[0-9]{4}-[0-9]{2}-[0-9]{2}(T[0-9]{2}:[0-9]{2})?(?=\s@|$)',stringToSearch):
                return datetime.fromisoformat(date.group())
            else:
                raise ValueError("@date field missing in one or more blog posts.")



if __name__ == "__main__":
    exampleString = "@title Example Title @author slimelia @date 2024-01-01T11:59"
    exampleBlogAttrs = blogAttributes(exampleString)
    print(f"Title: {exampleBlogAttrs.title}\nAuthor: {exampleBlogAttrs.author}\nDate: {exampleBlogAttrs.date:%Y-%m-%d}")

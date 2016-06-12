# tilde.town/~slimelia
This is the repository for the source code of my static blog generator I use for my [tilde.town website](http://tilde.town/~slimelia/).

It's very messy and crude, but the owners of tilde.town are all about brualist websites so I'm pretending that's intentional/ ;)

## Markdown formatting

Web blog content is generated from Markdown blog post documents.

All blog posts *MUST* contain a header on the first line.

Headers must follow this format:

`@title Title Goes Here @author author_name_here @date yyyy-mm-dd`

Dates *MUST* be written as yyyy-mm-dd format, separated by '-'.


## Required packages

Uses the following Python3 libraries:
  * markdown
  * pystache
  * PyTidyLib
  * BeautifulSoup4

# Slimelia's Blog Generator (SLIMEBLOGGER)
Static blog generator with Atom feed, as used on my [tilde.town page](https://tilde.town/~slimelia).

Takes Markdown posts, spits out HTML. Easy peasy lemon squeezy!

⚠️ **Requires Python 3.11 or greater!**


## How To Use

Please see the [wiki](https://github.com/slimelia/slimeblogger/wiki) for assistance on using this blog generator.

## Markdown formatting

Web blog content is generated from Markdown blog post documents.
All blog posts must contain a header on the first line:

`@title Title Goes Here @author author_name_here @date yyyy-mm-dd`
The date field can either be `yyyy-mm-dd` or `yyyy-mm-ddThh:mm`. If you have posts made on the same day, they will be ordered by time.
See the [example documents](https://github.com/slimelia/slimeblogger/tree/master/build/posts) for examples of valid date/time strings.

## Required packages

Copied from `build/requirements.txt`:
```
chevron==0.14.0
feedgen==1.0.0
Markdown==3.7
```
Open the `build` directory in your terminal and run `pip install -r requirements.txt` to install.

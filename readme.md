ssgen
=====
ssgen is a simple static site generator for blog posting with under 200 lines of code (~290 in total). It's also designed performance in mind, and it's fast or at least fast as you can get with python.

ssgen is only meant for minimal and simple sites, not for any modern fancy 10 MB sites. Only one template is used for the whole website.

Supported file formats
----------------------
Html and markdown are supported.

Dependencies
------------
- Python 3
- Pandoc for markdown (optional)

Writing first site
------------------
You can see an example site in the example directory. This may be the easiest way to learn to use this.

Here are some rules for creating a site. Basically you'll want to create one template file. Content file's contents will be placed to the template with magic word {{CONTENT}}.
Articles must be placed in "articles/" directory or otherwise, it's not considered to be an article. Article's filename must be formated as follows: "‰Y-‰m-‰d-title", for example 2021-01-01-This-is-an-article.
The article's filename upon generating is formatted correctly for the web. If HTML is used as a content file, set the filename ending to ".html.content". 


Magic words
-----------
- {{CONTENT}} - content of site (used in template)
- {{ARTICLES}} – full list of all articles
- {{RECENT}} – list of 8 most recent articles
- {{TIME}} – current UTC timestamp
- {{PUBLISHDATE}} - date from article's filename

Example site
------------
You can visit https://badai.xyz to see a website generated with ssgen in production.

Bugs
----
Please leave bug reports to https://gitlab.com/4shadoww/ssgen.
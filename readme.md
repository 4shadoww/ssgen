ssgen
=====
ssgen is a simple static site generator for blog posting with under 250 lines of code (~340 in total). It's also designed performance in mind, and it's fast or at least fast as you can get with python.

ssgen is only meant for minimal and simple sites. Only one template is used for the whole website.

Supported file formats
----------------------
Html and markdown are supported.

Dependencies
------------
- Python 3
- Pandoc, for markdown support (optional)
- python-feedgen, for rss feed support (optional)
- mathjax-node-cli, for math equations rendering (optional)

Writing first site
------------------
You can see an example site in the example directory. This may be the easiest way to learn to use this.

Here are some rules for creating a site:
- Only one template file for the whole site
- {{CONTENT}} magic word in the template indicates the place for the site's content 
- Articles must be placed in "articles/" directory or otherwise, it's not considered to be an article
- Article's filename must be formated as follows: "%Y-%m-%d-title", for example "2021-01-01-this-is-an-article". The date is the published date.
- First line of article file must be its title. If html is used it must be placed inside h1 tags.
- If HTML is used as a content file, set the filename ending to ".html.content". 

There is also sitemap generator "sitemap-gen.py" which can generate "sitemap.xml". 

Magic words
-----------
- {{CONTENT}} - content of site (used in template)
- {{ARTICLES}} – full list of all articles
- {{RECENT}} – list of 8 most recent articles
- {{TIME}} – current UTC timestamp
- {{PUBLISHDATE}} - date from article's filename

Math
----
Math equation SVGs can be generated using mathjax-cli (doesn't work with RSS feed). This is a bloated and very slow solution, but it's better than making end-user run javascript.

Install mathjax-cli with npm or yarn.

    $ npm install https://github.com/mathjax/mathjax-node-cli/ 

Then give executable location to ssgen with -mj parameter:

    $ ./ssgen.py source output master.html -mj node/node_modules/mathjax-node-cli/bin/tex2svg

RSS feed
--------
RSS feed can be generated separately with the following example command:

    ./ssgen.py source output master.html -rss https://base-url/ -rsst 'RSS feed title' -rssd 'RSS feed description'

Only "-rss" is required, "-rsst" and "-rssd" parameters are optional, but you should use them.
This functionality depends on python-feedgen.

Example site
------------
You can visit https://badai.xyz to see a website generated with ssgen in production.

Usage
-----
ssgen:

    ./ssgen.py src dest template
    
Force regeneration:

    ./ssgen.py src dest template force

Sitemap generator:

    ./sitemap-gen.py baseurl sourcedir output

Bugs
----
Please leave bug reports to https://gitlab.com/4shadoww/ssgen.

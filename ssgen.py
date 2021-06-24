#!/usr/bin/env python3

# Copyright (C) 2021 Noa-Emil Nissinen

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.    If not, see <https://www.gnu.org/licenses/>.

import sys
import os
from datetime import datetime
import subprocess
import shutil
import re

to_html_command = "pandoc --mathjax -f markdown -t html \"$input_file$\""
master = ""
src_dir = ""
dest_dir = ""
master_path = ""
generated_files = 0
copied_resources = 0
articles = []
article_list_html = ""
recent_articles_html = ""
current_file_index = 0


def get_current_dir():
    return os.getcwd() + '/'


def needs_update(path, new_path):
    try:
        new_mod = os.stat(new_path).st_mtime
    except FileNotFoundError:
        return True

    src_mod = os.stat(path).st_mtime
    return src_mod > new_mod


def get_article_info(index):
    for article in articles:
        if article[0] == index: return article

    return None


def generate_article_list():
    global article_list_html
    global recent_articles_html
    articles.sort(key = lambda articles: articles[3], reverse=True)

    i = 0
    html = "<ul>"

    for article in articles:
        html += "<li>" + article[3] + " – <a href=\"/articles/" + article[2] + "\">" + article[1] + "</a></li>"

        if i == 8:
            recent_articles_html = html + "</ul>"

    html += "</ul>"

    if recent_articles_html == "":
        recent_articles_html = html

    article_list_html = html


def replace_magics(html):
    html = html.replace("{{ARTICLES}}", article_list_html, 1)
    html = html.replace("{{RECENT}}", recent_articles_html, 1)
    return html


def replace_after_magics(html):
    html = html.replace("{{TIME}}", datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
    if("{{PUBLISHDATE}}" in html):
        html = html.replace("{{PUBLISHDATE}}", get_article_info(current_file_index)[3], 1)

    return html


def format_article_filename(filename, pattern=r"[^a-z0-9\-\.]"):
    filename = filename.lower()
    filename = re.sub(pattern, "", filename)

    return filename

def generate_copy_files(files):
    global current_file_index
    current_file_index = 0
    # Find articles for {{ARTICLES}} and {{RECENT}}
    i = 0
    for path in files:
        if src_dir + "articles/" in path:
            article = path[len(src_dir) + 9:]
            if article.endswith('.md'):
                form = article[:-3]
                article = form + ".html"
            elif article.endswith('.content'):
                form = article[:-12]
                article = form + ".html"
            elif article.endswith(".wipwip"):
                i += 1
                continue

            temp = form.split('-')
            date = '-'.join(temp[:3])
            title = ' '.join(temp[3:])

            articles.append([i, title, format_article_filename(article), date])

        i += 1

    generate_article_list()

    for path in files:
        if path == master_path:
            current_file_index += 1
            continue
        elif path.endswith('.md'):
            markdown_to_html(path)
        elif path.endswith('.content'):
            content_to_html(path)
        elif path.endswith('.wipwip'):
            current_file_index += 1
            continue
        else:
            copy_resource(path)

        current_file_index += 1


def get_files(path):
    subfolders, files = [], []

    for f in os.scandir(path):
        if f.name.startswith('.'): continue
        elif f.is_dir():
            subfolders.append(f.path)
        elif f.is_file():
            files.append(f.path)
    for _path in list(subfolders):
        sf, f = get_files(_path)
        subfolders.extend(sf)
        files.extend(f)

    return subfolders, files


def write_html(html, target_dir, f_name_new):
    html = replace_magics(html)
    target_dir = dir_format(target_dir)
    try:
        os.makedirs(target_dir)
    except FileExistsError: pass
    final_html = master.replace("{{CONTENT}}", html, 1)
    final_html = replace_after_magics(final_html)
    f = open(target_dir + f_name_new, 'w')
    f.write(final_html)
    f.close()

    return True


def copy_resource(f):
    global copied_resources
    f_name = f.split('/')[-1:][0]
    target_dir = dest_dir + get_dir_structure(f, src_dir, f_name)

    if not needs_update(f, target_dir + f_name): return

    try:
        os.makedirs(target_dir)
    except FileExistsError: pass
    shutil.copyfile(f, target_dir + f_name)
    copied_resources += 1


def content_to_html(path):
    global generated_files
    target_dir, f_name = get_target_name_dir(path)
    f_name_new = f_name[:-8]
    if "articles/" in path: f_name_new = format_article_filename(f_name_new)

    if not needs_update(path, target_dir + f_name_new) and not needs_update(master_path, target_dir + f_name_new):
        return

    f = open(path, 'r')
    html = f.read()
    f.close()
    write_html(html, target_dir, f_name_new)
    generated_files += 1


def markdown_to_html(path):
    global generated_files
    target_dir, f_name = get_target_name_dir(path)
    f_name_new = f_name[:-2] + "html"
    if "articles/" in path: f_name_new = format_article_filename(f_name_new)

    if not needs_update(path, target_dir + f_name_new) and not needs_update(master_path, target_dir + f_name_new): return

    res = subprocess.check_output(to_html_command.replace("$input_file$", path, 1), shell=True).decode('utf-8')
    write_html(res, target_dir, f_name_new)
    generated_files += 1


def get_target_name_dir(path):
    f_name = path.split('/')[-1:][0]
    target_dir = dest_dir + get_dir_structure(path, src_dir, f_name)
    return target_dir, f_name


def get_dir_structure(path, start, end):
    return path[len(start):-len(end)]


def dir_format(str):
    if str.endswith('/'): return str
    return str + '/'


def print_usage():
    print("usage:", sys.argv[0], "src dest template")

    options = """\nOptions:
    src\t\t\tmarkdown source directory
    dest\t\tdestination directory
    template\t\ttemplate html file
    """

    print(options)


def main():
    global master
    global src_dir
    global dest_dir
    global master_path

    # Parse arguments
    if len(sys.argv) < 4:
        print_usage()
        sys.exit(1)

    src_dir = dir_format(sys.argv[1])
    dest_dir = dir_format(sys.argv[2])
    master_path = src_dir + sys.argv[3]

    _, files = get_files(src_dir)

    # Load master html
    try:
        master_f = open(master_path, 'r')
        master = master_f.read()
        master_f.close()
    except Exception as e:
        print(e)
        sys.exit(1)

    # Generate files and copy resources
    generate_copy_files(files)

    print("generated", generated_files, "html file(s)")
    print("copied", copied_resources, "file(s)")

if __name__ == '__main__':
    main()

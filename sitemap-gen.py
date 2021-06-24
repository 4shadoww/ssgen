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

import xml.etree.cElementTree as ET
import sys
import os
from datetime import datetime


valid_documents = ['.html', '.php']
black_list = ["404.html"]


def is_document(f):
    for ext in valid_documents:
        if f.endswith(ext):
            for item in black_list:
                if item not in f: return True

    return False


def dir_format(str):
    if str.endswith('/'): return str
    return str + '/'


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


def print_usage():
    print(sys.argv[0] + " baseurl sourcedir output")


def main():
    if len(sys.argv) < 4:
        print_usage()
        sys.exit(1)

    base_url = dir_format(sys.argv[1])
    src_dir = dir_format(sys.argv[2])
    src_dir_len = len(src_dir)
    output = sys.argv[3]

    print("finding files...")
    _, files = get_files(src_dir)

    print("generating sitemap...")

    urlset = ET.Element("urlset")
    urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")

    for f in files:
        if is_document(f):
            timestamp = os.stat(f).st_mtime
            modified = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")

            url = base_url + f[src_dir_len:]

            urltag = ET.SubElement(urlset, "url")
            loc = ET.SubElement(urltag, "loc")
            loc.text = url
            lastmodtag = ET.SubElement(urltag, "lastmod")
            lastmodtag.text = modified

    tree = ET.ElementTree(urlset)

    tree.write(output)


if __name__ == "__main__":
    main()

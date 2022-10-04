"""
Parsing No Man's Ski Fandom WIki Cooking
https://nomanssky.fandom.com/wiki/Cooking_Products
"""
# TODO Load file for parsing from http
# TODO Github, branch without parsing fuctions
# TODO Problems revision
# TODO Comments, docstring, typig for BS

import csv
from dataclasses import dataclass, astuple
from bs4 import BeautifulSoup

FILE_FOR_PARSING = "html_source/wiki_cooking/Cooking Products - No Man's Sky Wiki.html"


@dataclass
class Item:
    group: str
    sub_group: str
    name: str
    # ptcture_link: str
    link: str


def parse_group(h2_tag) -> str:
    return str(h2_tag.find('span', {'class': 'mw-headline'}).string)


def parse_sub_group(h3_tag) -> str:
    return str(h3_tag.find('span', {'class': 'mw-headline'}).string) if h3_tag else ''


def parse_name(li_tag) -> str:
    return str(li_tag.div.find('p').a.string)


def parse_picture_link(li_tag) -> str:  # not used now
    return str(li_tag.div.div.div.a.img['src'])


def parse_link(li_tag) -> str:
    return str(li_tag.div.find('p').a['href'])


def parse_names(ul_tag, group, sub_group) -> list[Item]:
    return [Item(group=parse_group(group),
                 sub_group=parse_sub_group(sub_group),
                 name=parse_name(name),
                 # ptcture_link=parse_picture_link(name),
                 link=parse_link(name))
            for name in ul_tag.findAll('li')]


def dataclass2csv(filename: str, rows: list[Item], header: bool = True):
    with open(filename, 'w', encoding='utf-8', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, dialect='unix')
        if header:
            csv_writer.writerow(['group', 'subgroup', 'name', 'link'])
        csv_writer.writerows([astuple(row) for row in rows])


with open(FILE_FOR_PARSING, encoding='utf-8') as file_for_parsing:  # TODO To Ext function
    html_doc = file_for_parsing.read()

tags = BeautifulSoup(html_doc, 'html.parser') \
    .find('div', {'class': 'mw-parser-output'}) \
    .find('span', id='Summary').parent \
    .find_next_siblings(['h2', 'h3', 'ul'])

items: list[Item] = []
for tag in tags:
    match tag.name:
        case 'h2':
            h2 = tag
            h3 = None  # Optionaly
        case 'h3':
            h3 = tag
        case 'ul':
            items += parse_names(tag, h2, h3)

dataclass2csv('data.csv', items)

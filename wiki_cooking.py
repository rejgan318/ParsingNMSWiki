"""
Parsing No Man's Ski Fandom WIki Cooking
https://nomanssky.fandom.com/wiki/Cooking_Products
"""

# TODO tag from pycharm to github?

from dataclasses import dataclass, astuple, fields
import csv
from bs4 import BeautifulSoup
import requests

URL_FOR_PARSING = "https://nomanssky.fandom.com/wiki/Cooking_Products"
CSV_FOR_SAVE = "coocking_items.csv"


@dataclass(frozen=True)
class Item:
    group: str
    sub_group: str
    name: str
    link: str


def save_dataclass_to_csv(filename: str, rows: list[Item], header: bool = True):
    with open(filename, 'w', encoding='utf-8', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, dialect='unix')
        if header:
            csv_writer.writerow([field.name for field in fields(rows[0])])
        csv_writer.writerows([astuple(row) for row in rows])


html_doc = requests.get(URL_FOR_PARSING).text
tags = BeautifulSoup(html_doc, 'html.parser') \
    .find('div', {'class': 'mw-parser-output'}) \
    .find('span', id='Summary').parent \
    .find_next_siblings(['h2', 'h3', 'ul'])

items: list[Item] = []
for tag in tags:
    match tag.name:
        case 'h2':
            group = str(tag.find('span', {'class': 'mw-headline'}).string)
            sub_group = ''
        case 'h3':
            sub_group = str(tag.find('span', {'class': 'mw-headline'}).string)
        case 'ul':
            items += [Item(group=group,
                           sub_group=sub_group,
                           name=str((a_tag := li_tag.div.find('p').a).string),
                           link=str(a_tag['href']))
                      for li_tag in tag.findAll('li')]

save_dataclass_to_csv(CSV_FOR_SAVE, items)

import csv
from dataclasses import dataclass, asdict, fields, astuple
import itertools

CSV_FILE = r"..\coocking_items.csv"


@dataclass()
class Item:
    id: int
    name: str
    id_group: int
    id_subgroup: int
    name_lacale: str
    link: str


@dataclass()
class Group:
    id: int
    name: str


@dataclass()
class Subgroup:
    id: int
    name: str


def get_id_by_name(data, key: str, name: str) -> int:
    for row in data:
        if row[key] == name:
            return row['id']
    return -1


def export2csv_groups_and_subgoups(filename: str, data: list[dict]):
    with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, dialect='unix')
        csv_writer.writerow(data[0].keys())
        csv_writer.writerows([row.values() for row in data])


def export2csv_items(filename: str, rows: list):
    with open(filename, 'w', encoding='utf-8', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, dialect='unix')
        csv_writer.writerow([field.name for field in fields(rows[0])])
        csv_writer.writerows([astuple(row) for row in rows])


with open(CSV_FILE, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, dialect='unix')
    items = [row for row in csv_reader][1:]

num_id = 1
db_items: list[Item] = []
groups = [{'id': i + 1, 'group': group} for i, group in enumerate(sorted(list(set([row[0] for row in items]))))]
subgroups = [{'id': i + 1, 'subgroup': subgroup} for i, subgroup in enumerate(sorted(list(set([row[1] for row in items]))))]
for item in items:
    db_items.append(Item(id=num_id, name=item[2], id_group=get_id_by_name(groups, 'group', item[0]),
                         id_subgroup=get_id_by_name(subgroups, 'subgroup', item[1]),
                         name_lacale='',
                         link=item[3]))
    num_id += 1

export2csv_groups_and_subgoups(r"csv_for_db\groups.csv", groups)
export2csv_groups_and_subgoups(r"csv_for_db\subgroups.csv", subgroups)
export2csv_items(r"csv_for_db\items.csv", db_items)

print('Done')

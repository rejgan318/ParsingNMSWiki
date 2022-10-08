""" Research graph """

from dataclasses import dataclass, field


@dataclass()
class Node:
    name: str
    relations: list[str] = field(default_factory=list)

def read_graph(file_name):
    with open(file_name) as file:
        full_grapf = []
        for graph in file:
            ws = graph.strip().split(' ')
            full_grapf.append(Node(name=ws[0], relations=list(ws[1] if len(ws) == 2 else [])))
        return full_grapf


def main():
    full_graph = read_graph('topograph.txt')
    print(full_graph)
    current = full_graph[0].name

    print('Done.')


if __name__ == '__main__':
    main()

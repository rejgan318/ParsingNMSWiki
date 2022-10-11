"""
Research graph
1. Read graph topology from txt-file
    <Node-name> <Node-name1><Node-name2>...
    Example:
A BC
B D
C EF
D G
G IJH
I
J KG
K
H
E LM
L
M
F

    Graph can be with back relation - look "J KG"
2. Recursive parcing from top node start_node_name
3. Calculate unicum names nodes
"""
from dataclasses import dataclass, field, asdict


@dataclass()
class Node:
    name: str
    relations: list[str] = field(default_factory=list)


class Nodes:
    def __init__(self, file_name: str):
        self.full_grapf = dict({})
        self.names = set({})
        self.read_graph(file_name)

    def read_graph(self, file_name):
        with open(file_name) as file:
            for graph in file:
                node_config_str = graph.strip().split(' ')
                self.full_grapf[node_config_str[0]] = Node(name=node_config_str[0],
                                                           relations=list(
                                                               node_config_str[1] if len(node_config_str) == 2 else []))

    def get_node(self, name):
        return Node(**asdict(self.full_grapf[name]))

    def parse_node(self, node: Node):
        self.names = self.names | {node.name}
        for rel in node.relations:
            rel_node = self.get_node(rel)
            if not (rel_node.name in self.names):
                added_names = self.parse_node(rel_node)
                self.names = self.names | added_names
        return self.names


def main():
    start_node_name = 'A'
    nodes = Nodes('topograph.txt')
    nodes.parse_node(nodes.get_node(start_node_name))
    print(sorted(list(nodes.names)))
    print('Done.')


if __name__ == '__main__':
    main()

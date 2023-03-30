"""
Perform A* algorithm to find solution
uses Euclidean distance for the heuristics
"""
# from typing import Self  # Only on python 3.11


class Node:
    def __init__(self, x: int, y: int, t: int,
                 parent=None):
        self.x = x
        self.y = y
        self.t = t
        self.heuristic = -1
        self.dist_start = -1
        self.dist_target = -1
        self.g_cost = 0
        self.parent = parent

    def copy(self, other) -> None:
        self.heuristic = other.heuristic
        self.g_cost = other.g_cost
        self.parent = other.parent

    def __gt__(self, other) -> bool:
        if isinstance(other, Node):
            if self.heuristic == other.heuristic:
                return self.dist_target > other.dist_target
            return self.heuristic > other.heuristic

    def __eq__(self, other) -> bool:
        return ((self.x == other.x) and
                (self.y == other.y) and
                (self.t == other.t))


class Graph:
    def __init__(self):
        self.nodes = []

    def add_node(self, node: Node):
        self.nodes.append(node)

    def find_node(self, node: Node):
        for node_t in self.nodes:
            if node_t == node:
                return node

    def get_path(self, end_node: Node):
        path = []
        while end_node.parent is not None:
            path.append(end_node)
            end_node = end_node.parent
        path.append(end_node)
        path.reverse()
        return path

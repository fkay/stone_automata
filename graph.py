"""
Perform A* algorithm to find solution
uses Euclidean distance for the heuristics
"""
# from typing import Self  # Only on python 3.11


class Node:
    def __init__(self, x: int, y: int, t: int,
                 parent=None, remain_lifes: int = 0):
        self.x = x
        self.y = y
        self.t = t
        self.h_cost = -1
        self.g_cost = 0
        self.f_cost = -1
        self.parent = parent
        self.remain_lifes = remain_lifes

    def copy(self, other) -> None:
        self.h_cost = other.h_cost
        self.g_cost = other.g_cost
        self.f_cost = self.h_cost + self.g_cost
        self.parent = other.parent

    def __gt__(self, other) -> bool:
        if isinstance(other, Node):
            if self.f_cost == other.f_cost:
                if self.remain_lifes == other.remain_lifes:
                    return self.h_cost > other.h_cost
                return self.remain_lifes < other.remain_lifes
            return self.f_cost > other.f_cost

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

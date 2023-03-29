import math
from automata import find_postion, next_step_map
from graph import Graph, Node


class A_star:
    def __init__(self, init_map: list[list[int]]):
        self.maps = [init_map]      # maps for every timeframe
        self.start = find_postion(init_map, 3)
        self.target = find_postion(init_map, 4)
        self.graph = Graph()
        start_node = Node(self.start['x'], self.start['y'], 0)
        self.calculate_distances(start_node)
        self.graph.add_node(start_node)
        self.rows = len(init_map)
        self.cols = len(init_map[0])
        # self.create_children(self.node[0])

    def create_children(self, node: Node) -> list[Node]:
        children = []
        next_t = node.t + 1
        if len(self.maps) < (next_t + 1):
            self.maps.append(next_step_map(
                self.maps[-1]
            ))
        for y, x in [(-1, 0), (1, 0),
                     (0, -1), (0, 1)]:
            if (node.y + y >= 0 and
               node.y + y < self.rows and
               node.x + x >= 0 and
               node.x + x < self.cols and
               self.maps[next_t][node.y + y][node.x + x] == 0):
                new_node = Node(node.x + x, node.y + y, next_t, node)
                # if node already exist on graph, append it
                if self.graph.find_node(new_node) is None:
                    self.calculate_distances(new_node)
                    self.graph.add_node(new_node)
                    children.append(new_node)
        return children

    def calculate_distances(self, node: Node):
        dist_start = math.sqrt((node.x - self.start['x'])**2 +
                               (node.y - self.start['y'])**2) + node.t
        dist_target = math.sqrt((node.x - self.target['x'])**2 +
                                (node.y - self.target['y'])**2)
        node.dist_start = dist_start
        node.heuristic = dist_start + dist_target

    def calculate_movements(self, path: list[Node]) -> list[chr]:
        moves = []
        prev_node = path[0]
        for node in path[1:]:
            if node.x - prev_node.x > 0:
                moves.append('R')
            elif node.x - prev_node.x < 0:
                moves.append('L')
            elif node.y - prev_node.y > 0:
                moves.append('D')
            else:
                moves.append('U')
            prev_node = node
        return moves

    def solve(self) -> list[chr]:
        """
        Solve the map, return list with movements:
        U - up
        D - down
        L - left
        R - right

        Returns:
            list[chr]: list with the movevements to solve
        """
        # put root node as starting node
        open_nodes = [self.graph.nodes[0]]
        # closed nodes empty
        close_nodes = []

        while True:
            if len(open_nodes) == 0:
                print('No solution found')
                return []

            open_nodes.sort()
            actual_node = open_nodes.pop(0)
            close_nodes.append(actual_node)
            if (actual_node.x == self.target['x'] and
               actual_node.y == self.target['y']):
                # found solution
                path = self.graph.get_path(actual_node)
                return self.calculate_movements(path)

            # open next steps of this node
            next_nodes = self.create_children(actual_node)
            for next_node in next_nodes:
                if (next_node not in close_nodes and
                   next_node not in open_nodes):
                    # only open with already not visited
                    open_nodes.append(next_node)

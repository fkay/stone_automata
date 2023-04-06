import math
import time
from datetime import timedelta
from automata import find_postion, next_step_map_convolve, load_init_map
from graph import Graph, Node


class A_star:
    def __init__(self, init_map: list[list[int]],
                 heuristics_type: str = 'manhattan',
                 heuristics_const: float = 3.0,
                 init_lifes: int = 1):
        self.maps = [init_map]  # maps for every time frame
        # self.start = find_postion(init_map, 3)
        # self.target = find_postion(init_map, 4)
        self.start = {'x': 0, 'y': 0}
        self.target = {'x': init_map.shape[1] - 1, 'y': init_map.shape[0] - 1}
        self.graph = Graph()
        start_node = Node(self.start['x'], self.start['y'], 0,
                          parent=None, remain_lifes=init_lifes)
        self.heuristics_const = heuristics_const
        if heuristics_type == 'manhattan':
            self.heuristics = self.calc_manhattan
        else:
            self.heuristics = self.calc_euclidean
        if heuristics_const == 0:
            self.heuristics = self.calc_zero_heuristic
        start_node.g_cost = 0
        self.heuristics(start_node)
        start_node.f_cost = 0
        self.graph.add_node(start_node)
        self.rows = len(init_map)
        self.cols = len(init_map[0])
        self.lifes = init_lifes

    def calc_zero_heuristic(self, node: Node) -> None:
        node.h_cost = 0

    def calc_manhattan(self, node: Node) -> None:
        node.h_cost = (abs(node.x - self.target['x']) +
                       abs(node.y - self.target['y'])) * self.heuristics_const

    def calc_euclidean(self, node: Node) -> None:
        node.h_cost = math.sqrt(
            (node.x - self.target['x'])**2 +
            (node.y - self.target['y'])**2
            ) * self.heuristics_const

    def create_children(self, node: Node) -> list[Node]:
        children = []
        next_t = node.t + 1
        if len(self.maps) < (next_t + 1):
            self.maps.append(next_step_map_convolve(
                self.maps[-1]
            ))
        for y, x in [(-1, 0), (1, 0),
                     (0, -1), (0, 1)]:
            if (node.y + y >= 0 and
               node.y + y < self.rows and
               node.x + x >= 0 and
               node.x + x < self.cols):
                next_value = self.maps[next_t][node.y + y][node.x + x]
                if (next_value != 1 or
                   node.remain_lifes > 1):
                    new_node = Node(node.x + x, node.y + y, next_t, node,
                                    node.remain_lifes - next_value)
                    children.append(new_node)
        return children

    def calculate_costs(self, node: Node):
        node.g_cost = node.parent.g_cost + 1  # + (self.lifes - node.remain_lifes)  # noqa
        # calc h_cost
        self.heuristics(node)
        # f_cost
        node.f_cost = node.g_cost + node.h_cost

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
        _start = time.monotonic()
        nodes_visited = 0
        # put root node as starting node
        open_nodes = [self.graph.nodes[0]]
        # closed nodes empty
        close_nodes = []

        while True:
            if len(open_nodes) == 0:
                print('No solution found')
                sol = []
                break

            nodes_visited += 1

            open_nodes.sort()
            actual_node = open_nodes.pop(0)
            close_nodes.append(actual_node)

            if nodes_visited % 1000 == 0:
                print(f'open nodes: {len(open_nodes)}')
                print(f'closed nodes: {nodes_visited}')
                print(f'maps generated: {len(self.maps)}')
                # print(f'graph_size: {len(self.graph.nodes)}')
                print(f'Actual node: x:{actual_node.x} | ' +
                      f'y: {actual_node.y} | ' +
                      f't: {actual_node.t} | ' +
                      f'g_cost: {actual_node.g_cost} | ' +
                      f'h_cost: {actual_node.h_cost} | ' +
                      f'f_cost: {actual_node.f_cost}')

            if (actual_node.x == self.target['x'] and
               actual_node.y == self.target['y']):
                # found solution
                path = self.graph.get_path(actual_node)
                sol = self.calculate_movements(path)
                break

            # open next steps of this node
            next_nodes = self.create_children(actual_node)
            for next_node in next_nodes:
                if next_node in close_nodes or next_node in open_nodes:
                    continue

                self.calculate_costs(next_node)
                open_nodes.append(next_node)
                self.graph.add_node(next_node)
        _end = time.monotonic()
        print('Time to solve: ' + str(timedelta(seconds=_end - _start)))
        return sol


if __name__ == '__main__':
    # %% load the initial map
    init_map = load_init_map()
    init_map = init_map[10:40, 20:50]
    init_map[0, 0] = 0  # 3
    init_map[-1, -1] = 0  # 4

    solution = A_star(init_map, heuristics_type='manhattan',
                      heuristics_const=0,
                      init_lifes=5).solve()
    print(f'Solution length: {len(solution)}')
    solution = ' '.join(solution)
    print(solution)

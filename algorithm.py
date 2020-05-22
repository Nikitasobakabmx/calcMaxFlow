import numpy as np


def _gen(line):
    for i in range(len(line)):
        yield line[i], i


class GraphPath:
    def __init__(self, graph=None):
        self.graph = graph

    def split_str(self, string: str):
        self.graph = np.array(
            [
                np.int32(i.split()) for i in string.split(sep="\n")
            ], dtype=np.int32)

    def input_graph(self, size):
        """it is specific input from stdin you might input like:
                1 2 3
                4 5 6
                7 8 9
        """
        self.graph = np.array(
            [
                np.int32(input().split()) for _ in range(size)
            ], dtype=np.int32)

    def find_max_power(self, begin, end):
        graph = self.graph.copy()
        path = self._get_path(graph, [begin - 1, ], end)
        power = list()
        while path:
            mask_x = np.array(path[1:])
            mask_y = np.array(path[:-1])
            costs = graph[mask_y, mask_x]
            power.append(np.min(graph[mask_y, mask_x]))
            # print(graph[mask_x, mask_y])
            # print(mask_x, mask_y)
            graph[mask_x, mask_y] += power[-1]
            graph = graph.T
            graph[mask_x, mask_y] -= power[-1]
            graph = graph.T
            more_then_zero = graph < 0
            positive_graph = graph.copy()
            positive_graph[more_then_zero] = 0
            # print(graph)
            print("Path : {0}, power : {1}, costs {2}, graph : {3}"
                  .format(path,
                          power[-1],
                          costs,
                          graph))
            path = self._get_path(positive_graph, [begin - 1, ], end)
        return sum(power), graph

    def check_point_one(self, power, graph):
        check_top = self.graph[0] - graph[0]
        check_top = sum(check_top) == power
        check_but = graph[-1] - self.graph[-1]
        check_but = sum(check_but) == power
        return check_top and check_but

    def check_point_two(self, s: set, power):
        result = 0
        # print()
        for i in s:
            for item, pos in _gen(self.graph[i]):
                if item:
                    if pos in s:
                        continue
                    result += item
                    # print("step : {0}, result : {1}, item : {2}, graph : {3}"
                    #       .format(i, result, item, self.graph[i]))
        # print("S : ", result)
        if power <= result:
            return True
        return False

    def find_section(self, graph, path, pos=0):
        path.add(pos)
        for item, position in _gen(graph[pos]):
            if item:

                # print(item, position)
                if pos == position or position in path:
                    continue
                path.update(self.find_section(graph, path, position))
        return path

    def _get_path(self, gr, path, direction):
        for item, pos in _gen(gr[path[-1]]):
            if item:
                if pos in path:
                    continue
                if pos == (direction - 1):
                    return path + [pos, ]
                tmp = self._get_path(gr, path + [pos, ], direction)
                if tmp:
                    return tmp
        return []

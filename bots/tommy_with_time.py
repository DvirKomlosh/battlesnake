from api import *
import math
import time
import random


def manhattan_distance(coord, coord2):
    return abs(coord[0] - coord2[0]) + abs(coord[1] - coord2[1])


def next_to(origin, destination):
    """assumes the two coords are legal"""
    return manhattan_distance(origin, destination) == 1


class Graph:
    def __init__(self, width, height, occupied):
        self.vertices = [[x, y] for x in range(width) for y in range(height)]

        self.edges = self.generate_edges(occupied)

    def generate_edges(self, occupied):
        adj_matrix = {tuple(vertex): [] for vertex in self.vertices}

        for origin in self.vertices:
            for destination in self.vertices:
                if tuple(destination) not in occupied and next_to(origin, destination):
                    adj_matrix[tuple(origin)].append(destination)

        return adj_matrix

    def bfs(self, curr_pos):
        visited = {tuple(vertex): False for vertex in self.vertices}

        queue = [list(curr_pos)]

        structure = {curr_pos: None}
        visited[curr_pos] = True

        while queue:
            v = queue.pop(0)

            for neighbor in self.edges[tuple(v)]:
                if not visited[tuple(neighbor)]:
                    queue.append(neighbor)

                    if tuple(neighbor) not in structure:
                        structure[tuple(neighbor)] = v

                    visited[tuple(neighbor)] = True

        return structure


def find_dist(paths, dst):
    dist = -1
    prev = None
    prev_prev = None
    if tuple(dst) not in paths:
        return math.inf, None

    while dst != None:
        prev_prev = prev
        prev = dst
        dst = paths[tuple(dst)]
        dist += 1

    return dist, prev_prev


class MyBot(CodeBattlesBot):
    times = []

    def choose_destination(self, paths):
        min_obj = None
        min_val = math.inf

        for apple in self.context.get_apples():
            dist, prev = find_dist(paths, apple)
            if dist <= min_val:
                min_val = dist
                min_obj = prev

        if math.isinf(min_val):
            return None

        return min_obj

    def calc_move(self, move_to):
        if move_to is None:
            return None

        x, y = self.context.get_position(self.context.get_myself())[-1]
        dst_x, dst_y = move_to

        if dst_x == x:
            if dst_y == y + 1:
                return "U"

            if dst_y == y - 1:
                return "D"

        if dst_y == y:
            if dst_x == x + 1:
                return "R"

            if dst_x == x - 1:
                return "L"

        return None

    def run(self) -> None:
        start = time.time()
        size = self.context.get_game_size()
        head = self.context.get_position(self.context.get_myself())[-1]
        graph = Graph(size[0], size[1], self.context.get_occupied_tiles())

        paths = graph.bfs(head)

        move_to = self.choose_destination(paths)

        val = self.calc_move(move_to)

        if val is None:
            return

        self.context.set_direction(val)
        self.times.append(time.time() - start)
        print("average tommy : ", sum(self.times) / len(self.times))

    def setup(self) -> None:
        pass

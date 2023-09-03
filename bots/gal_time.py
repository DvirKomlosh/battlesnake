from api import *
import math
from typing import Tuple
import time

Point = Tuple[int, int]


def manhattan_distance(coord: Point, coord2: Point) -> int:
    return abs(coord[0] - coord2[0]) + abs(coord[1] - coord2[1])


def dir_to(src: Point, dst: Point) -> str:
    assert manhattan_distance(src, dst) == 1
    sx, sy = src
    dx, dy = dst
    if dx == sx + 1:
        return "R"
    if dx == sx - 1:
        return "L"
    if dy == sy + 1:
        return "U"
    if dy == sy - 1:
        return "D"
    assert False


class MyBot(CodeBattlesBot):
    times = []

    def get_head_pos(self) -> Point:
        return self.context.get_position(self.me)[-1]

    def get_avail_neighs(self, loc: Point) -> List[Point]:
        x, y = loc
        options = [(x, y + 1), (x + 1, y), (x - 1, y), (x, y - 1)]
        good_options = []
        for pt in options:
            if pt not in self.context.get_occupied_tiles() and self.context.in_bounds(
                pt
            ):
                good_options.append(pt)
        return good_options

    def move_toward(self, target: Point) -> Tuple[str, int]:
        root = self.get_head_pos()
        if root == target:
            return None

        q = [root]
        parent = {root: None}

        while len(q) != 0:
            v = q.pop(0)
            if v == target:
                dist = 0
                while True:
                    prev = parent[v]
                    dist += 1
                    if prev == root:
                        return dir_to(root, v), dist
                    v = prev

            for neigh in self.get_avail_neighs(v):
                if neigh in parent:
                    continue
                parent[neigh] = v
                q.append(neigh)

        # Unreachable
        return None

    def survive_move(self) -> str:
        opts = self.get_avail_neighs(self.get_head_pos())
        if len(opts) == 0:
            return "U"
        else:
            return dir_to(self.get_head_pos(), opts[0])

    def run(self) -> None:
        start = time.time()

        self.me = self.context.get_myself()

        move = self.survive_move()

        best_dist = None
        if self.context.get_health(self.me) < 50:
            for apple in self.context.get_apples():
                opt_amove = self.move_toward(apple)
                if opt_amove is not None:
                    amove, dist = opt_amove

                    if best_dist is None or dist < best_dist:
                        move = amove
                        best_dist = dist

        self.context.set_direction(move)
        self.times.append(time.time() - start)
        print("average gal : ", sum(self.times) / len(self.times))

    def setup(self) -> None:
        pass

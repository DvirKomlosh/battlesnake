import math
import random
import time

from api import *


APPLE_POINTS = 15
SNAKE_PUNISHMENT = 8
AFRAID_OF_MYSELF = 1 / 25


def manhattan_distance(coord, coord2) -> int:
    return abs(coord[0] - coord2[0]) + abs(coord[1] - coord2[1])


def get_directions(coord, coord2) -> list[str]:
    x1, y1 = coord
    x2, y2 = coord2
    directions = []
    if y2 > y1:
        directions.append("U")
    elif y2 < y1:
        directions.append("D")
    if x2 > x1:
        directions.append("R")
    elif x2 < x1:
        directions.append("L")
    return directions


class MyBot(CodeBattlesBot):
    times = []
    me = None
    my_head = None
    step_start_time = None
    hungry = False
    points = None

    def get_available_options(self) -> list[str]:
        # returns all non killing coordinates for next move
        all_options = self.get_all_options()
        options = []
        for direction, coord in all_options.items():
            if (
                coord not in self.context.get_occupied_tiles()
                and self.context.in_bounds(coord)
            ):
                options.append(direction)
        random.shuffle(options)
        return options

    def get_all_options(self) -> dict[str, tuple[int, int]]:
        # returns all coordinates for next move
        x, y = self.my_head
        return {"U": (x, y + 1), "D": (x, y - 1), "L": (x - 1, y), "R": (x + 1, y)}

    def get_head(self, snake: PlayerState) -> tuple[int, int]:
        return self.context.get_position(snake)[-1]

    def initialize_variables(self):
        # helper function to set variables that will not change during the step
        self.step_start_time = time.time()
        self.me = self.context.get_myself()
        self.my_head = self.get_head(self.me)
        if self.context.get_has_eaten_last_step(self.me):
            self.hungry = False

    def get_closest_apple(self) -> tuple[int, int]:
        return min(
            self.context.get_apples(),
            key=lambda coord: manhattan_distance(self.my_head, coord),
        )

    def should_eat(self) -> bool:
        self.hungry = self.hungry or self.context.get_health(
            self.me
        ) < 5 * manhattan_distance(self.my_head, self.get_closest_apple())
        return self.hungry
        # return self.context.get_health(self.me) < 20 * manhattan_distance(self.my_head, self.get_closest_apple())

    def consider_apples(self):
        apple = self.get_closest_apple()
        for direction in get_directions(self.my_head, apple):
            if direction in self.points:
                self.points[direction] += APPLE_POINTS

    def consider_collisions(self):
        for snake in self.context.get_active_players():
            factor = 1
            if self.get_head(snake) == self.my_head:
                factor = AFRAID_OF_MYSELF
            for coord in self.context.get_position(snake):
                if coord == self.my_head:
                    continue
                dist = manhattan_distance(coord, self.my_head)
                punishment = factor * SNAKE_PUNISHMENT / (dist**2)
                for direction in get_directions(self.my_head, coord):
                    if direction in self.points:
                        self.points[direction] -= punishment

    def run(self) -> None:
        self.initialize_variables()

        move = "U"
        options = self.get_available_options()
        self.points = {direction: 0.0 for direction in options}
        if self.should_eat():
            self.consider_apples()
        self.consider_collisions()
        if len(options) > 0:
            # takes the a random available option which should not kill him
            # move = list(options.keys())[random.randint(0, len(options) - 1)]
            move = max(self.points.keys(), key=self.points.__getitem__)
        self.context.set_direction(move)

        self.times.append(time.time() - self.step_start_time)
        # print the average time every 100 steps:
        if len(self.times) % 100 == 0:
            print("average time per turn : ", sum(self.times) / len(self.times))

    def setup(self) -> None:
        pass

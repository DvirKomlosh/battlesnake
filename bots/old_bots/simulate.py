import copy
import math
from api import *

BORDER_DANGER = 2
BODY_DANGER = 2
HEAD_DANGER = 4

INFTY = 100000


def manhattan_distance(coord, coord2):
    return abs(coord[0] - coord2[0]) + abs(coord[1] - coord2[1])


class MyBot(CodeBattlesBot):
    state = None
    players = None
    danger_map = None
    food_map = None

    def update_state(self):
        self.state = self.context.get_state()
        self.players = self.state.players
        self.me = self.context.get_player()
        self.simulated_state = copy.deepcopy(self.state)

    def choose_direction(self):
        x, y = self.me.head
        up = (x, y + 1)
        down = (x, y - 1)
        right = (x + 1, y)
        left = (x - 1, y)

        options = [up, down, right, left]
        options = [option for option in options if self.state.in_bounds(option)]
        best_value = self.calculate_value(options[0])
        best_option = options[0]

        for option in options:
            if best_value < self.calculate_value(option):
                best_value = self.calculate_value(option)
                best_option = option

        if best_option == up:
            return "U"
        if best_option == down:
            return "D"
        if best_option == right:
            return "R"
        if best_option == left:
            return "L"

    def run(self) -> None:
        self.update_state()
        self.calc_danger_map()
        self.calc_food_map(int((140 - self.me.hunger) / 15))

        self.context.set_direction(self.choose_direction())

    def setup(self) -> None:
        pass

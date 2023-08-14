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

    def propagate(self, coord, value, map):
        for i in range(coord[0] - value, coord[0] + value + 1):
            for j in range(coord[1] - value, coord[1] + value + 1):
                if self.state.in_bounds((i, j)):
                    map[(i, j)] += max(0, value - manhattan_distance(coord, (i, j)))

    def calc_food_map(self, value):
        self.food_map = {
            (i, j): 0 for i in range(self.state.width) for j in range(self.state.height)
        }
        for apple in self.state.apples:
            self.propagate(apple, value, self.food_map)

    def calc_danger_map(self):
        self.danger_map = {
            (i, j): 0 for i in range(self.state.width) for j in range(self.state.height)
        }
        for i in range(self.state.width):
            self.propagate((i, 0), BORDER_DANGER, self.danger_map)
            self.propagate((i, self.state.height), BORDER_DANGER, self.danger_map)
        for j in range(self.state.height):
            self.propagate((0, j), BORDER_DANGER, self.danger_map)
            self.propagate((self.state.width, j), BORDER_DANGER, self.danger_map)

        for body in self.state.body_tiles:
            self.propagate(body, BODY_DANGER, self.danger_map)

        for i, player in self.state.active_players:
            if player.head != self.me.head:
                self.propagate(player.head, HEAD_DANGER, self.danger_map)

        for i in range(self.state.width):
            for j in range(self.state.height):
                if (i, j) in self.state.occupied_tiles:
                    self.danger_map[(i, j)] = INFTY

    def calculate_value(self, coord):
        return self.food_map[coord] - self.danger_map[coord]

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
            # print("for ", option, "value is ", self.calculate_value(option))
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

        # if self.state.time % 20 == 0:
        #     print(self.state.time)
        #     print(self.danger_map)
        #     print("\n\n\n")
        #     print(self.food_map)
        self.context.set_direction(self.choose_direction())

    def setup(self) -> None:
        pass

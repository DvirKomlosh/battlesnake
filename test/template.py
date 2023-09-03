from api import *
import math


def manhattan_distance(coord, coord2):
    return abs(coord[0] - coord2[0]) + abs(coord[1] - coord2[1])


class MyBot(CodeBattlesBot):
    state = None
    players = None
    danger_map = None
    food_map = None

    def get_available_options_with_tailling(self):
        # returns all non killing coordinates for next move
        options = self.get_all_options()
        to_del = []
        tails = []

        for player in self.context.get_active_players():
            if self.context.get_length(player) > 2:
                tails.append(self.context.get_position(player)[0])

        for direction, coord in options.items():
            if (
                coord in self.context.get_occupied_tiles() and coord not in tails
            ) or not self.context.in_bounds(coord):
                to_del.append(direction)
        for direction in to_del:
            del options[direction]

        return options

    def get_best_option(self, destinations):
        options = self.get_available_options_with_tailling()
        if len(options) == 0:
            return "U"
        best_distance = 10000
        best_dir = None
        for dest in destinations:
            for dir, coord in options.items():
                dist = manhattan_distance(dest, coord)
                if manhattan_distance(dest, coord) < best_distance:
                    best_dir = dir
                    best_distance = dist
        return best_dir

    def get_direction(self):
        if (
            self.context.get_health((self.context.get_myself())) > 20
            and self.context.get_length((self.context.get_myself())) % 2 == 0
        ):
            return self.get_best_option(
                [self.context.get_position(self.context.get_myself())[0]]
            )
        else:
            return self.get_best_option(self.context.get_apples())

    def get_all_options(self):
        # returns all coordinates for next move
        x, y = self.context.get_position(self.me)[-1]
        return {"U": (x, y + 1), "D": (x, y - 1), "L": (x - 1, y), "R": (x + 1, y)}

    def run(self) -> None:
        self.me = self.context.get_myself()
        self.context.set_direction(self.get_direction())

    def setup(self) -> None:
        pass

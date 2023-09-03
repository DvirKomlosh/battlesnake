from api import *
import math


def manhattan_distance(coord, coord2):
    return abs(coord[0] - coord2[0]) + abs(coord[1] - coord2[1])


class MyBot(CodeBattlesBot):
    state = None
    players = None
    danger_map = None
    food_map = None

    def get_available_options(self):
        # returns all non killing coordinates for next move
        options = self.get_all_options()
        to_del = []
        for direction, coord in options.items():
            if coord in self.context.get_occupied_tiles() or not self.context.in_bounds(
                coord
            ):
                to_del.append(direction)
        for direction in to_del:
            del options[direction]

        return options

    def get_all_options(self):
        # returns all coordinates for next move
        x, y = self.context.get_position(self.me)[-1]
        return {"U": (x, y + 1), "D": (x, y - 1), "L": (x - 1, y), "R": (x + 1, y)}

    def run(self) -> None:
        self.me = self.context.get_myself()
        move = "U"
        if len(self.get_available_options()) > 0:
            # takes the first available option which will not kill him
            move = list(self.get_available_options().keys())[-1]
        self.context.set_direction(move)

    def setup(self) -> None:
        pass

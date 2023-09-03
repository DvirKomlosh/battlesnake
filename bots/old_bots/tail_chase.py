import math
from api import *


def manhattan_distance(coord, coord2):
    return abs(coord[0] - coord2[0]) + abs(coord[1] - coord2[1])


class MyBot(CodeBattlesBot):
    state = None
    players = None
    looking_for_food = False

    def get_real_occupied_tiles(self):
        real = self.state.occupied_tiles
        for player in self.players:
            if player.has_eaten_last_step <= 0:
                # remove tail if the player has not eaten last turn:
                real.remove(player.position[0])
        return real

    def get_available_options(self):
        # returns all non killing coordinates for next move
        options = self.get_all_options()
        to_del = []
        for direction, coord in options.items():
            if coord in self.get_real_occupied_tiles() or not self.state.in_bounds(
                coord
            ):
                to_del.append(direction)
        for direction in to_del:
            del options[direction]
        if len(options) == 0:
            print("gonna die now")
        return options

    def get_all_options(self):
        # returns all coordinates for next move
        x, y = self.me.head
        return {"U": (x, y + 1), "D": (x, y - 1), "L": (x - 1, y), "R": (x + 1, y)}

    def update_state(self):
        self.state = self.context.get_state()
        self.players = [player for i, player in self.state.active_players]
        self.me = self.context.get_player()

    def choose_direction(self):
        if self.looking_for_food:
            best_option = None
            best_distance = 1000
            for direction, coord in self.get_available_options().items():
                for apple in self.state.apples:
                    if manhattan_distance(coord, apple) < best_distance:
                        best_distance = manhattan_distance(coord, apple)
                        best_option = direction
            return best_option
        else:  # even size, can chase tail:
            best_option = None
            best_distance = 1000
            for direction, coord in self.get_available_options().items():
                if manhattan_distance(coord, self.me.position[0]) < best_distance:
                    best_distance = manhattan_distance(coord, self.me.position[0])
                    best_option = direction
            return best_option

    def run(self) -> None:
        self.update_state()
        state = self.looking_for_food
        self.looking_for_food = (
            self.me.length < 8 or self.me.length % 2 == 1 or self.me.hunger <= 27
        )

        self.context.set_direction(self.choose_direction())

    def setup(self) -> None:
        pass

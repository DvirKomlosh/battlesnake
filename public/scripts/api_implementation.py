"""
The API implementation of the game.
This class should be a complete implementation of the Context
class defined in the api file.
It has access to the game's state, and can change it accordingly.
It also has access to its player's index.
"""
from api import *
from game_state import GameState
from constants import UP, DOWN, LEFT, RIGHT


class GameContext(Context):
    _game: GameState
    _player_index: int

    def __init__(self, game: GameState, player_index: int) -> None:
        self._game = game
        self._player_index = player_index

    ### API IMPLEMENTATION ###

    def debug(message):
        print(str(message))

    def set_direction(self, direction):
        str_to_vec = {
            "L": LEFT,
            "R": RIGHT,
            "U": UP,
            "D": DOWN,
        }
        if direction not in str_to_vec:
            return Exceptions.INVALID_DIRECTION

        self._game.players[self._player_index].next_move = str_to_vec[direction]

    def get_state(self):
        return self._game

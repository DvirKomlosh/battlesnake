"""
The API implementation of the game.
This class should be a complete implementation of the Context
class defined in the api file.
It has access to the game's state, and can change it accordingly.
It also has access to its player's index.
"""

from typing import List, Tuple
from api import API, Exceptions
from code_battles.utilities import console_log
from game_state import GameState, PlayerState
from constants import UP, DOWN, LEFT, RIGHT
import copy


class APIImplementation(API):
    _game: GameState
    _player_index: int
    _copied_state: GameState

    def __init__(self, game: GameState, player_index: int) -> None:
        self._game = game
        self._player_index = player_index
        self._copied_state = copy.deepcopy(self._game)

    def _update(self):
        if self._copied_state.time != self._game.time:
            self._copied_state = copy.deepcopy(self._game)

    ### API IMPLEMENTATION ###

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

    def get_myself(self) -> PlayerState:
        self._update()
        return self._game.players[self._player_index]

    def get_apples(self) -> List[Tuple[int, int]]:
        self._update()
        return self._copied_state.apples

    def get_game_size(self) -> Tuple[int, int]:
        self._update()
        return self._copied_state.width, self._copied_state.height

    def get_occupied_tiles(self) -> List[Tuple[int, int]]:
        "returns all tiles occupied by snakes"
        self._update()
        return self._copied_state.occupied_tiles

    def in_bounds(self, coord: Tuple[int, int]) -> bool:
        self._update()
        return self._copied_state.in_bounds(coord)

    def get_active_players(self) -> List[PlayerState]:
        self._update()
        return [player for index, player in self._copied_state.active_players]

    def get_position(self, player: PlayerState) -> List[Tuple[int, int]]:
        return player.position

    def get_length(self, player: PlayerState) -> int:
        return player.length

    def get_health(self, player: PlayerState) -> int:
        return player.health

    def get_has_eaten_last_step(self, player: PlayerState) -> int:
        return player.has_eaten_last_step

    def log_info(self, text: str):
        console_log(
            self._player_index,
            f"[INFO {str(self._game.time).rjust(8)}s] {text}",
            "#f8f8f2",
        )

    def log_warning(self, text: str):
        console_log(
            self._player_index,
            f"[WARNING {str(self._game.time).rjust(5)}s] {text}",
            "#f1fa8c",
        )

    def log_error(self, text: str):
        console_log(
            self._player_index,
            f"[ERROR {str(self._game.time).rjust(7)}s] {text}",
            "#ff5555",
        )

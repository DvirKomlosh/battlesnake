"""
The API implementation of the game.
This class should be a complete implementation of the Context
class defined in the api file.
It has access to the game's state, and can change it accordingly.
It also has access to its player's index.
"""

from typing import List, Tuple
from api import API, Exceptions
from code_battles.battles import CodeBattles
from game_state import GameState, PlayerState
from constants import UP, DOWN, LEFT, RIGHT


class PlayerRequests:
    next_move: bytes


class APIImplementation(API):
    _battles: CodeBattles
    _player_index: int
    _state: GameState
    _requests: PlayerRequests

    def __init__(
        self,
        player_index: int,
        state: GameState,
        requests: PlayerRequests,
        battles: CodeBattles,
    ) -> None:
        self._player_index = player_index
        self._state = state
        self._requests = requests
        self._battles = battles

    ### API IMPLEMENTATION ###

    def set_direction(self, direction):
        if type(direction) is not str:
            return Exceptions.INVALID_DIRECTION
        if direction not in "LRUD":
            return Exceptions.INVALID_DIRECTION
        self._requests.next_move = direction.encode("ascii")

    def get_myself(self) -> PlayerState:
        return self._state.players[self._player_index]

    def get_apples(self) -> List[Tuple[int, int]]:
        return self._state.apples

    def get_game_size(self) -> Tuple[int, int]:
        return self._state.width, self._state.height

    def get_occupied_tiles(self) -> List[Tuple[int, int]]:
        "returns all tiles occupied by snakes"
        return self._state.occupied_tiles

    def in_bounds(self, coord: Tuple[int, int]) -> bool:
        return self._state.in_bounds(coord)

    def get_active_players(self) -> List[PlayerState]:
        return [player for index, player in self._state.active_players]

    def get_position(self, player: PlayerState) -> List[Tuple[int, int]]:
        return player.position

    def get_length(self, player: PlayerState) -> int:
        return player.length

    def get_health(self, player: PlayerState) -> int:
        return player.health

    def get_has_eaten_last_step(self, player: PlayerState) -> int:
        return player.has_eaten_last_step

    def log_info(self, text: str):
        self._battles.log(
            f"[INFO T{self._battles.step}] {text}",
            self._player_index,
            "#f8f8f2",
        )

    def log_warning(self, text: str):
        self._battles.log(
            f"[WARNING T{self._battles.step}] {text}",
            self._player_index,
            "#f1fa8c",
        )

    def log_error(self, text: str):
        self._battles.log(
            f"[ERROR T{self._battles.step}] {text}",
            self._player_index,
            "#ff5555",
        )

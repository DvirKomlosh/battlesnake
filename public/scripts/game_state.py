"""
The state class of the game.
In this class, there must be all of the information required to render the game
and also to know what will be the next state of the game, when a step is simulated.
For example, there must be some variables which are set from the user APIs,
and variables corresponding to the position of every game object.
"""

from __future__ import annotations

from random import Random
from typing import List, Tuple

from constants import MAX_HEALTH, STEPS_PER_SECOND


class PlayerState:
    position: List[
        Tuple[int, int]
    ]  # position is a list of snake nodes, where the first one is the player's tail, last is head.
    length: int
    health: int
    next_move: Tuple[int, int]  # "U,D,L,R"
    last_move: Tuple[int, int]
    has_eaten_last_step: int

    def __init__(self, position):
        self.position = position
        self.health = MAX_HEALTH
        self.next_move = None
        self.last_move = None
        self.has_eaten_last_step = 2

    @property
    def length(self):
        return len(self.position)

    @property
    def head(self):
        if self.length == 0:
            return None
        return self.position[-1]

    @property
    def body(self):
        return self.position[:-1]

    def eat(self):
        self.health = MAX_HEALTH
        self.has_eaten_last_step += 1


class GameState:
    height: int = 12
    width: int = 12
    players: List[PlayerState] = []
    steps: int = 0
    apples: List[Tuple[int, int]] = []

    results: List[int]
    active_player_indices: List[int]

    def __init__(self, players: int, random: Random):
        self.active_player_indices = [i for i in range(players)]
        player_positions = self.get_random_player_positions(players, random)
        self.players = [PlayerState([pos]) for pos in player_positions]
        self.apples = []
        self.steps = 0
        self.add_apple(random)
        self.add_apple(random)
        self.add_apple(random)

        self.results = []

    def reset(self, players):
        self.__init__(players)

    @property
    def time(self):
        return self.steps / STEPS_PER_SECOND

    @property
    def active_players(self):
        return [(i, self.players[i]) for i in self.active_player_indices]

    @property
    def occupied_tiles(self):
        occupied = []
        for i, player in self.active_players:
            occupied += [tile for tile in player.position]
        return occupied

    @property
    def body_tiles(self):
        bodies = []
        for i, player in self.active_players:
            bodies += player.body
        return bodies

    @property
    def unoccupied_tiles(self):
        unoccupied = []
        occupied = self.occupied_tiles
        for i in range(self.width):
            for j in range(self.height):
                if (i, j) not in occupied and (i, j) not in self.apples:
                    unoccupied.append((i, j))
        return unoccupied

    @property
    def heads(self):
        heads = []
        for i, player in self.active_players:
            heads.append(player.head)
        return heads

    def is_over(self):
        return len(self.active_player_indices) <= 1

    def add_apple(self, random: Random):
        unoccupied = self.unoccupied_tiles
        new_apple_index = random.randint(0, len(unoccupied) - 1)
        new_apple = unoccupied[new_apple_index]
        self.apples.append(new_apple)

    def in_bounds(self, position: Tuple[int, int]):
        if position[0] < 0 or position[0] >= self.width:
            return False
        if position[1] < 0 or position[1] >= self.height:
            return False
        return True

    def get_random_player_positions(self, players: int, random: Random):
        positions = []
        unoccupied = [(i, j) for i in range(self.width) for j in range(self.height)]
        for i in range(players):
            new_position_index = random.randint(0, len(unoccupied) - 1)
            new_position = unoccupied[new_position_index]
            positions.append(new_position)
            unoccupied.remove(new_position)
        return positions

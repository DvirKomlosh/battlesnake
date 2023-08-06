"""
The state class of the game.
In this class, there must be all of the information required to render the game
and also to know what will be the next state of the game, when a step is simulated.
For example, there must be some variables which are set from the user APIs,
and variables corresponding to the position of every game object.
"""


from typing import List, Tuple
from constants import STEPS_PER_SECOND, MAX_HUNGER
from enum import Enum


# class Coordinate:
#     x: int
#     y: int

#     def __init__(self, x, y):
#         self.x = x
#         self.y = y

#     def __add__(self, other):
#         self.x += other.x
#         self.y += other.y

#     def __sub__(self, other):
#         self.x -= other.x
#         self.y -= other.y


class PlayerState:
    position: List[
        Tuple[int, int]
    ]  # position is a list of snake nodes, where the first one is the player's tail, last is head.
    length: int
    hunger: int
    next_move: Tuple[int, int]  # "U,D,L,R"
    last_move: Tuple[int, int]  # "

    def __init__(self, position):
        self.position = position
        self.length = len(position)
        self.hunger = MAX_HUNGER
        self.next_move = None


class GameState:
    height: int
    width: int
    players: List[PlayerState]
    steps: int
    apples: List[Tuple[int, int]]
    active_player_indices: List[int]

    def __init__(self, players: int):
        self.players = [PlayerState([(5 + i, 5 + i)]) for i in range(players)]
        self.steps = 0
        self.height = 10
        self.width = 10
        self.active_player_indices = [i for i in range(len(self.players))]

    @property
    def time(self):
        return self.steps / STEPS_PER_SECOND

    def is_over(self):
        return self.time > 100

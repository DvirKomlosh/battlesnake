"""
The simulation method of the game.
This method should take a state of the game and change it to the next one.
It is not responsible for running the Player APIs, but the Player APIs
are run immediately before it and should keep information in the game state.
"""

import math
import time
import random
from typing import Tuple
from constants import MAX_APPLES
from game_state import GameState, PlayerState
from code_battles.utilities import show_alert

to_eliminate = []


def add_to_result(state: GameState):
    global to_eliminate
    while len(to_eliminate) > 0:
        random_player = to_eliminate[math.floor(random.random() * len(to_eliminate))]
        state.results.append(random_player)
        to_eliminate.remove(random_player)


def eliminate_player(
    state: GameState, player_names, player, player_index, message, verbose, battles
):
    global to_eliminate
    state.active_player_indices.remove(player_index)
    to_eliminate.append(player_index)
    battles.eliminate_player(player_index, message)


def eat_apple(state: GameState, player: PlayerState, position: Tuple[int, int]):
    state.apples.remove(position)
    player.eat()


def simulate_step(
    state: GameState, player_names: list[str], verbose: bool = True, battles=None
) -> None:
    state.steps += 1
    if state.steps == 1:
        return

    # move one step per player:
    for player_index, player in state.active_players:
        if player.next_move is None:
            eliminate_player(
                state,
                player_names,
                player,
                player_index,
                "did not have next move!",
                verbose,
                battles,
            )
            continue

        new_head = tuple(map(lambda i, j: i + j, player.head, player.next_move))

        if not state.in_bounds(new_head):
            eliminate_player(
                state,
                player_names,
                player,
                player_index,
                "exited bounds!",
                verbose,
                battles,
            )

            continue

        player.position.append(new_head)

    for player_index, player in state.active_players:
        if player.has_eaten_last_step > 0:
            player.has_eaten_last_step -= 1
        else:  # remove tail:
            player.position.pop(0)

    eliminate = set()
    for player_index, player in state.active_players:
        # check if head collided
        # if hit a body, eliminate
        if player.head in state.body_tiles:
            eliminate.add((player_index, player))

        # else, if hit another head, test
        for player_index2, player2 in state.active_players:
            if player_index2 != player_index and player2.head == player.head:
                # print("head to head collision")
                if player2.length >= player.length:
                    eliminate.add((player_index, player))

    for player_index, player in eliminate:
        eliminate_player(
            state,
            player_names,
            player,
            player_index,
            "collided with a snake!",
            verbose,
            battles,
        )

    for player_index, player in state.active_players:
        player.health -= 1
        if player.head in state.apples:
            eat_apple(state, player, player.head)
        else:
            if player.health <= 0:
                eliminate_player(
                    state,
                    player_names,
                    player,
                    player_index,
                    "too hungry!",
                    verbose,
                    battles,
                )
        player.last_move = player.next_move
        player.next_move = None

    add_to_result(state)
    if len(state.active_player_indices) == 1:
        state.results.append(state.active_player_indices[0])

    if len(state.active_player_indices) <= 1:
        return (player_names, state.results[::-1], "NYC")

    if len(state.apples) < MAX_APPLES:
        state.add_apple()

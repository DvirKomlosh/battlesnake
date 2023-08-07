"""
The simulation method of the game.
This method should take a state of the game and change it to the next one.
It is not responsible for running the Player APIs, but the Player APIs
are run immediately before it and should keep information in the game state.
"""
from typing import Tuple
from game_state import GameState
from web_utilities import set_results, show_alert


def in_bounds(state, position: Tuple[int, int]):
    if position[0] < 0 or position[0] >= state.width:
        return False
    if position[1] < 0 or position[1] >= state.height:
        return False
    return True


def simulate_step(state: GameState, player_names: list[str]) -> None:
    state.steps += 1

    # move one step per player:
    for player_index, player in state.active_players:
        head = player.position[-1]
        if player.next_move is None:
            print("did not have next move")
            continue

        new_head = tuple(map(lambda i, j: i + j, head, player.next_move))

        if not in_bounds(state, new_head):
            show_alert(
                f"{player_names[player_index]} was eliminated!",
                f"They finished in place after {state.time} seconds.",
                "blue",
                "fa-solid fa-skull",
                0,
                False,
            )
            state.results.append(player)
            state.active_player_indices.remove(player_index)
            state.results.append(player_index)
            if len(state.active_player_indices) == 1:
                state.results.append(state.active_player_indices[0])
                set_results(player_names, state.results[::-1], "map")

            continue

        player.position.append(new_head)
        player.last_move = player.next_move

    # for p in state.players:
    #     if p.next_move + p.position not in d:
    #         d[p.next_move + p.position] = p
    #     else:
    #         # p and d[p.next_move + p.position] fight over p.next_move + p.position
    #         if p.length > ...:
    #             p.length = 0

"""
The simulation method of the game.
This method should take a state of the game and change it to the next one.
It is not responsible for running the Player APIs, but the Player APIs
are run immediately before it and should keep information in the game state.
"""
from game_state import GameState


def simulate_step(state: GameState, player_names: list[str]) -> None:
    state.steps += 1

    # move one step per player:
    for player in state.players:
        head = player.position[-1]
        if player.next_move is None:
            print("did not have next move")
            continue
        new_head = head + player.next_move
        player.position.append(new_head)
        player.last_move = player.next_move

    # for p in state.players:
    #     if p.next_move + p.position not in d:
    #         d[p.next_move + p.position] = p
    #     else:
    #         # p and d[p.next_move + p.position] fight over p.next_move + p.position
    #         if p.length > ...:
    #             p.length = 0

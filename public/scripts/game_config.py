"""
Main game configuration
"""

from api_implementation import GameContext
from game_renderer import render
from game_simulator import simulate_step
from game_state import GameState
from code_battles.utilities import download_images
from constants import SNAKE_COLORS, BODY_PARTS, IMAGES_NAMES


async def initial_setup(player_names: list[str]):
    """
    Performs additional setup for the simulation,
    and returns additional arguments to render the game
    """
    snakes = await download_images(
        [
            (
                color + " " + body_part,
                "/images/snakes/" + color + "_" + body_part + ".png",
            )
            for color in SNAKE_COLORS
            for body_part in BODY_PARTS
        ]
    )
    assets = await download_images(
        [
            (
                name,
                "/images/assets/" + name + ".png",
            )
            for name in IMAGES_NAMES
        ]
    )
    return [snakes, assets]


def create_initial_state(player_count: int, map: str):
    return GameState(player_count)


def create_context(game_state: GameState, player_index: int):
    return GameContext(game_state, player_index)


CONFIGURATION = {
    "render": render,
    "simulate_step": simulate_step,
    "create_initial_state": create_initial_state,
    "initial_setup": initial_setup,
    "create_context": create_context,
    "extra_height": 180,
}

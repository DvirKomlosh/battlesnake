""" """

from typing import Dict, Tuple
from game_state import GameState
from js import Image
from code_battles.utilities import GameCanvas
from constants import SNAKE_COLORS, TILE_SIZE, DIRECTION_TO_ROTATION, TEXT_COLORS

# TODO: make hirerchies
# a render element that has a father, and renders reletive to the father (gets rotation,size etc from him)
# when you call on something to render it calls the render on the father etc
# that way UI elements are much eaasier to implement

# in terms of future rendering all i need to do is:
# 1. dead snake
# 2. UI elements (for each snake, display length and health)
# 3. better assets (snakes should be rendered on top of empty tiles, and i could draw more beutifly, for sure)


def render(
    game_canvas: GameCanvas,
    player_count: int,
    game: GameState,
    player_names: list[str],
    map_image: Image,
    snakes_assets: Dict[str, Image],
    assets: Dict[str, Image],
):
    game_canvas.clear()

    # for player_index in range(player_count):
    #     game_canvas.draw_text(
    #         player_names[player_index], "black", map_image.width / 2, 100, 50
    #     )

    game_canvas.draw_text(
        "Time: " + str(int(game.time)),
        "black",
        0,
        game_canvas.total_width * 4 / 5,
        map_image.height + 100,
        50,
    )
    if player_count <= 6:
        draw_health(game_canvas, player_names, game, map_image)

    for i in range(game.height):
        for j in range(game.width):
            draw_empty(game_canvas, assets, (i, j))

    for coords in game.apples:
        draw_apple(game_canvas, assets, coords)

    for i, player in game.active_players:
        for coords in player.position[:-1]:
            draw_snake_body(game_canvas, snakes_assets, i, coords)
        draw_snake_head(game_canvas, snakes_assets, i, player.head, player.last_move)


def draw_health(game_canvas: GameCanvas, player_names, state: GameState, map_image):
    for i, player in state.active_players:
        game_canvas.draw_text(
            player_names[i][:16]
            + " " * int(1.4 * (15 - len(player_names[i])))
            + "❤"
            + str(state.players[i].health),
            TEXT_COLORS[i % len(SNAKE_COLORS)],
            0,
            250 + 440 * (i // 2),
            map_image.height + 75 * (1 + (i % 2)),
            34,
        )


def coords_to_screencoords(game_canvas, coords):
    x, y = coords
    return (x + 4) * (TILE_SIZE * 1.1), (13 - (y + 1)) * (TILE_SIZE * 1.1)


def draw_empty(game_canvas: GameCanvas, assets, coords):
    x, y = coords_to_screencoords(game_canvas, coords)
    game_canvas.draw_element(
        assets["empty"],
        0,
        x,
        y,
        TILE_SIZE,
    )


def draw_apple(game_canvas: GameCanvas, assets, coords: Tuple[int, int]):
    x, y = coords_to_screencoords(game_canvas, coords)
    game_canvas.draw_element(
        assets["apple"],
        0,
        x,
        y,
        TILE_SIZE,
    )


def draw_snake_body(game_canvas: GameCanvas, snakes_assets, player_number, coords):
    x, y = coords_to_screencoords(game_canvas, coords)
    color = SNAKE_COLORS[player_number % len(SNAKE_COLORS)]
    game_canvas.draw_element(
        snakes_assets[color + " body"],
        0,
        x,
        y,
        TILE_SIZE,
    )


def draw_snake_head(
    game_canvas: GameCanvas, snakes_assets, player_number, coords, last_move
):
    if last_move is None:
        last_move = (0, 1)
    x, y = coords_to_screencoords(game_canvas, coords)
    color = SNAKE_COLORS[player_number % len(SNAKE_COLORS)]
    game_canvas.draw_element(
        snakes_assets[color + " head"],
        0,
        x,
        y,
        TILE_SIZE,
        direction=DIRECTION_TO_ROTATION[last_move],
    )

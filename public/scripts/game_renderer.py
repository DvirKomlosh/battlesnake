"""

"""

from typing import Tuple
from game_state import GameState
from js import Image
from web_utilities import GameCanvas


def render(
    game_canvas: GameCanvas,
    player_count: int,
    game: GameState,
    player_names: list[str],
    map_image: Image,
):
    # game_canvas.clear()

    # for player_index in range(player_count):
    #     game_canvas.draw_text(
    #         player_names[player_index], "black", player_index, map_image.width / 2, 100
    #     )

    # game_canvas.draw_text(
    #     "Time: " + str(int(game.time)),
    #     "black",
    #     0,
    #     game_canvas.total_width / 2,
    #     map_image.height + 160,
    # )
    # game_canvas.clear()
    game_canvas.draw_text("a", "black", 0, 500, 500)
    # for i in range(game.height):
    #     for j in range(game.width):
    #         draw_empty(game_canvas, (i, j))

    # for coords in game.apples:
    #     draw_apple(coords)

    # for i, player in enumerate(game.players):
    #     for coords in player.position[:-1]:
    #         draw_snake_body(game_canvas, i, coords)
    #     draw_snake_head(game_canvas, i, player.position[-1], player.last_move)


def coords_to_screencoords(game_canvas, coords):
    return (50, 50)


def draw_empty():
    pass


def draw_apple(game_canvas: GameCanvas, coords: Tuple[int, int]):
    x, y = coords_to_screencoords(coords)
    game_canvas.draw_text(
        "a",
        "black",
        0,
        x,
        y,
    )


def draw_snake_body(game_canvas: GameCanvas, player_number, coords):
    x, y = coords_to_screencoords(coords)
    game_canvas.draw_text(
        str(player_number),
        "black",
        0,
        x,
        y,
    )


def draw_snake_head(game_canvas: GameCanvas, player_number, coords):
    x, y = coords_to_screencoords(coords)
    game_canvas.draw_text(
        str(player_number) + "h",
        "black",
        0,
        x,
        y,
    )

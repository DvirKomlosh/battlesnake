from code_battles import CodeBattles
from code_battles.utilities import download_images
import api
from api_implementation import GameContext
from game_renderer import render
from game_simulator import simulate_step
from game_state import GameState
from constants import SNAKE_COLORS, BODY_PARTS, IMAGES_NAMES


class BattleSnake(CodeBattles[GameState, GameContext, type(api)]):
    async def setup(self):
        self.snakes = await download_images(
            [
                (
                    color + " " + body_part,
                    "/images/snakes/" + color + "_" + body_part + ".png",
                )
                for color in SNAKE_COLORS
                for body_part in BODY_PARTS
            ]
        )
        self.assets = await download_images(
            [
                (
                    name,
                    "/images/assets/" + name + ".png",
                )
                for name in IMAGES_NAMES
            ]
        )

    def render(self) -> None:
        render(
            self.canvas,
            len(self.player_names),
            self.state,
            self.player_names,
            self.map_image,
            self.snakes,
            self.assets,
        )

    def simulate_step(self) -> None:
        simulate_step(self.state, self.player_names, True, self)

    def create_initial_state(self):
        return GameState(len(self.player_names))

    def get_api(self):
        return api

    def create_game_context(self, player_index: int):
        return GameContext(self.state, player_index)

    def get_extra_height(self):
        return 180

    def get_steps_per_second(self):
        return 20


game = BattleSnake()

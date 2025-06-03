import api
from api_implementation import APIImplementation, PlayerRequests
from code_battles import CodeBattles, run_game
from constants import BODY_PARTS, DECISION_TO_VEC, IMAGES_NAMES, SNAKE_COLORS
from game_renderer import render
from game_simulator import simulate_step
from game_state import GameState


class BattleSnake(CodeBattles[GameState, APIImplementation, type(api), PlayerRequests]):
    async def setup(self):
        self.snakes = await self.download_images(
            [
                (
                    color + " " + body_part,
                    "/images/snakes/" + color + "_" + body_part + ".png",
                )
                for color in SNAKE_COLORS
                for body_part in BODY_PARTS
            ]
        )
        self.assets = await self.download_images(
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

    def make_decisions(self) -> bytes:
        for player_index in self.active_players:
            self.player_requests[player_index].next_move = b"0"  # no move
            self.run_bot_method(player_index, "run")
        decisions = b"".join(
            [
                self.player_requests[player_index].next_move
                for player_index in self.active_players
            ]
        )

        return decisions

    def apply_decisions(self, decisions: bytes) -> None:
        decision_arr = [decision for decision in decisions.decode("ascii")]
        for i, player_index in enumerate(self.active_players):
            self.state.players[player_index].next_move = DECISION_TO_VEC[
                decision_arr[i]
            ]

        max_snake_length = max([len(snake.body) for snake in self.state.players])
        self.max_snake_length = max(
            self.max_snake_length if hasattr(self, "max_snake_length") else 0,
            max_snake_length,
        )

        simulate_step(self.state, self.player_names, True, self)

    def create_initial_state(self):
        return GameState(len(self.player_names), self.random)

    def create_initial_player_requests(self, player_index: int):
        return PlayerRequests()

    def get_api(self):
        return api

    def create_api_implementation(self, player_index: int):
        return APIImplementation(
            player_index, self.state, self.player_requests[player_index], self
        )

    def configure_extra_height(self):
        return 180

    def get_statistics(self):
        return {"Snake Length": self.max_snake_length}


if __name__ == "__main__":
    run_game(BattleSnake())

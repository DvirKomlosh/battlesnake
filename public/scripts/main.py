from code_battles import CodeBattles, run_game
import api
from api_implementation import APIImplementation, PlayerRequests
from game_renderer import render
from game_simulator import simulate_step
from game_state import GameState
from constants import SNAKE_COLORS, BODY_PARTS, IMAGES_NAMES, DECISION_TO_VEC


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
            self.player_requests[player_index].next_move = b"0" # no move
            self.run_bot_method(player_index, "run")
        decisions = b"".join([self.player_requests[player_index].next_move for player_index in self.active_players])
        
        return decisions

        

    def apply_decisions(self, decisions: bytes) -> None:
        
        decision_arr = [decision for decision in decisions.decode("ascii")]
        for i,player_index in enumerate(self.active_players):
            
            self.state.players[player_index].next_move = DECISION_TO_VEC[decision_arr[i]]
        
        simulate_step(self.state, self.player_names, True, self)


    def create_initial_state(self):
        return GameState(len(self.player_names))
    
    def create_initial_player_requests(self, player_index: int):
        return PlayerRequests()

    def get_api(self):
        return api

    def create_api_implementation(self, player_index: int):
        return APIImplementation(player_index, self.state, self.player_requests[player_index])

    def configure_extra_height(self):
        return 180


if __name__ == "__main__":
    run_game(BattleSnake())

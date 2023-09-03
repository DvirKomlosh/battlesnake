from api import *


class MyBot(CodeBattlesBot):
    def run(self) -> None:
        self.context.set_direction("R")

    def setup(self) -> None:
        return

from api import *


class MyBot(CodeBattlesBot):
    def run(self) -> None:
        self.context.set_direction("L")
        time = str(self.context.get_state().time)
        print(
            "position of head0:", str(self.context.get_state().players[0].position[-1])
        )
        print(
            "position of head1:", str(self.context.get_state().players[1].position[-1])
        )

    def setup(self) -> None:
        return

from api import *


class MyBot(CodeBattlesBot):
    def run(self) -> None:
        self.context.set_direction("L")
        print("L")
        time = str(self.context.get_state().time)
        print("time", time)
        # self.context.debug("L")
        # self.context.debug("time is = "+ str(self.context.get_state().time))

    def setup(self) -> None:
        return

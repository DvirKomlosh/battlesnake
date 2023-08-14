"""
Welcome to the API Documentation!

You probably want to get started with `Context` methods, and have a look at `Exceptions`.
"""

from enum import Enum


class Exceptions(Enum):
    """
    An enum representing result of API methods.
    See each method for a list of possible exceptions.
    If a method was successful, it always returns `OK`.
    """

    OK = 0
    INVALID_DIRECTION = 1

    def __bool__(self):
        return self == Exceptions.OK


class Context:
    """
    The main access point for your bot. Access this using `self.context` inside your `run` method.

    Each action method returns `Exceptions`, which is `Exceptions.OK` if it succeeded, or another value explaining why it failed.
    """

    def set_direction(self, direction: str):
        """
        sets the direction of your snake's next move,
        "U" to move Up
        "D" to move Down
        "L" to move Left
        "R" to move Right
        """
        raise NotImplementedError("Not Implemented!")

    def get_state(self):
        """
        returns the state of the game
        """
        raise NotImplementedError("Not Implemented!")

    def get_player(self):
        """
        returns the state of the player
        """
        raise NotImplementedError("Not Implemented!")

    def debug(message):
        """
        prints a debug message
        """
        raise NotImplementedError("Not Implemented!")

    def __init__(self) -> None:
        pass


class CodeBattlesBot:
    """
    Base class for writing your bots.

    **Important:** Your bot must subclass this directly, and be called MyBot!

    **Important:** Your bot must not have a custom __init__ method. Use `setup` for any setup code you may have.

    **Example:**

    ```python
    class MyBot(CodeBattlesBot):
        def setup(self):
            self.message = "Hello!"
        def run(self):
            print(self.context)
    ```
    """

    context: Context

    def __init__(self, context: Context):
        self.context = context
        self.setup()

    def setup(self) -> None:
        """
        This optional method will be called upon construction.

        If you need to define any instance variables like in a constructor, do it here.
        """

    def run(self) -> None:
        """
        This method will be called once every game step.

        Interact with the game using `self.context`.
        """

import math

# """Amount of steps in a single second"""
STEPS_PER_SECOND = 1

UP = (0, 1)
DOWN = (0, -1)
RIGHT = (1, 0)
LEFT = (-1, 0)

IMAGES_NAMES = ["empty", "apple"]
SNAKE_COLORS = ["red", "green", "blue"]
BODY_PARTS = ["body", "head"]

DIRECTION_TO_ROTATION = {
    UP: 0,
    RIGHT: math.pi / 2,
    DOWN: math.pi,
    LEFT: math.pi * 1.5,
}

TILE_SIZE = 70

MAX_HUNGER = 100
MAX_APPLES = 3

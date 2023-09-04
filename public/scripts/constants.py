import math
import random

# """Amount of steps in a single second"""
STEPS_PER_SECOND = 1

UP = (0, 1)
DOWN = (0, -1)
RIGHT = (1, 0)
LEFT = (-1, 0)

IMAGES_NAMES = ["empty", "apple"]
SNAKE_COLORS = ["red", "green", "blue", "purple", "brown", "yellow", "black"]
TEXT_COLORS = ["red", "green", "blue", "purple", "brown", "orange", "black"]
BODY_PARTS = ["body", "head"]

DIRECTION_TO_ROTATION = {
    RIGHT: 0,
    DOWN: math.pi / 2,
    LEFT: math.pi,
    UP: math.pi * 1.5,
}

TILE_SIZE = 68

MAX_HEALTH = 100
MAX_APPLES = 3

from __future__ import annotations

import math

# """Amount of steps in a single second"""
STEPS_PER_SECOND = 1

UP = (0, 1)
DOWN = (0, -1)
RIGHT = (1, 0)
LEFT = (-1, 0)

IMAGES_NAMES = ["empty", "apple"]
SNAKE_COLORS = ["red", "brown", "green", "yellow", "black", "blue", "purple"]
TEXT_COLORS = ["red", "brown", "green", "yellow", "black", "blue", "purple"]
BODY_PARTS = ["body", "head"]

DECISION_TO_VEC = {"U": UP, "D": DOWN, "R": RIGHT, "L": LEFT, "0": None}


DIRECTION_TO_ROTATION = {
    RIGHT: 0,
    DOWN: math.pi / 2,
    LEFT: math.pi,
    UP: math.pi * 1.5,
}

TILE_SIZE = 68

MAX_HEALTH = 100
MAX_APPLES = 3

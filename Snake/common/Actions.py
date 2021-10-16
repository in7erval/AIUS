from enum import Enum


class Actions(Enum):
    MOVE_DOWN = 'MOVE_DOWN'
    MOVE_UP = 'MOVE_UP'
    MOVE_LEFT = 'MOVE_LEFT'
    MOVE_RIGHT = 'MOVE_RIGHT'
    EXIT = 'EXIT'
    RESET = 'RESET'
    UNKNOWN_COMMAND = 'UNKNOWN_COMMAND'

from enum import Enum


class Actions(Enum):
    MOVE_DOWN = 'MOVE_DOWN'  # движение вниз
    MOVE_UP = 'MOVE_UP'  # движение вверх
    MOVE_LEFT = 'MOVE_LEFT'  # движение влево
    MOVE_RIGHT = 'MOVE_RIGHT'  # движение вправо
    EXIT = 'EXIT'  # выход из игры
    RESET = 'RESET'  # сброс игры
    SPEED_UP = 'SPEED_UP'  # увеличение скорости змейки
    SPEED_DOWN = 'SPEED_DOWN'  # уменьшение скорости змейки
    SINGLE_KEY_MODE = 'SINGLE_KEY_MODE'  # включение/отключение режима по нажатию на клавишу
    UNKNOWN_COMMAND = 'UNKNOWN_COMMAND'  # неизвестная команда

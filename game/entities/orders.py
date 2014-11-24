from enum import Enum, unique


@unique
class SnakeCommand(Enum):
    none = None
    forward = 'F'
    right = 'R'
    left = 'L'

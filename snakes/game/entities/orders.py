from enum import Enum, unique


@unique
class Order(Enum):
    none = None
    forward = 'F'
    right = 'R'
    left = 'L'

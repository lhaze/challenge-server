from enum import Enum, unique


@unique
class Order(Enum):
    """
    An enum of possible turns. At the same time, it is definition of possible
    orders that you can give a Snake.
    """
    FORWARD = 'F'
    RIGHT = 'R'
    LEFT = 'L'

    # Enum/IntEnum can have only __dunder__ attributes as the ones not
    # processed by their Enum.__new__
    __OPPOSITE_MAP__ = {
        FORWARD: FORWARD,
        LEFT: RIGHT,
        RIGHT: LEFT
    }

    @property
    def opposite(self):
        """
        What would be the turn if you have to do it in the opposite direction?

        Returns:
            the opposite Order instance.
        """
        return self.__OPPOSITE_MAP__[self]

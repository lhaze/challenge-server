from collections import deque, namedtuple, Sequence
from enum import IntEnum, unique
from itertools import combinations

from .orders import Order


@unique
class Direction(IntEnum):
    """
    Enumeration type describing four directions of the world: north,
    """
    north = '0'
    east = '1'
    south = '2'
    west = '3'

    def turn(self, order):
        """
        This method lets you change the direction regarding the given order.

        NOTE: No order at all (Order.NONE) is interpreted like
              the Order.FORWARD!

        Params:
            order - commands in which direction you should turn.
        Returns:
            a new Direction you are facing after the turn.
        """
        order_to_turn = {
            Order.forward: 0,
            Order.none: 0,  # No order is interpreted like the Order.FORWARD!
            Order.right: 1,
            Order.left: -1
        }
        return Direction((self + order_to_turn[order]) % 4)

    def opposite(self):
        """
        Returns:
            the opposite direction.
        """
        return Direction((self + 2) % 4)


class Tile(namedtuple('Tile', ('x', 'y'))):

    # Assumes that (0, 0) tile is in the south-west corner.
    DIRECTION_2_VECTOR = {
        Direction.north: (0, 1),
        Direction.east: (1, 0),
        Direction.south: (0, -1),
        Direction.west: (-1, 0)
    }

    VECTOR_2_DIRECTION = {
        (0, 1): Direction.north,
        (1, 0): Direction.east,
        (0, -1): Direction.south,
        (-1, 0): Direction.west
    }

    def __add__(self, vector):
        """
        Returns a tile which is positioned to the self by the given vector.

        Params:
            other - a vector (iterable of len == 2)
        Returns:
            a Tile instance.
        Raises:
            ValueError - vector is invalid.
        """
        if not isinstance(vector, Sequence) or len(vector) != 2:
            raise ValueError(
                "Tile supports only positional addition of an 2-tuple")
        x = self[0] + vector[0]
        y = self[1] + vector[1]
        return Tile(x, y)

    def __sub__(self, other):
        """
        Returns vector (2-tuple of positional addition) between this tile and
        the other one. The self is interpreted as the *end* of the vector, while
        the 'other' is its beginning.
        """
        if not isinstance(other, Tile):
            raise ValueError(
                "Tile supports only positional subtraction of an Tile instance")
        return (self.x - other.x, self.y - other.y)

    def get_adjacent(self, direction):
        """
        Returns a Tile which is adjacent regarding the given direction.
        Params:
            direction - a Direction instance.
        Returns:
            the Tile instance.
        Raises:
            ValueError -- direction is invalid.
        """
        vector = self.DIRECTION_2_VECTOR.get(direction)
        if not vector:
            raise ValueError("{} given as a direction is invalid".format(
                direction))
        return self + vector if vector else None

    def get_direction_to(self, other):
        """
        """
        # TODO

    def is_adjacent(self, tile):
        # TODO
        return


class Snake(deque):
    """
    Represents a snake: deque of tiles that he occupies. He constantly moves:
    ceaselessly pushes his head forward and you can only change his heading,
    sending him an order. Normally, he draws his tail while pushing the head
    forward... Unless it's the case that he has eaten a food, then he grows,
    i.e. pushes head forward but the tail stays at the same spot.
    """
    heading = None

    def __init__(self, tiles, heading):
        super(self, Snake).__init__(tiles)
        self._heading = heading

    @property
    def head(self):
        """ The head of the snake (its first tile). Snakes move head-first. """
        return self[0]

    @property
    def tail(self):
        """ The tail of the snake (its last tile)."""
        return self[-1]

    @property
    def heading(self):
        """
        The heading of the snake: Direction in which its head turned after the
        last turn.
        """
        return self._heading

    def move(self, order, food=None):
        self._heading = self._heading.turn(order)  # turn your head
        new_head = self.head.get_adjacent(self._heading)
        self.appendleft(new_head)  # move your head forward
        fed = new_head in foods  # do I reach the food?
        if not fed:  # iff not, I don't grow, so...
            self.pop()  # pull my tail

    def is_valid(self):
        """
        True iff snake is valid, which means:
            * all tiles are adjacent and unique,
            * heading is consistent with the first two tiles.
        """
        return all(
            self.is_non_intersecting,
            self.is_consistent,
            self.has_valid_heading)

    @property
    def is_non_intersecting(self):
        """ True iff none of my tiles overlap """
        return len(self) == len(set(self))

    @property
    def is_consistent(self):
        for tile in self:
            tile

    @property
    def has_valid_heading(self):
        """
        True iff I'm heading in the direction that my first two tiles define.
        """


class Map(object):
    """
    Represents game map: array of tiles with snakes and possible obstacles on
    it. Encapsulates map logic.
    """
    snakes = None
    food = None
    walls = None

    def compute_orders(self, orders):
        """
        Passes Orders on all snakes, even if it leads to an invalid map
        state. This method assumes that you've passed Order for all
        snakes, even if it is Order.none.

        Params:
            orders - orders per snake: a list of Order instances
        """
        snakes = [
            snake.move(order, self.food)
            for snake, order in zip(self.snakes, orders)
        ]
        # remove a food iff needed
        return Map(snakes, objects, food)

    def is_valid(self):
        """
        True iff map is in a valid state, which means that all snakes are valid
        and there's no clash between them, objects and walls.
        """
        snakes_are_valid = all(snake.is_valid() for snake in self.snakes)
        clash = Snake.snake_clash(self.snakes)
        return snakes_are_valid and not clash

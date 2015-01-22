from collections import deque, namedtuple, Sequence
from enum import IntEnum
import itertools

from .orders import Turn


class Direction(IntEnum):
    """
    Enumeration type describing four directions of the world: north, east,
    south and west. Representation is numerical for the sake of
    """
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    # Enum/IntEnum can have only __dunder__ attributes as the ones not
    # processed by their Enum.__new__
    __SYMBOL_2_VALUE_MAP__ = {
        'N': 0,
        'E': 1,
        'S': 2,
        'W': 3,
    }

    __VALUE_2_SYMBOL_MAP__ = {
        0: 'N',
        1: 'E',
        2: 'S',
        3: 'W',
    }

    # FIXME accessing Turn by their values seems a naive way, but it is a
    # workaround around other INSTANCE of Turn type here. Turn instances
    # can't be used as keys, else you're going to encounter a KeyError on
    # Direction.make_turn method. This seems to be a enum34 bug.
    __TURN_2_ADDEND_MAP__ = {
        'F': 0,
        'R': 1,
        'L': -1,
    }

    # Keys are difference between 'other' (minuend; the 'next' direction) and
    # 'me' (subtrahend; the previous direction).
    __DIFFERENCE_2_TURN_MAP__ = {
        -1: 'L',
        0: 'F',
        1: 'R',
        3: 'L',  # -1 mod 4
    }

    @classmethod
    def from_symbol(cls, symbol):
        """
        Returns a Direction instance from its common symbol:
        one of [N, S, W, E]

        It has to be a class factory method (not a __new__), because it is
        the way that Enum works in enum34 (no custom __new__ after Enum
        creation): https://pypi.python.org/pypi/enum34/#finer-points
        """
        try:
            value = cls.__SYMBOL_2_VALUE_MAP__[symbol]
        except KeyError:
            raise ValueError(
                "Invalid Direction symbol '{}'. Accepted values are: {}.".
                format(symbol, ", ".join(cls.__SYMBOL_2_VALUE_MAP__.keys())))
        return cls(value)

    def to_symbol(self):
        """
        Returns a common symbol of the direction: one of [N, S, W, E].
        """
        return self.__VALUE_2_SYMBOL_MAP__[self.value]

    def make_turn(self, turn):
        """
        This method lets you change the direction regarding the given turn.

        NOTE: None is interpreted like the Turn.FORWARD!

        Params:
            order - a Turn instancein which direction you should turn.
        Returns:
            a new Direction you are facing after the turn.
        """
        try:
            addend = self.__TURN_2_ADDEND_MAP__[turn.value]
        except KeyError:
            raise ValueError((
                "Invalid turn choice '{}'. Accepted values are Turn instances "
                "or None.").format(turn))
        return Direction((self + addend) % 4)

    def get_turn_to(self, direction):
        """
        Returns:
            Turn instance representing a turn which you have to take to make
            'self' change into 'direction'.
        Raises:
            ValueError iff it can't be done (ie. turning N into S can't be done
            in a single turn).
        """
        symbol = self.__DIFFERENCE_2_TURN_MAP__.get((direction - self) % 4)
        if symbol is None:
            raise ValueError((
                "Turning from {} to {} can't be done in a single "
                "turn.").format(self.value, direction.value))
        return Turn(symbol)

    @property
    def opposite(self):
        """
        Returns:
            the opposite direction.
        """
        return Direction((self + 2) % 4)


class Tile(namedtuple('Tile', ('x', 'y'))):

    # Assumes that (0, 0) tile is in the south-west corner.
    DIRECTION_2_VECTOR_MAP = {
        Direction.NORTH: (0, 1),
        Direction.EAST: (1, 0),
        Direction.SOUTH: (0, -1),
        Direction.WEST: (-1, 0)
    }

    VECTOR_2_DIRECTION_MAP = {
        (0, 1): Direction.NORTH,
        (1, 0): Direction.EAST,
        (0, -1): Direction.SOUTH,
        (-1, 0): Direction.WEST
    }

    def __new__(cls, x, y):
        """ Casts arguments to int """
        return super(Tile, cls).__new__(cls, int(x), int(y))

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
        try:
            other_x = int(vector[0])
            other_y = int(vector[1])
        except TypeError:
            raise ValueError(
                "Value '{}' seems to be invalid. Can't be cast to int.".
                format(vector))
        x = self[0] + other_x
        y = self[1] + other_y
        return Tile(x, y)

    def __sub__(self, other):
        """
        Returns vector (2-tuple of positional addition) between this tile and
        the other one. The self is interpreted as the *end* of the vector,
        while the 'other' is its beginning.
        """
        if not isinstance(other, Tile):
            raise ValueError(
                "Tile supports only positional subtraction of an Tile "
                "instance")
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
        try:
            vector = self.DIRECTION_2_VECTOR_MAP[direction]
        except KeyError:
            raise ValueError((
                "Invalid direction '{}'. Accepted values are Direction "
                "instances only.").format(
                direction))
        return self + vector

    def get_direction_to(self, other):
        """
        Returns a Direction to an other Tile iff it is adjacent,
        or None otherwise. List of all vectors to adjacent Tiles are defined in
        VECTOR_2_DIRECTION_MAP.

        Params:
            other - a Tile instance, interpreted as the end of the vector.
        Returns:
            a Direction iff adjacent, or None otherwise.
        """
        vector = other - self
        return self.VECTOR_2_DIRECTION_MAP.get(vector)

    def is_adjacent(self, other):
        """ Checks iff this tile is adjacent to the other """
        vector = other - self
        return vector in self.VECTOR_2_DIRECTION_MAP.keys()

    def to_short_repr(self):
        """
        Returns short representation of the tile in the form of:
            <int>,<int>
        """
        return ",".join((str(self[0]), str(self[1])))


def _iterate_pairwise(sequence):
    """ Returns iterable which iterates by pairs """
    a, b = itertools.tee(sequence)
    next(b, None)
    return itertools.izip(a, b)


class Snake(deque):
    """
    Represents a snake: deque of tiles that he occupies. He constantly moves:
    ceaselessly pushes his head forward and you can only change his heading,
    sending him an order. Normally, he draws his tail while pushing the head
    forward... Unless it's the case that he has eaten a food, then he grows,
    i.e. pushes head forward but the tail stays at the same spot.

    Head, i.e. snake[0], is on his left end.
    """

    def __init__(self, tiles):
        if len(tiles) < 2:
            raise ValueError((
                "Snake should have at least 2 tiles. Input sequence {} has "
                "only {} tiles").format(tiles, len(tiles)))
        super(Snake, self).__init__(tiles)
        self.heading = tiles[1].get_direction_to(tiles[0])

    def __str__(self):
        return self.to_tile_form()

    @classmethod
    def from_tile_form(cls, snake_repr):
        """
        Creates instance from stringified sequence of turns.

        BNF of the tiles form:
        <tile> ::= <number> "," <number>
        <tile_sequence> ::= <tile_sequence> ":" <tile> | <tile> ":" <tile>
        <snake_repr> ::= <tile_sequence>
        """
        tiles_repr = snake_repr.split(':')
        tiles = [Tile(*tile_repr.split(',')) for tile_repr in tiles_repr]
        return cls(tiles)

    def to_tile_form(self):
        """
        Returns a stringified Snake in the form of sequence of tiles separated
        with colons. Definition of the form is in the 'form_tile_form' method
        docstring.
        """
        return ":".join(["%s,%s" % (tile.x, tile.y) for tile in self])

    @classmethod
    def from_hhot_form(cls, snake_repr):
        """
        Creates instance from Head-Heading-Opposite-Turns serialization form.
        It is a compromise between human-readability and compactness. In this
        representation, snake is easy to move, rotate or reproduce his history
        of commands.

        NOTE 1: Reversed sequence of opposited turns is just a history of snake
            turns (hence the 'opposite' concept in the name).

        NOTE 2: Definition states there is at least one turn, so the snake
            should have at least 3 tiles (head, heading-determined and
            turn-determined).

        BNF of the HHOT form:
        <tile> ::= <number> "," <number>
        <head> ::= <tile>
        <heading> ::= "N" | "E" | "S" | "W"  # Direction.NORTH/EAST/SOUTH/WEST
        <turn> ::= "F" | "L" | "R"  # Turn.FORWARD/LEFT/RIGHT
        <turn_sequence> ::= <turn> <turn_sequence> | <turn>
        <snake_repr> ::= <head> ":" <heading> <turn_sequence>

        For example:
            1,1:ERLFF
        """
        head_repr, body_repr = snake_repr.split(':')
        # assuming at least one symbol present, which will be the heading
        # while the rest of the body will be interpreted as turns
        assert len(body_repr)
        direction = Direction.from_symbol(body_repr[0]).opposite
        head = Tile(*head_repr.split(','))
        tile = head.get_adjacent(direction)
        snake = deque((head, tile))
        for turn_symbol in body_repr[1:]:
            turn = Turn(turn_symbol)
            direction = direction.make_turn(turn)
            tile = tile.get_adjacent(direction)
            snake.append(tile)
        return cls(snake)

    def to_hhot_form(self):
        """
        Returns a stringified Head-Heading-Opposite-Turns serialization form.

        You can find a definition of it in docstring of from_hhot_form factory
        method.
        """
        # iterate over tiles, evaluate Directions (using pair of adjacent
        # tiles) and turn them to Turns (using pairs of sequential Directions)
        tiles_iterator = iter(self)
        next(tiles_iterator)
        old_tile = next(tiles_iterator)
        old_direction = self.heading.opposite
        turns = []
        for tile in tiles_iterator:
            direction = old_tile.get_direction_to(tile)
            if direction is None:
                raise ValueError((
                    "The snake seems to be in an invalid state. Tile {} is "
                    "not adjacent to the {} tile.").format(old_tile, tile))
            turns.append(old_direction.get_turn_to(direction))
            old_tile, old_direction = tile, direction
        turns_repr = "".join([turn.value for turn in turns])
        return "{head}:{heading}{turns_repr}".format(
            head=self.head.to_short_repr(), heading=self.heading.to_symbol(),
            turns_repr=turns_repr)

    @property
    def head(self):
        """
        The head of the snake (its first tile), leftmost.
        NOTE: Snakes move head-first.
        """
        return self[0]

    @property
    def tail(self):
        """ The tail of the snake (its last tile), rightmost."""
        return self[-1]

    def move(self, order, foods=None):
        self.heading = self.heading.turn(order)  # turn your head
        new_head = self[0].get_adjacent(self.heading)
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
        return all((
            self.is_non_intersecting(),
            self.is_consistent(),
            self.has_valid_heading()))

    def is_non_intersecting(self):
        """ True iff none of my tiles overlap """
        return len(self) == len(set(self))

    def is_consistent(self):
        """ True iff all Snake's tiles are adjacent to their neighbours """
        return all(x.is_adjacent(y) for x, y in _iterate_pairwise(self))

    def has_valid_heading(self):
        """
        True iff Snake is heading in the direction that my first two tiles
        define.
        """
        direction = self[1].get_direction_to(self[0])
        return direction == self.heading

from random import randint

from challenge.snakes.entities import Tile


def generate_food_naive(board):
    """
    Food generation strategy: take just a random tile. It may be naive, but it
    can be interesting if there is no rule forbidding placing food on a tile
    occupied by a snake.

    Params:
        board - a Board instance.

    Returns:
        a Tile instance.
    """
    return _get_random_tile(*board.size)


def generate_food_unoccupied(board):
    """
    Food generation strategy: take a random tile that's not occupied by a snake
    Still too naive: inefficient when more more tiles are occupied than not.

    Params:
        board - a Board instance.

    Returns:
        a Tile instance.
    """
    while True:
        tile = _get_random_tile(*board.size)
        for snake in board.snakes:
            if tile in snake:
                break
        else:
            break
    return tile


def _rand_value(max_value):
    """ Returns random int from the 1..max_value interval """
    return randint(1, max_value)


def _get_random_tile(max_x, max_y):
    """ Returns a random tile based on """
    return Tile(_rand_value(max_x), _rand_value(max_y))

from random import randint

from .entities import Tile


def move_snake(snake, order, food):
    """
    Commonsense strategy of snake movement. Mutates snake, which can be either
    in valid or invalid state after the move.

    Params:
        snake - Snake instance to move
        food - iterable of tiles that represent locations with food
    """
    snake.heading = snake.heading.make_turn(order)  # turn your head
    new_head = snake.head.get_adjacent(snake.heading)
    snake.appendleft(new_head)  # move your head forward
    fed = new_head in food  # do i reach the food?
    if not fed:  # iff not, i don't grow, so...
        snake.pop()  # pull my tail


def simple_border_check(size, snake):
    """
    True iff all tiles of the given snake are inside of board's borders.

    Params:
        size - the size of the board: 2-tuple of positive ints
        snake - given Snake instance
    """
    max_x, max_y = size
    for x, y in snake:
        # iterate over snake's tiles and take their coordinates
        if not (0 <= x <= max_x and 0 <= y <= max_y):
            return False
    return True


def _rand_value(max_value):
    """ Returns random int from the 1..max_value interval """
    return randint(1, max_value)


def _get_random_tile(max_x, max_y):
    """ Returns a random tile based on """
    return Tile(_rand_value(max_x), _rand_value(max_y))


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
    Still too naive: unefficient when more more tiles are occupied than not.

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


def compute_result():
    pass  # TODO implementation

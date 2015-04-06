import pytest
import mock

from snakes import strategies
from snakes.repos import exemplary_board_factory
from snakes.entities import Direction, Order, Snake, Tile


tile_list = [Tile(1, 1), Tile(1, 1), Tile(5, 5), None]
mocked_get_random_tile = mock.MagicMock(
    side_effect=lambda *args: tile_list.pop(0))


def test_generate_food_unoccupied(mocker):
    " Test of getting unoccupied tile using generate_food_unoccupied "
    board = exemplary_board_factory()
    with mocker.patch('snakes.strategies._get_random_tile',
                      mocked_get_random_tile):
        result = strategies.generate_food_unoccupied(board)
    assert result == Tile(5, 5)
    assert mocked_get_random_tile.call_count == 3


class TestMoveSnake(object):
    """ Tests of move_snake strategies """
    @pytest.fixture
    def snake(self):
        " A snake for the tests "
        return Snake.from_hhot_form("5,5:NR")

    @pytest.fixture
    def food(self):
        " Food placed in front of mouth of the snake "
        return [Tile(5, 6)]

    def test_pulling_tail_without_food(self, snake):
        " Test if snake is pulling its tail without food "
        tail_before = snake.tail
        strategies.classic_move(snake, Order.FORWARD, [])
        assert tail_before not in snake

    def test_not_pulling_tail_with_food(self, snake, food):
        " Test if snake is not pulling its tail with food "
        tail_before = snake.tail
        strategies.classic_move(snake, Order.FORWARD, food)
        assert snake.tail == tail_before

    @pytest.mark.parametrize("order, heading", [
        (Order.LEFT, Direction.WEST),
        (Order.FORWARD, Direction.NORTH),
        (Order.RIGHT, Direction.EAST),
    ])
    def test_snake_is_turning(self, snake, order, heading):
        " Test if snake is changing its heading "
        strategies.classic_move(snake, order, [])
        assert snake.heading == heading

    @pytest.mark.parametrize("order", [Order.LEFT, Order.FORWARD, Order.RIGHT])
    def test_snake_holds_length(self, snake, order):
        " Test if snake has holds its length without food "
        len_before = len(snake)
        strategies.classic_move(snake, order, [])
        assert len(snake) == len_before

    @pytest.mark.parametrize("order, heading", [
        (Order.LEFT, Direction.WEST),
        (Order.FORWARD, Direction.NORTH),
        (Order.RIGHT, Direction.EAST),
    ])
    def test_snake_moves_head(self, snake, order, heading):
        " Test if snake moves its head to expected tile "
        head_before = snake.head
        strategies.classic_move(snake, order, [])
        assert snake.head == head_before.get_adjacent(heading)


class TestCheckSnake(object):
    """ Tests of check_snake strategies """

    @pytest.mark.parametrize("snake_repr, result", [
        ('0,0:0,1:1,1:1,0', True),
        ('5,5:4,5:4,4:5,4', True),
        ('6,5:5,5', False),
        ('5,6:5,5', False),
        ('-1,0:0,0', False),
        ('0,-1:0,0', False),
    ])
    def test_simple_border_check(self, snake_repr, result):
        snake = Snake.from_tile_form(snake_repr)
        assert strategies.simple_border_check((5, 5), snake) == result

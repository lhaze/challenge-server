import pytest
import mock

from game import policy
from game.repos import board_factory
from game.entities import Direction, Order, Snake, Tile


tile_list = [Tile(1, 1), Tile(1, 1), Tile(5, 5), None]
mocked_get_random_tile = mock.MagicMock(
    side_effect=lambda *args: tile_list.pop(0))


@mock.patch('game.policy._get_random_tile', mocked_get_random_tile)
def test_generate_food_unoccupied():
    " Test of getting unoccupied tile using generate_food_unoccupied "
    board = board_factory('')  # TODO use actual description
    result = policy.generate_food_unoccupied(board)
    assert result == Tile(5, 5)
    assert mocked_get_random_tile.call_count == 3


class TestMoveSnake(object):
    """ Tests of move_snake strategy """
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
        policy.move_snake(snake, Order.FORWARD, [])
        assert tail_before not in snake

    def test_not_pulling_tail_with_food(self, snake, food):
        " Test if snake is not pulling its tail with food "
        tail_before = snake.tail
        policy.move_snake(snake, Order.FORWARD, food)
        assert snake.tail == tail_before

    @pytest.mark.parametrize("order, heading", [
        (Order.LEFT, Direction.WEST),
        (Order.FORWARD, Direction.NORTH),
        (Order.RIGHT, Direction.EAST),
    ])
    def test_snake_is_turning(self, snake, order, heading):
        " Test if snake is changing its heading "
        policy.move_snake(snake, order, [])
        assert snake.heading == heading

    @pytest.mark.parametrize("order", [Order.LEFT, Order.FORWARD, Order.RIGHT])
    def test_snake_holds_length(self, snake, order):
        " Test if snake has holds its length without food "
        len_before = len(snake)
        policy.move_snake(snake, order, [])
        assert len(snake) == len_before

    @pytest.mark.parametrize("order, heading", [
        (Order.LEFT, Direction.WEST),
        (Order.FORWARD, Direction.NORTH),
        (Order.RIGHT, Direction.EAST),
    ])
    def test_snake_moves_head(self, snake, order, heading):
        " Test if snake moves its head to expected tile "
        head_before = snake.head
        policy.move_snake(snake, order, [])
        assert snake.head == head_before.get_adjacent(heading)

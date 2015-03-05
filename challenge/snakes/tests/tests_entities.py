import pytest

from snakes.entities import Direction, Order, Snake, Tile


class TestDirection(object):
    """ Tests of Direction class """

    @pytest.mark.parametrize("direction, order, result", [
        (Direction.NORTH, Order.FORWARD, Direction.NORTH),
        (Direction.NORTH, Order.LEFT, Direction.WEST),
        (Direction.WEST, Order.RIGHT, Direction.NORTH),
        (Direction.SOUTH, Order.RIGHT, Direction.WEST),
        (Direction.SOUTH, Order.LEFT, Direction.EAST),
    ])
    def test_turning_direction(self, direction, order, result):
        " Test of orders which changes Direction in the right (sic!) way "
        assert direction.make_turn(order) == result

    @pytest.mark.parametrize("direction, result", [
        (Direction.NORTH, Direction.SOUTH),
        (Direction.SOUTH, Direction.NORTH),
        (Direction.EAST, Direction.WEST),
        (Direction.WEST, Direction.EAST),
    ])
    def test_opposite_direction(self, direction, result):
        " Test of opposite direction "
        assert direction.opposite == result

    def test_direction2symbol_bijection(self):
        " Test of __VALUE_2_SYMBOL_MAP__/__SYMBOL_2_VALUE_MAP__ bijection "
        V2S = Direction.__VALUE_2_SYMBOL_MAP__
        S2V = Direction.__SYMBOL_2_VALUE_MAP__
        for d in Direction:
            assert d == S2V[V2S[d.value]]

    @pytest.mark.parametrize("this_direction, other_direction, result", [
        (Direction.NORTH, Direction.WEST, Order.LEFT),
        (Direction.NORTH, Direction.EAST, Order.RIGHT),
        (Direction.NORTH, Direction.NORTH, Order.FORWARD),
        (Direction.WEST, Direction.NORTH, Order.RIGHT),
        (Direction.WEST, Direction.SOUTH, Order.LEFT),
    ])
    def test_get_turn_to(self, this_direction, other_direction, result):
        " Test of Direction.get_turn_to "
        assert this_direction.get_turn_to(other_direction) == result

    def test_turn2addend_bijection(self):
        " Test of __TURN_2_ADDEND_MAP__/__DIFFERENCE_2_TURN_MAP__ bijection "
        T2A = Direction.__TURN_2_ADDEND_MAP__
        D2T = Direction.__DIFFERENCE_2_TURN_MAP__
        for o in Order:
            value = o.value
            assert value == D2T[T2A[value]]


class TestTile(object):
    """ Tests of Tile class and Tile-Direction interations """

    @pytest.mark.parametrize("tile, direction, result", [
        (Tile(1, 1), Direction.NORTH, Tile(1, 2)),
        (Tile(1, 1), Direction.EAST, Tile(2, 1)),
        (Tile(1, 1), Direction.SOUTH, Tile(1, 0)),
        (Tile(1, 1), Direction.WEST, Tile(0, 1)),
    ])
    def test_adjacent_tile(self, tile, direction, result):
        " Test of getting valid adjacent tiles "
        assert tile.get_adjacent(direction) == result

    def test_tile2vector_bijection(self):
        " Test of Tile.VECTOR_2_DIRECTION/DIRECTION_2_VECTOR bijection "
        V2D = Tile.VECTOR_2_DIRECTION_MAP
        D2V = Tile.DIRECTION_2_VECTOR_MAP
        for vector in V2D.keys():
            assert vector == D2V[V2D[vector]]

    @pytest.mark.parametrize("tile, other_tile", [
        (Tile(1, 1), Tile(1, 2)),
        (Tile(1, 1), Tile(2, 1)),
        (Tile(1, 1), Tile(1, 0)),
        (Tile(1, 1), Tile(0, 1)),
    ])
    def test_get_direction_to_bijection(self, tile, other_tile):
        " Test of Tile.get_direction_to "
        assert tile.get_adjacent(tile.get_direction_to(other_tile)) ==  \
            other_tile


class TestSnake(object):
    """
    Tests of Snake class and Snake-Order interactions.
    """
    @pytest.mark.parametrize("snake_repr", [
        "5,5:NRLF",
        "-1,-1:EL",
        "0,0:SRR",
    ])
    def test_hhot2snake(self, snake_repr):
        " Test of transforming HHOT form to Snake instance and back "
        snake = Snake.from_hhot_form(snake_repr)
        assert snake.is_valid()
        assert snake_repr == snake.to_hhot_form()

    @pytest.mark.parametrize("snake_tile_repr", [
        "5,5:5,6:6,6:7,6",
        "1,1:2,1:2,2:1,2"
    ])
    def test_snake2hhot(self, snake_tile_repr):
        " Test of transforming Snake instance to HHOT and back "
        snake = Snake.from_tile_form(snake_tile_repr)
        assert snake.is_valid()
        assert snake == Snake.from_hhot_form(snake.to_hhot_form())

    @pytest.mark.parametrize("snake, result", [
        (Snake.from_hhot_form("1,1:SRRR"), False),
        (Snake.from_hhot_form("1,1:SRR"), True),
        (Snake.from_hhot_form("1,1:S"), True)
    ])
    def test_non_intersecting_snake(self, snake, result):
        " Test of intersecting snake validation "
        assert snake.is_non_intersecting() == result

    @pytest.mark.parametrize("snake, result", [
        (Snake.from_tile_form("1,1:2,2:2,3"), False),
        (Snake.from_tile_form("1,1:1,3:1,4"), False),
        (Snake.from_tile_form("1,1:1,2:2,2:2,1:3,1"), True),
    ])
    def test_is_consistent(self, snake, result):
        " Test of snake consistency validation "
        assert snake.is_consistent() == result

    def test_has_valid_heading(self):
        " Test of heading validation "
        snake = Snake.from_tile_form("1,1:1,2:1,3")
        snake.heading = Direction.NORTH
        assert not snake.has_valid_heading()

import pytest

from .entities import Direction, Snake, Tile, Turn


class TestDirection(object):
    """ Tests of Direction class """

    @pytest.mark.parametrize("direction, turn, result", [
        (Direction.NORTH, Turn.FORWARD, Direction.NORTH),
        (Direction.NORTH, Turn.LEFT, Direction.WEST),
        (Direction.WEST, Turn.RIGHT, Direction.NORTH),
        (Direction.SOUTH, Turn.RIGHT, Direction.WEST),
        (Direction.SOUTH, Turn.LEFT, Direction.EAST),
    ])
    def test_turning_direction(self, direction, turn, result):
        " Test of orders which changes Direction in the right (sic!) way "
        assert direction.make_turn(turn) == result

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

    @pytest.mark.parametrize("this_turn, other_direction, result", [
        (Direction.NORTH, Direction.WEST, Turn.LEFT),
        (Direction.NORTH, Direction.EAST, Turn.RIGHT),
        (Direction.NORTH, Direction.NORTH, Turn.FORWARD),
        (Direction.WEST, Direction.NORTH, Turn.RIGHT),
        (Direction.WEST, Direction.SOUTH, Turn.LEFT),
    ])
    def test_get_turn_to(self, this_turn, other_direction, result):
        " Test of Direction.get_turn_to "
        assert this_turn.get_turn_to(other_direction) == result

    def test_turn2addend_bijection(self):
        " Test of __TURN_2_ADDEND_MAP__/__DIFFERENCE_2_TURN_MAP__ bijection "
        T2A = Direction.__TURN_2_ADDEND_MAP__
        D2T = Direction.__DIFFERENCE_2_TURN_MAP__
        for t in Turn:
            value = t.value
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
        assert snake_repr == Snake.from_hhot_form(snake_repr).to_hhot_form()

    @pytest.mark.parametrize("snake_tile_repr", [
        "5,5:5,6:6,6:7,6",
        "1,1:2,1:2,2:1,2:1,1"
    ])
    def test_snake2hhot(self, snake_tile_repr):
        " Test of transforming Snake instance to HHOT and back "
        snake = Snake.from_tile_form(snake_tile_repr)
        assert snake == Snake.from_hhot_form(snake.to_hhot_form())

    @pytest.mark.parametrize("snake, result", [
        (Snake.from_hhot_form("1,1:SRRR"), False)
    ])
    def test_non_intersecting_snake(self, snake, result):
        " Test of intersecting snake validation "
        assert snake.is_non_intersecting() == result

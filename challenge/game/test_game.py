import pytest

from .entities import Direction, Snake, Tile, Turn


class TestTileDirection(object):
    """
    Tests of features with Tile-Direction interaction.
    """

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
        (Direction.WEST, Direction.EAST)
    ])
    def test_opposite_direction(self, direction, result):
        " Test of opposite direction "
        assert direction.opposite() == result

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


class TestSnake(object):
    """
    Tests assumptions about Snake objects.
    """

    @pytest.mark.xfail
    @pytest.mark.parametrize("snake_repr", [
        "5,5:N:FRLF",
        "-1,-1:E:L",
        "0,0:S:RR"
    ])
    def test_hhot2snake(self, snake_repr):
        " Test of transforming HHOT form to Snake instance and back "
        assert snake_repr == Snake.from_hhot_form(snake_repr).to_hhot_form()

    @pytest.mark.parametrize("snake", [])
    def test_snake2hhot(self, snake):
        " Test of transforming Snake instance to HHOT and back "
        assert snake == Snake.from_hhot_form(snake.to_hhot_form())

    @pytest.mark.parametrize("snake, result", [
        (Snake.from_hhot_form("1,1:S:RRR"), True)
    ])
    def test_intersecting_snake(self, snake, result):
        " Test of intersecting snake validation "
        assert snake.is_non_intersecting == result


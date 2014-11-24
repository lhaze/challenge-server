import pytest

from .entities import Direction, Order, Tile


class TestTileDirection(object):
    """
    Tests of features with Tile-Direction interaction. Some of them may sound
    dumb, but here are the sweet spots where a bug has cost me hours of
    non-obvious debugging.
    """

    @pytest.mark.parametrize("direction, order, result", [
        (Direction.north, Order.forward, Direction.north),
        (Direction.north, Order.left, Direction.west),
        (Direction.west, Order.right, Direction.north),
        (Direction.south, Order.right, Direction.west),
        (Direction.south, Order.left, Direction.east),
    ])
    def test_turning_direction(self, direction, order, result):
        " Test of Orders which changes Direction in the right(sic!) way "
        assert direction.turn(order) == result

    @pytest.mark.parametrize("direction, result", [
        (Direction.north, Direction.south),
        (Direction.south, Direction.north),
        (Direction.east, Direction.west),
        (Direction.west, Direction.east)
    ])
    def test_opposite_direction(self, direction, result):
        " Test of opposite direction "
        assert direction.opposite() == result

    @pytest.mark.parametrize("tile, direction, result", [
        (Tile(1, 1), Direction.north, Tile(1, 2)),
        (Tile(1, 1), Direction.east, Tile(2, 1)),
        (Tile(1, 1), Direction.south, Tile(1, 0)),
        (Tile(1, 1), Direction.west, Tile(0, 1)),
    ])
    def test_adjacent_tile(self, tile, direction, result):
        " Test of getting valid adjacent tiles "
        assert tile.get_adjacent(direction) == result

    def test_tile2vector_bijection(self):
        " Test of Tile.VECTOR_2_DIRECTION/DIRECTION_2_VECTOR bijection "
        V2D = Tile.VECTOR_2_DIRECTION
        D2V = Tile.DIRECTION_2_VECTOR
        for vector in V2D.keys():
            assert vector == D2V[V2D[vector]]

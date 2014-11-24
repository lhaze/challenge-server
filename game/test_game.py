import pytest

from .entities import Direction, SnakeCommand, Tile


class TestTileDirection(object):
    " Tests of features with Tile-Direction interaction "

    @pytest.mark.parametrize("direction, command, result", [
        (Direction.north, SnakeCommand.forward, Direction.north),
        (Direction.north, SnakeCommand.left, Direction.west),
        (Direction.west, SnakeCommand.right, Direction.north),
        (Direction.south, SnakeCommand.right, Direction.west),
        (Direction.south, SnakeCommand.left, Direction.east),
    ])
    def test_turning_direction(self, direction, command, result):
        " Test of SnakeCommands which changes Direction in the right(sic!) way "
        assert direction.turn(command) == result

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


from .map import Direction, Snake, Tile, Map
from .orders import SnakeCommand
from .game import Game, GameHistory

# silence pep8
assert [Direction, Snake, SnakeCommand, Tile, Map]
assert SnakeCommand
assert [Game, GameHistory]
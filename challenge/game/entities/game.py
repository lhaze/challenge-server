from dharma.data import Entity, Policy, instance, integer, string, tupl
from typing import Dict, List, NewType, Tuple

from .board import Board, Order, Result


PlayerHash = NewType('Hash', str)


class Game(Entity):

    id = ('hash',)
    hash = string(doc="a natural PK")
    players = tupl(PlayerHash, doc=(
        "a tuple of player hashes; the position of the hash describes which "
        "Snake the player controls."
    ))
    policy = instance(Policy, doc="a bunch of strategies determinating flow of the game")
    state = instance(GameState, null=True, doc=(
        "current state of the game; null iff it hasn't been started at all"
    ))
    result = instance(Result, null=True, doc="a result of the game iff it has been determined")

    @property
    def turn(self) -> int:
        return self.state.turn if self.state else None

    def compute_orders(self, orders: Dict[PlayerHash, Order]) -> None:
        assert self.state, "Current state of the game hasn't been provided"
        # map orders from players to snakes
        mapped_orders = [orders[player] for player in self.players]  # type: List[Order]
        # compute next state of the game
        self.state = self.state.compute_next(mapped_orders)
        # ... and check iff the result has come
        if self.state.result:
            self.result = self.state.result


class GameState(Entity):
    """
    Describes the state of a given game in a particular turn.

    Immutable.

    Pair of the (game, turn) values present a natural PK of
    the GameState.
    """
    id = ('game', 'turn')
    game = instance(Game, immutable=True, doc="an instance which is owner of this game")
    turn = integer(min_value=0, immutable=True)
    board = instance(Board, immutable=True)

    def compute_next(self, orders: List[Order]) -> 'GameState':
        """
        Computes next state of the game, using given orders.

        Returns:
            a new instance of GameState (not necessary valid) after executing
            the orders.
        """
        return GameState(self.game, self.turn + 1, self.board.compute_orders(orders))

    def get_result(self) -> Result:
        """ My board declares if there is the result of the game """
        return self.board.result

    def is_valid(self) -> bool:
        """ GameState is valid iff board seems not to have conflicts. """
        return self.board.is_valid()
        # TODO checking ie. time exceeded which is not a function of the board

    def is_valid_successor(self, other: 'GameState') -> bool:
        """
        Validates if the 'other' GameState is valid successor for this state.
        """
        # TODO


class GameHistory(object):
    """
    Represents history of the Game. Implemented by a sequence of GameStates. TBDL
    """

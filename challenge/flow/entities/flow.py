from dharma.data import Entity, instance, integer, reference, tuple_, uuid
from dharma.domain.policy import Policy
from typing import Dict, List, Mapping, NewType

from .board import Board, Order, Result
from .resolvers import EventResolver


Id = NewType('Id', str)
PlayerTicket = NewType('PlayerTicket', str)


class Flow(Entity):

    # Game instance id
    id = reference('challenge.game.entities.Game')
    # a tuple of player hashes; the position of the hash describes which
    # player a user is controling
    players = tuple_(PlayerTicket)
    # a bunch of strategies determinating flow of the game
    policy = instance(Policy)
    # current state of the game; null iff it hasn't been started
    state = instance(GameState, null=True)
    event_resolver = EventResolver()
    # a result of the game iff it has been determined
    result = instance(Result, null=True)

    @property
    def turn(self) -> int:
        return self.state.turn if self.state else None

    def compute_orders(self, orders: Dict[PlayerTicket, Order]) -> None:
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

    Pair of the (game, turn) values present a natural PK of
    the GameState.
    """
    id = ('game', 'turn')
    # an instance which is owner of this game
    flow = instance(Flow, immutable=True)
    turn = integer(min_value=0)
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
        # TODO checking conditions which are not a function of the board
        # ie. time has run out

    def is_valid_successor(self, other: 'GameState') -> bool:
        """
        Validates if the 'other' GameState is valid successor for this state.
        """
        # TODO

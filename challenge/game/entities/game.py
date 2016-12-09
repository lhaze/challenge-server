from dharma.data import Entity, instance, integer, tuple_, uuid
from dharma.domain.policy import Policy
from typing import Dict, List, Mapping, NewType

from .board import Board, Order, Result
from .resolvers import EventResolver


Id = NewType('Id', str)
PlayerTicket = NewType('PlayerTicket', str)


class Game(Entity):

    id = uuid(doc="a natural PK")  # type: Id
    players = tuple_(Id, doc=(
        "a tuple of player hashes; the position of the hash describes which "
        "Snake the player controls."
    ))
    result = instance(Result, null=True, doc="a result of the game iff it has been determined")

    @property
    def turn(self) -> int:
        return self.state.turn if self.state else None

    def resolve(self, event):
        state = self.resolver.resolve(self.state, event)
        if state:
            self.state = state
        return state

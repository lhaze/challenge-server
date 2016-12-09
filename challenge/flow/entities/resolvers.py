import abc

from .flow import GameState


class EventResolver(object, metaclass=abc.ABCMeta):

    # TODO does Resolver has an internal state?
    state = GameState()

    # logging history of events and states is orthogonal to the problem
    # of resolving events
    # TODO event gateway with event logging and history of states
    @abc.abstractmethod
    def resolve(self, event):
        pass


class TurnResolver(EventResolver):

    def resolve(self, event):
        pass

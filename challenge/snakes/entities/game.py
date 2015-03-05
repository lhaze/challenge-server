class Game(object):

    def __init__(self, hash, players, policy, state=None):
        """
        Params:
            hash - hash. The natural PK.
            players - tuple of user hashes. The position of the hash describes
                which Snake the player controls.
            policy - a bunch of strategies determinating flow of the game:
                a GamePolicy instance.
            state - current state of the game: a GameState instance.
        """
        self.hash = hash
        self.players = players
        self.policy = policy
        self.state = state

    @property
    def turn(self):
        return self.state.turn if self.state else None

    def compute_orders(self, orders):
        """
        Params:
            orders - a dict of {user_hash: Order instance}
        """
        assert self.state, "Current state of the game hasn't been provided"
        # map orders from players to snakes
        mapped_orders = [orders[player] for player in players]
        # compute next state of the game
        self.previous_state = self.state  # TODO needed?
        self.state = self.state.compute_next(orders)
        # ... and check iff the result has come
        if self.state.result:
            self.result = self.state.result


class GameState(object):
    """
    Describes the state of a given game in a particular turn.

    Immutable.

    Pair of the (game, turn) values present a natural PK of
    the GameState.
    """

    def __init__(self, game, turn, map):
        """
        Params:
            game - a Game instsance which is owner of this GameState.
            turn - turn number.
            map - a Map instance.
        """
        super(GameState, self).__setattr__('game', game)
        super(GameState, self).__setattr__('turn', turn)
        super(GameState, self).__setattr__('map', map)

    def __setattr__(self, *args):
        raise TypeError("You try to change GameState, which is immutable")
    __delattr__ = __setattr__

    def compute_next(self, orders):
        """
        Computes next state of the game, using given orders.

        Params:
            orders - a dict of {player_hash: Order instance}
        Returns:
            a new instance of GameState (not necessary valid) after executing
            the orders.
        """
        # TODO mutable/immutable board?
        return GameState(game, turn+1, self.map.compute_orders(orders))

    def get_result(self, result_policy):
        """ My map declares if there is the result of the game """
        return self.map.result

    def is_valid(self):
        """ GameState is valid iff map seems not to have conflicts. """
        return self.map.is_valid()
        # TODO

    def is_valid_successor(self, other):
        """
        Validates if the 'other' GameState is valid successor for this state.
        """
        # TODO


class GameHistory(object):
    # list of GameStates
    sequence = None

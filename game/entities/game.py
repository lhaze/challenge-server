
class Game(object):
    key = ('game_hash',)
    # a hash that is the PK of the game
    hash = None
    # players - tuple of user hashes. The position of the hash describes which Snake the player controls.
    players = None
    # the game result iff determinated
    result = None

    def __init__(self, hash, players, state=None):
        """
        Params:
            hash - hash PK.
            players - tuple of user hashes. The position of the hash describes
                which Snake the player controls.
            state - present state of the game. GameState instance.
        """
        self.hash = hash
        self.players = players
        self.state = state

    @property
    def turn(self):
        return self.state.turn if self.state else None

    def execute_orders(self, orders):
        """
        Params:
            orders - a dict of {user_hash: SnakeCommand instance}
        """
        # map orders from players to snakes
        mapped_orders = [orders[player] for player in players]
        # compute next state of the game
        previous_state = self.state  # TODO needed?
        self.state = self.state.compute_next(orders)
        # ... and check iff the result has come
        if self.state.result:
            self.result = self.state.result


class GameState(object):
    compound_key = ('game', 'turn')
    turn = None
    map = None
    result = None

    def __init__(self, turn, map):
        # the turn number
        self.turn = turn
        # a Map instsance
        self.map = map

    def compute_next(self, orders):
        """
        Params:
            orders - a dict of {player_hash: SnakeCommand instance}
        Returns:
            a new instance of GameState (not necessary valid) after executing
            the orders.
        """
        return GameState(game, turn+1, self.map.compute_orders(orders))

    def is_valid(self):
        """ GameState is valid iff map seems not to have conflicts. """
        return self.map.is_valid()
        # TODO

    def is_valid_successor(self, other):
        """
        Validates if the 'other' GameState is valid successor for this state.
        """
        # TODO

    @property
    def result(self):
        """ My map declares if there is the result of the game """
        return self.map.result


class GameHistory(object):
    # list of GameStates
    sequence = None
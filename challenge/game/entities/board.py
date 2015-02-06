class Board(object):
    """
    Represents game board: array of tiles with snakes and possible obstacles on
    it.

    Board is intended to be persisted as JSON to be stored in either in KV
    stores or in RDBMs.
    """
    policy = None
    snakes = None
    food = None
    walls = None

    @classmethod
    def from_json(self, json_repr):
        """
        Params:
            json_repr - a string containing JSON serialization of the Board.
        Returns:
            a Board instance from serialized state.
        """
        pass  # TODO immplementation

    def __init__(self, state):
        pass  # TODO implementation

    def compute_orders(self, orders):
        """
        Passes orders (Order instances) on all snakes, even if it leads to
        an invalid map state. This method assumes that you've passed order for
        all snakes, even if it is None.

        Params:
            orders - orders per snake: a list of Order instances
        """
        # TODO doesn't it need to be immutable? together with Snakes?
        snakes = [
            self.policy.move_snake(snake, order, self.food)
            for snake, order in zip(self.snakes, orders)
        ]
        # TODO remove a food iff needed
        # TODO generate new food iff needed
        return self  # TODO fix when (im)mutablity is decided

    def is_valid(self):
        """
        True iff map is in a valid state, which means that all snakes are valid
        and there's no clash between them, objects and walls.
        """
        snakes_are_valid = all(snake.is_valid() for snake in self.snakes)
        clash = Snake.snake_clash(self.snakes)
        return snakes_are_valid and not clash

class Board(object):
    """
    Represents game board: array of tiles with snakes, pieces of food and
    possible obstacles on it.
    """

    def __init__(self, policy, snakes, food):
        self.policy = policy
        self.snakes = snakes
        self.food = food

    @property
    def size(self):
        """ Returns size of the board: a 2-tuple of positive ints """
        return self.policy.size

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
        snakes_coherent_with_board = all(
            self.is_coherent_with_snake(snake) for snake in self.snakes)
        clashes = Snake.snake_clash(self.snakes)
        return snakes_are_valid and snakes_coherent_with_board and not clashes

    def is_coherent_with_snake(self, snake):
        """
        True iff a given snake is coherent with the board. For now, it checks
        wheather snake hasn't moved across board's borders.
        """
        self.policy.check_snake(self.size, snake)

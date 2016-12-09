class Board(object):
    """
    Represents game board: array of tiles with snakes, pieces of food and
    possible obstacles on it.
    """

    def __init__(self, policy, size, snakes, food):
        self.policy = policy
        self.size = size
        self.snakes = snakes
        self.food = food

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
        Checks whether board state is valid: policy.validation.
        """
        return self.policy.validate_board(self)

    def is_coherent_with_snake(self, snake):
        """
        True iff a given snake is coherent with the board. For now, it checks
        wheather snake hasn't moved across board's borders.
        """
        self.policy.check_snake(self, snake)


class Order(object):
    """
    Abstract ancestor of all 'order' classes. TBDL
    """


class Result(object):
    """
    Abstract ancestor of all 'result' classes. TBDL
    """

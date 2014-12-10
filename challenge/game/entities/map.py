class Map(object):
    """
    Represents game map: array of tiles with snakes and possible obstacles on
    it. It encapsulates game logic related to the map.

    Map is intended to be persisted as JSON to be stored in either in KV stores,
    or in RDBMs.
    """
    snakes = None
    food = None
    walls = None

    @classmethod
    def from_json(self, json_repr):
        """
        Params:
            json_repr - a string containing JSON serialization of the Map.
        Returns:
            a Map instance from serialized state.
        """
        pass

    def __init__(self, state, policy):
        self.food_generation_strategy = policy.food_generation

    def compute_orders(self, orders):
        """
        Passes orders (Turn instances) on all snakes, even if it leads to
        an invalid map state. This method assumes that you've passed order for
        all snakes, even if it is None.

        Params:
            orders - orders per snake: a list of Turn instances
        """
        # TODO doesn't it need to be immutable? together with Snakes?
        snakes = [
            snake.move(order, self.food)
            for snake, order in zip(self.snakes, orders)
        ]
        # remove a food iff needed
        return Map(snakes, objects, food)

    def is_valid(self):
        """
        True iff map is in a valid state, which means that all snakes are valid
        and there's no clash between them, objects and walls.
        """
        snakes_are_valid = all(snake.is_valid() for snake in self.snakes)
        clash = Snake.snake_clash(self.snakes)
        return snakes_are_valid and not clash


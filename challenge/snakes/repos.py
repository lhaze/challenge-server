from dharma.data import Policy, PolicySerializer

from . import strategies
from .entities import Board, Snake, Tile


def board_factory(snake_repr, food_repr, policy_desc=None):
    policy_desc = policy_desc or {}
    policy = exemplary_snakes_policy_factory(**policy_desc)
    snakes = [Snake.from_tile_form(snake) for snake in snake_repr]
    food = [Tile(*food_desc) for food_desc in food_repr]
    return Board(policy=policy, snakes=snakes, food=food)


def exemplary_board_factory():
    snakes = [Snake.from_hhot_form(d).to_tile_form()
              for d in ('1,1:SF', '3,3:NR')]
    return board_factory(snake_repr=snakes, food_repr=[(7, 7)])


def exemplary_snakes_policy_factory(**kwargs):
    """
    Params:
        kwargs -- an optional kwargs of {strategy_role: strategy_name} strings
    Returns:
        an instance of SnakesPolicy
    """
    d = {
        'move_snake': strategies.move_snake.classic_move,
        'check_snake': strategies.check_snake.simple_border_check,
        'generate_food': strategies.generate_food.generate_food_unoccupied,
    }
    d.update(kwargs)
    return Policy(**d)


board_policy_serializer = PolicySerializer(
    move_snake=strategies.move_snake,
    check_snake=strategies.check_snake,
    generate_food=strategies.generate_food,
    validate_board=strategies.validate_board,
)

from jsonweb import decode

from game.policy import BasePolicy, policy_constructor
from . import strategies
from .entities import Board


@decode.from_object(policy_constructor)
class SnakesPolicy(BasePolicy):

    STRATEGY_CHOICES = {
        'move_snake': ('classic_move',),
        'check_snake': ('simple_border_check',),
        'generate_food': ('generate_food_naive', 'generate_food_unoccupied', ),
        'compute_result': ('compute_result',),
    }
    STRATEGY_MODULE = strategies

    SERIALIZED_ATTRS = BasePolicy.SERIALIZED_ATTRS + ('board_size',)
    BOARD_CLASS = Board

    def __init__(self, board_size, **kwargs):
        self.board_size = board_size
        super(SnakesPolicy, self).__init__(**kwargs)

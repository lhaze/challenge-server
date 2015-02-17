from bunch import Bunch

from .. import policy


STRATEGY_CHOICES = {
    'move_snake': ('move_snake',),
    'check_snake': ('simple_border_check',),
    'generate_food': ('generate_food_unoccupied', 'generate_food_naive'),
    'compute_result': ('compute_result',),
}


def game_policy_factory(description=None):
    """
    Params:
        description -- a dictionary of {strategy_key: strategy_name} strings
    Returns:
        a Bunch of strategies
    """
    d = {
        'move_snake': policy.move_snake,
        'check_snake': policy.simple_border_check,
        'generate_food': policy.generate_food_unoccupied,
        'compute_result': policy.compute_result,
        'size': (7, 7),
        'turn_length': 1,  # 1s
    }
    if description:
        for key, name in description.items():
            strategy = getattr(policy, name, None)
            if strategy and strategy in STRATEGY_CHOICES['key']:
                d['key'] = strategy
            else:
                raise ValueError((
                    "Invalid strategy name {} given for the key {}. Look into "
                    "STRATEGY_CHOICES dict for proper choices.").format(
                    name, key))
    return Bunch(**d)

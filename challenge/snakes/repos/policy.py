from ..policy import SnakesPolicy


def exemplary_snakes_policy_factory(**kwargs):
    """
    Params:
        kwargs -- an optional kwargs of {strategy_role: strategy_name} strings
    Returns:
        an instance of SnakesPolicy
    """
    d = {
        'move_snake': 'classic_move',
        'check_snake': 'simple_border_check',
        'generate_food': 'generate_food_unoccupied',
        'compute_result': 'compute_result',
        'board_size': [7, 7],
        'turn_length': 1000,  # 1s
    }
    d.update(kwargs)
    return SnakesPolicy(**d)

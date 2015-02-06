from bunch import Bunch

from ..entities import policy


def game_policy_factory(description):
    """
    Returns:
        a Bunch with strategies
    """
    # TODO use actual description
    dict = {
        'move_snake': policy.move_snake,
        'generate_food': policy.generate_food_unoccupied,
        'compute_result': policy.compute_result,
    }
    return Bunch(**dict)

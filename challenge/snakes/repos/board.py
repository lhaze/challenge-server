from bunch import Bunch

from ..entities import Board, Snake, Tile
from .policy import game_policy_factory


def board_factory(policy_desc, snake_repr, food_repr):
    policy = game_policy_factory(policy_desc)
    snakes = [Snake.from_tile_form(snake) for snake in snake_repr]
    food = [Tile(*food_desc) for food_desc in food_repr]
    return Board(policy=policy, snakes=snakes, food=food)


def exemplary_board_factory():
    snakes = [Snake.from_hhot_form(d).to_tile_form()
              for d in ('1,1:SF', '3,3:NR')]
    return board_factory(None, snakes, [(7, 7)])

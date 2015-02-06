from bunch import Bunch

from ..entities import Snake


def board_factory(description):
    # TODO use description to build the board
    snakes = [Snake.from_hhot_form(d) for d in ('1,1:SF', '3,3:NR')]
    return Bunch(max_x=7, max_y=7, snakes=snakes)

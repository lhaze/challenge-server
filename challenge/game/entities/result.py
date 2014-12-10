


class Clash(object):

    @classmethod
    def snake_clash(cls, snakes):
        """ Each pair of snakes from argument don't have common """
        return {
            (snake1, snake2): snake1.union(snake2)
            for snake1, snake2 in combinations(snakes, 2)
        }

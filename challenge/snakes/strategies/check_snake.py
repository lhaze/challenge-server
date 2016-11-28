def simple_border_check(board: 'Board', snake: 'Snake'):
    """
    True iff all tiles of the given snake are inside of board's borders.
    """
    max_x, max_y = board.size
    for x, y in snake:
        # iterate over snake's tiles and take their coordinates
        if not (0 <= x <= max_x and 0 <= y <= max_y):
            return False
    return True

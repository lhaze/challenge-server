def board_validation(board):
    """
    True iff map is in a valid state, which means that all snakes are valid
    and there's no clash between them, objects and walls.
    """
    from challenge.snakes.entities import Snake
    snakes_are_valid = all(snake.is_valid() for snake in board.snakes)
    snakes_coherent_with_board = all(
        board.is_coherent_with_snake(snake) for snake in board.snakes)
    clashes = Snake.snake_clash(board.snakes)
    return snakes_are_valid and snakes_coherent_with_board and not clashes

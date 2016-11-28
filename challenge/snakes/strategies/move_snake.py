def classic_move(snake, order, food):
    """
    Classic strategy of snake movement. Mutates snake, which can be either
    in valid or invalid state after the move.

    Params:
        snake - Snake instance to move
        order - Order instance which is an order given to the snake
        food - iterable of tiles that represent locations with food
    """
    snake.heading = snake.heading.make_turn(order)  # turn your head
    new_head = snake.head.get_adjacent(snake.heading)
    snake.appendleft(new_head)  # move your head forward
    fed = new_head in food  # do i reach the food?
    if not fed:  # iff not, i don't grow, so...
        snake.pop()  # pull my tail

# Package `game`: abstractions of playing a game

## Listening to the game: The flow

### `services.get_game_state`

## Making orders in the game: The flow

### `services.submit_game_event`

The entry point of logic of this package. Takes a DTO and returns a DTO as a response:

```python
input_data = Bunch({
    'game_ticket': 'ticket_uuid',
    # here comes a structure that describes the event
    'order': 'L',
})
response = services.submit_game_event(input_data)
```

Inside, the service can be quite straightforward:

```python
def submit_game_event(input_data):
    try:
        game = game_repo.get_by_ticket(input_data.game_ticket)
    except game_repo.NotFound as e:
        ...
        return build_failure_response(
            code='GAME_NOT_FOUND',
            data=input_data.game_ticket
        )
    try:
        event = game.policy.event_constructor(input_data)
    except Exception as e:
        ...
        return build_failure_response(code='MALFORMED_INPUT', data=input_data)
    try:
        game.resolve(event)
    except Exception as e:
        ...
        return build_failure_response(
            code='INTERNAL_ERROR',
            data=input_data,
            ...
        )
    return build_success_response()
```

As you can see, the service doesn't return any state of the game. There are two reasons for that.
The first one is about principles. As in CQRS, [...].
The second is practical. In several cases of game mechanics, submitting an order for my turn might
doesn't necessarily finish the turn, ie. you have to wait till other players decide.

Logging process at the service layer has a bit different purpose than the one that is done by
the game's event resolver. The event resolver will not see requests that was made for
non-existing game tickets or the ones that was malformed. On the other hand, the service logger
knows nothing about games' logic so the event is uninterpretable for it.

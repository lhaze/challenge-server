from dharma.compat import SqlAlchemyRepo
from dharma.data import EntitySerializer, PolicySerializer

from . import entities, strategies


game_serializer = EntitySerializer(entities.Game)
game_repo = SqlAlchemyRepo(serializer=game_serializer, engine_config={})

game_policy_serializer = PolicySerializer(
    board=strategies.board_constructors,
)

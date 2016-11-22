from dharma.compat import SqlAlchemyRepo
from dharma.data import EntitySerializer

from .entities import Game


game_serializer = EntitySerializer(Game)
game_repo = SqlAlchemyRepo(serializer=game_serializer, engine_config={})

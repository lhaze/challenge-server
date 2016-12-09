from dharma.compat.db import RedisRepo
from dharma.data import EntitySerializer, PolicySerializer

from . import entities, strategies


flow_serializer = EntitySerializer(entities.Flow)
flow_repo = RedisRepo(serializer=flow_serializer, engine_config={})

game_policy_serializer = PolicySerializer(
    board=strategies.board_constructors,
)

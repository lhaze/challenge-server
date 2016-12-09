from dharma.utils.collections import Bunch
from enum import Enum
import logging
from typing import Any

from .repos import flow_repo

logger = logging.getLogger(__file__)


def submit_flow_event(input_data: Bunch) -> Bunch:
    try:
        flow = flow_repo.get_by_ticket(input_data.game_ticket)
    except flow_repo.NotFound as e:
        logger.warning(e, input_data)
        return _build_failure_response(
            code='GAME_NOT_FOUND',
            data=input_data.game_ticket
        )
    try:
        event = flow.policy.event_constructor(input_data)
    except Exception as e:
        logger.warning(e, input_data)
        return _build_failure_response(code='MALFORMED_INPUT', data=input_data)
    try:
        flow.resolve(event)
    except Exception as e:
        logger.error(e, input_data)
        return _build_failure_response(
            code='INTERNAL_ERROR',
            error=ErrorCodes.ERROR_500,
            data=input_data
        )
    return _build_success_response()


def _build_success_response() -> Bunch:
    return Bunch(success=True)


def _build_failure_response(
        code: str,
        error: 'ErrorCodes' = None,
        data: Any = None
) -> Bunch:
    description = RESPONSE_DESCRIPTION_MAP.get(code)
    return Bunch(
        success=False,
        error=error,
        code=code,
        description=description,
        data=data,
    )


RESPONSE_DESCRIPTION_MAP = Bunch(
    GAME_NOT_FOUND="Game ticket was not found",
    MALFORMED_INPUT="",
    INTERNAL_ERROR='',
)


class ErrorCodes(Enum):
    ERROR_500 = 500

"""Event publisher handlers."""

import json
from dataclasses import asdict
from typing import TYPE_CHECKING

import redis
import structlog

from oak_signs.settings import settings

if TYPE_CHECKING:
    from oak_signs.domain.events.event_types import Event

logger = structlog.get_logger(__name__)

client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


def publish_with_redis(event: "Event") -> None:
    """Publish an event to redis.

    Args:
        event (Event): event object with type which is the channel name.
    """
    try:
        client.publish(
            event.event_type.value,
            json.dumps(asdict(event), default=str),
        )
    except redis.exceptions.ConnectionError as exc:
        logger.error("Could not connect to redis", exc=exc)

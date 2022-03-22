"""Event publisher handlers."""

import json
from typing import TYPE_CHECKING

import redis

from oak_signs.settings import settings

if TYPE_CHECKING:
    from oak_signs.domain.events.event_types import Event

client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


def publish_with_redis(event: "Event") -> None:
    """Publish an event to redis.

    Args:
        event (Event): event object with type which is the channel name.
    """
    client.publish(event.event_type.value, json.dumps(event, default=str))

"""Event publisher handlers."""

import json
from typing import TYPE_CHECKING

import redis

from oak_signs.settings import settings

if TYPE_CHECKING:
    from oak_signs.domain.events.event_types import Event
    from oak_signs.events.event_types import EventType

client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


def publish_with_redis(channel: "EventType", payload: "Event") -> None:
    """Publish an event to redis.

    Args:
        channel (EventType): event type, which is the channel name.
        payload (Event): event data.
    """
    client.publish(channel.value, json.dumps(payload, default=str))

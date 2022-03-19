"""Event bus."""

import json
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

from structlog import get_logger

from oak_signs.events.publisher import publish_with_redis

if TYPE_CHECKING:
    from oak_signs.domain.events.event_types import Event
    from oak_signs.events.event_types import EventType

logger = get_logger(__name__)


class EventBus:
    """Dispatcher and publisher for event objects."""

    events: dict[str, type["Event"]] = {}

    @classmethod
    def dispatch(cls, event_type: bytes, event_data: bytes) -> None:
        """Dispatch an event to the appropriate handler.

        Args:
            event_type (bytes): channel name, which is the event type.
            event_data (bytes): event data.
        """
        logger.info(
            "Dispatching event",
            event_type=event_type,
            event_data=event_data,
        )
        event = cls.events.get(event_type.decode())
        if not event:
            logger.warning(
                "No event registered to dispatch",
                event_type=event_type,
                events=cls.events,
            )
            return
        data = json.loads(event_data.decode())
        event(**data).handle()

    @classmethod
    def publish(cls, event_type: "EventType", event_data: "Event") -> None:
        """Publish an event to redis.

        Args:
            event_type (EventType): event type, which is the channel name.
            event_data (Event): event data.
        """
        logger.info(
            "Publishing event",
            event_type=event_type,
            event_data=event_data,
        )
        event = cls.events.get(event_type)
        if not event:
            logger.warning(
                "No event registered to publish",
                event_type=event_type,
                events=cls.events,
            )
            return
        publish_with_redis(event_type, event_data)


def eventclass(event_type: "EventType") -> Callable:
    """Register an event class and return it as a dataclass.

    Connector between the event type and the event class (dataclass).

    Args:
        event_type (EventType): event type - channel name.

    Returns:
        Callable: a decorator.
    """
    logger.info("Registering event class", event_type=event_type)

    def wrapper(cls) -> type:
        """Register the event class and create the dataclass.

        Args:
            cls (type): event class.

        Returns:
            type: the dataclass.
        """
        EventBus.events[event_type.value] = cls
        return dataclass(cls)

    return wrapper

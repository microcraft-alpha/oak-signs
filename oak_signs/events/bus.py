"""Event bus."""

import json
from dataclasses import dataclass, fields
from typing import TYPE_CHECKING, Callable

from structlog import get_logger

from oak_signs.events.publisher import publish_with_redis

if TYPE_CHECKING:
    from oak_signs.domain.events.event_types import Event
    from oak_signs.events.event_types import EventType

logger = get_logger(__name__)


def clean_event_data(event_data: bytes, event: type["Event"]) -> dict:
    """Parse bytes data to json and remove fields not included in the dataclass.

    Args:
        event_data (bytes): event data.
        event (type[Event]): event class.

    Returns:
        dict: cleaned event data.
    """
    # Parse bytes data to json
    data = json.loads(event_data.decode())
    # Clean extra fields - take only those required in dataclass
    event_fields = [field.name for field in fields(event)]
    return {key: value for key, value in data.items() if key in event_fields}


class EventBus:
    """Dispatcher and publisher for event objects."""

    events: dict[str, type["Event"]] = {}

    @classmethod
    async def dispatch(cls, event_type: bytes, event_data: bytes) -> None:
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
        clean_data = clean_event_data(event_data, event)
        await event(**clean_data).handle()

    @classmethod
    async def publish(cls, event: "Event") -> None:
        """Publish an event to redis.

        Args:
            event (Event): event object.
        """
        logger.info(
            "Publishing event",
            event_object=event,
        )
        if not cls.events.get(event.event_type.value):
            logger.warning(
                "No event registered to publish",
                event_object=event,
                events=cls.events,
            )
            return
        await event.handle()
        publish_with_redis(event)


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
        cls.event_type = event_type
        return dataclass(cls)

    return wrapper

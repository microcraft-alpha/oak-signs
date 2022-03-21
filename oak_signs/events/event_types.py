"""Service level event types."""

import enum


class EventType(str, enum.Enum):  # noqa: WPS600
    """Event types enum."""


class IncomingEventType(EventType):
    """Incoming event types."""

    MONSTER_CREATED = "monster-created"


class OutgoingEventType(EventType):
    """Outgoing event types."""

    NOTIFICATION_CREATED = "notification-created"

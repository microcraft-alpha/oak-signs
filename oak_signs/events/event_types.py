"""Service level event types."""

import enum


class EventType(str, enum.Enum):  # noqa: WPS600
    """Event types enum."""


class IncomingEventType(EventType):
    """Incoming event types."""

    MONSTER_CREATED = "monster-created"
    MONSTER_DELETED = "monster-deleted"

    ITEM_CREATED = "item-created"
    ITEM_DELETED = "item-deleted"


class OutgoingEventType(EventType):
    """Outgoing event types."""

    NOTIFICATION_CREATED = "notification-created"

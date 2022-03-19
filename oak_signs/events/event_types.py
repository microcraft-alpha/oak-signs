"""Service level event types."""

import enum


class EventType(str, enum.Enum):  # noqa: WPS600
    """Event types."""

    MONSTER_CREATED = "monster-created"

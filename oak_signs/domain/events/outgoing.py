"""Domain events going to the outside world."""

import datetime
import uuid

from oak_signs.domain.events.event_types import Event
from oak_signs.events.bus import eventclass
from oak_signs.events.event_types import OutgoingEventType


# TODO: Adding common interface for all object makes some sence.
@eventclass(OutgoingEventType.NOTIFICATION_CREATED)
class NotificationCreated(Event):
    """Event handler for monster creation."""

    id: uuid.UUID
    created_at: datetime.datetime
    type: str
    message: str
    resolved: bool
    entities: list[uuid.UUID]

    async def handle(self) -> None:
        """Publish information about a notification being created."""

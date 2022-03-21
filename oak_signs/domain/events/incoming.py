"""Domain events coming from the outside world."""

import uuid

from structlog import get_logger

from oak_signs.api.v1 import fields
from oak_signs.domain.events.event_types import Event
from oak_signs.domain.notifications.registry import notifications_registry
from oak_signs.events.bus import eventclass
from oak_signs.events.event_types import IncomingEventType

logger = get_logger(__name__)


srv = notifications_registry.service


@eventclass(IncomingEventType.MONSTER_CREATED)
class MonsterCreated(Event):
    """Event handler for monster creation."""

    id: uuid.UUID
    name: str

    async def handle(self) -> None:
        """Create a notification about a monster being created."""
        logger.info("Handling monster creation", name=self.name)
        notification = fields.NotificationCreate(
            type="monster-created",
            message=f"Monster `{self.name}` got created",
            entities=[self.id],
        )
        await srv.create(notification)

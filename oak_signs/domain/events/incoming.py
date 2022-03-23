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
        logger.info("Handling monster creation", id=self.id, name=self.name)
        notification = fields.NotificationCreate(
            type="monster-created",
            message=f"Monster `{self.name}` got created",
            entities=[self.id],
        )
        await srv.create(notification)


@eventclass(IncomingEventType.MONSTER_DELETED)
class MonsterDeleted(Event):
    """Event handler for monster deletion."""

    id: uuid.UUID

    async def handle(self) -> None:
        """Create a notification about a monster being deleted."""
        logger.info("Handling monster deletion", id=self.id)
        notification = fields.NotificationCreate(
            type="monster-deleted",
            message="Monster got deleted",
            entities=[self.id],
        )
        await srv.create(notification)


@eventclass(IncomingEventType.ITEM_CREATED)
class ItemCreated(Event):
    """Event handler for item creation."""

    id: uuid.UUID
    name: str

    async def handle(self) -> None:
        """Create a notification about an item being created."""
        logger.info("Handling item creation", id=self.id, name=self.name)
        notification = fields.NotificationCreate(
            type="item-created",
            message=f"Item `{self.name}` got created",
            entities=[self.id],
        )
        await srv.create(notification)


@eventclass(IncomingEventType.ITEM_DELETED)
class ItemDeleted(Event):
    """Event handler for item deletion."""

    id: uuid.UUID

    async def handle(self) -> None:
        """Create a notification about an item being deleted."""
        logger.info("Handling item deletion", id=self.id)
        notification = fields.NotificationCreate(
            type="item-deleted",
            message="Item got deleted",
            entities=[self.id],
        )
        await srv.create(notification)

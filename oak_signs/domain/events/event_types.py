"""Domain level event types."""

import abc

from structlog import get_logger

from oak_signs.events.bus import eventclass
from oak_signs.events.event_types import EventType

logger = get_logger(__name__)


class Event(abc.ABC):
    """Base class for domain events."""

    def __init__(self, *args, **kwargs) -> None:
        """Allow taking parameters."""  # noqa: DAR101

    @abc.abstractmethod
    def handle(self) -> None:
        """Handle the event."""


@eventclass(EventType.MONSTER_CREATED)
class MonsterCreated(Event):
    """Event handler for monster creation."""

    name: str

    def handle(self) -> None:
        """Create a notification about a monster being created."""
        logger.info("Handling monster creation", name=self.name)

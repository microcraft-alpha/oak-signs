"""Domain level event types."""

import abc
import enum


class Event(abc.ABC):
    """Base class for domain events."""

    event_type: enum.Enum

    def __init__(self, *args, **kwargs) -> None:
        """Allow taking parameters."""  # noqa: DAR101

    @abc.abstractmethod
    async def handle(self) -> None:
        """Handle the event."""

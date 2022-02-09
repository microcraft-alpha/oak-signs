"""GraphQL API fields."""

import uuid
from dataclasses import field

import strawberry

from oak_signs.api import interfaces


@strawberry.type
class Notification(interfaces.Inteface):
    """Notification API model."""

    type: str
    message: str
    resolved: bool = False
    entities: list[uuid.UUID] = field(default_factory=list)

"""GraphQL API fields."""

import datetime
import uuid
from dataclasses import field

import strawberry


@strawberry.type
class Notification:
    """Notification API model."""

    id: uuid.UUID
    type: str
    message: str
    created_at: datetime.datetime
    resolved: bool = False
    entities: list[uuid.UUID] = field(default_factory=list)

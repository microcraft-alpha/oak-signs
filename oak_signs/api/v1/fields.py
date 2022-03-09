"""GraphQL API fields."""

import datetime
import uuid
from dataclasses import field

import strawberry

from oak_signs.api import fields


@strawberry.type
class NotificationCreate(fields.Interface):
    """Notification input API model."""

    type: str
    message: str
    resolved: bool = False
    entities: list[uuid.UUID] = field(default_factory=list)


@strawberry.type
class NotificationOut(fields.Interface):
    """Notification output API model."""

    id: uuid.UUID
    created_at: datetime.datetime

    type: str
    message: str
    resolved: bool
    entities: list[uuid.UUID]


@strawberry.type
class NotificationUpdate(fields.Interface):
    """Notification update input API model."""

    type: str | None = None
    message: str | None = None
    resolved: bool | None = None
    entities: list[uuid.UUID] | None = None

"""Database models."""

import datetime
import uuid

from beanie import Document
from pydantic import Field


class Model(Document):
    """Document model abstraction."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)


class Notification(Model):
    """Notification document model."""

    type: str
    message: str
    resolved: bool = False
    entities: list[uuid.UUID] = Field(default_factory=list)

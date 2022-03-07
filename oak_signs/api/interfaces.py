"""API interfaces."""

import datetime
import uuid

import strawberry


@strawberry.interface
class Inteface:
    """Interface abstraction."""

    id: uuid.UUID
    created_at: datetime.datetime

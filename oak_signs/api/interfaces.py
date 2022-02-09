"""API interfaces."""

import datetime
import uuid

import strawberry


@strawberry.interface
class Inteface:
    """Generic interface."""

    id: uuid.UUID
    created_at: datetime.datetime

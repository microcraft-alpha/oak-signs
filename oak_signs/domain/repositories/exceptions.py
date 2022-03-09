"""Domain exceptions."""

import uuid
from dataclasses import dataclass


@dataclass
class DoesNotExistError(Exception):
    """Raised when an object does not exist."""

    id: uuid.UUID


@dataclass
class AlreadyExistsError(Exception):
    """Raised when an object already exists."""

    id: uuid.UUID

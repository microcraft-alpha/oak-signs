"""Domain types."""

import typing as T

from oak_signs.api import interfaces

CreateSchema = T.TypeVar(
    "CreateSchema",
    bound=interfaces.Inteface,
    contravariant=True,
)

UpdateSchema = T.TypeVar(
    "UpdateSchema",
    bound=interfaces.Inteface,
    contravariant=True,
)

OutSchema = T.TypeVar("OutSchema", bound=interfaces.Inteface)

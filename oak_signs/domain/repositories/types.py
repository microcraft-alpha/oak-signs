"""Domain types."""

import typing as T

from oak_signs.api import fields

CreateSchema = T.TypeVar(
    "CreateSchema",
    bound=fields.Interface,
    contravariant=True,
)

UpdateSchema = T.TypeVar(
    "UpdateSchema",
    bound=fields.Interface,
    contravariant=True,
)

OutSchema = T.TypeVar("OutSchema", bound=fields.Interface)

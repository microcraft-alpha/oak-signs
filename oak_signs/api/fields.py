"""API interfaces."""

import typing as T
import uuid

import strawberry
from beanie import Document

InterfaceObj = T.TypeVar("InterfaceObj", bound="Interface")


@strawberry.interface
class Interface:
    """Generic API interface."""

    def __init__(self, **kwargs) -> None:
        """Allow taking parameters.

        Note:
            Mypy seems to be confused about missing init.

        Args:
            kwargs: additional keyword arguments.
        """

    @classmethod
    def from_orm(cls: type[InterfaceObj], entry: Document) -> InterfaceObj:
        """Create a new instance from an ORM entry.

        Args:
            entry (Document): ORM entry.

        Returns:
            InterfaceObj: new instance.
        """
        return cls(**entry.dict())

    def to_dict(self, exclude_unset=False) -> dict:
        """Convert the instance to a dict.

        Args:
            exclude_unset (bool): whether to exclude unset fields.

        Returns:
            dict: dict representation.
        """
        if not exclude_unset:
            return self.__dict__

        return {
            key: value
            for key, value in self.__dict__.items()
            if value is not None
        }

    @strawberry.field
    def _id(self) -> uuid.UUID:
        """Just a simple object identifier, to satisfy the interface API.

        Returns:
            UUID: random UUID.
        """
        return uuid.uuid4()

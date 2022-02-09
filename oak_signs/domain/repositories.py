"""Storage abstractions."""

import typing as T
import uuid

from oak_signs.domain import types


class Repository(
    T.Generic[
        types.CreateSchema,
        types.UpdateSchema,
        types.OutSchema,
    ],
    T.Protocol,
):
    """Storage interface."""

    async def create(self, data_object: types.CreateSchema) -> types.OutSchema:
        """Create a new entry.

        Args:
            data_object (types.CreateSchema): input data object.
        """
        ...  # noqa: WPS428

    async def get_by_id(self, entry_id: uuid.UUID) -> types.OutSchema:
        """Get an entry by its identifier.

        Args:
            entry_id (UUID): entry ID.
        """
        ...  # noqa: WPS428

    async def collect(
        self,
        **filters,
    ) -> list[types.OutSchema]:
        """Collect all entries and allow filtering.

        Args:
            filters (dict): additional filters to apply.
        """
        ...  # noqa: WPS428

    async def delete(self, entry_id: uuid.UUID) -> None:
        """Delete an entry.

        Args:
            entry_id (UUID): entry ID.
        """
        ...  # noqa: WPS428

    async def update(
        self,
        entry_id: uuid.UUID,
        data_object: types.UpdateSchema,
    ) -> types.OutSchema:
        """Update an existing entry.

        Args:
            entry_id (UUID): entry ID.
            data_object (types.UpdateSchema): input data object.
        """
        ...  # noqa: WPS428

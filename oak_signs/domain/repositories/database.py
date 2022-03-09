"""Database storage classes."""

import typing as T
import uuid

from beanie import Document, operators
from structlog import get_logger

from oak_signs.domain.repositories import exceptions, types

logger = get_logger(__name__)

Model = T.TypeVar("Model", bound=Document)


def create_query(body: dict, model: type[Document]) -> dict:
    """Create an orm query from a dict.

    Args:
        body (dict): payload.
        model (type[Document]): orm model.

    Returns:
        dict: orm query.
    """
    return {getattr(model, key): value for key, value in body.items()}


class MongoRepository(
    T.Generic[
        Model,
        types.CreateSchema,
        types.UpdateSchema,
        types.OutSchema,
    ],
):
    """Generic database storage for ORM models."""

    table: type[Model]
    schema: type[types.OutSchema]

    async def create(
        self,
        data_object: types.CreateSchema,
    ) -> types.OutSchema:
        """Create a new entry.

        Args:
            data_object (CreateSchema): input data object.

        Returns:
            OutSchema: output data representation.
        """
        entry = await self.table(**data_object.to_dict()).insert()
        return self.schema.from_orm(entry)

    async def collect(
        self,
        **filters,
    ) -> list[types.OutSchema]:
        """Collect all entries nased on the query.

        Args:
            filters (dict): filters to apply.

        Returns:
            list[OutSchema]: list of output data representations.
        """
        query = create_query(filters, self.table)
        return [
            self.schema.from_orm(entry)
            async for entry in self.table.find(query)
        ]

    async def get_by_id(self, entry_id: uuid.UUID) -> types.OutSchema:
        """Get an entry by its id.

        Args:
            entry_id (UUID): primary key.

        Raises:
            DoesNotExistError: when entry does not exist.

        Returns:
            OutSchema: output data representation.
        """
        entry = await self.table.find_one(self.table.id == entry_id)
        if not entry:
            logger.error("Entry was not found", id=entry_id)
            raise exceptions.DoesNotExistError(id=entry_id)
        return self.schema.from_orm(entry)

    async def delete(self, entry_id: uuid.UUID) -> None:
        """Get an entry by its id and delete it.

        Args:
            entry_id (UUID): primary key.

        Raises:
            DoesNotExistError: when entry does not exist.
        """
        entry = await self.table.find_one(self.table.id == entry_id)
        if not entry:
            logger.error("Entry was not found", id=entry_id)
            raise exceptions.DoesNotExistError(id=entry_id)
        await entry.delete()

    async def update(
        self,
        entry_id: uuid.UUID,
        data_object: types.UpdateSchema,
    ) -> types.OutSchema:
        """Update an existing entry.

        Args:
            entry_id (UUID): primary key.
            data_object (CreateSchema): input data object.

        Raises:
            DoesNotExistError: when entry does not exist.

        Returns:
            OutSchema: output data representation.
        """
        query = create_query(
            data_object.to_dict(exclude_unset=True),
            self.table,
        )
        update_result = await self.table.find_one(
            self.table.id == entry_id,
        ).set(query)
        if getattr(update_result, "matched_count", 0) == 0:
            logger.error("Entry was not found", id=entry_id)
            raise exceptions.DoesNotExistError(id=entry_id)
        return await self.get_by_id(entry_id)

    async def update_many(
        self,
        entries_ids: list[uuid.UUID],
        data_object: types.UpdateSchema,
    ) -> list[types.OutSchema]:
        """Update multiple entries.

        Error is not raised even if all entries do not exist.

        Args:
            entries_ids (list[UUID]): list of primary keys.
            data_object (CreateSchema): input data object.

        Returns:
            list[OutSchema]: list of output data representations.
        """
        query = create_query(
            data_object.to_dict(exclude_unset=True),
            self.table,
        )
        entries = self.table.find(operators.In(self.table.id, entries_ids))
        await entries.update({"$set": query})
        return [
            self.schema.from_orm(entry) for entry in await entries.to_list()
        ]

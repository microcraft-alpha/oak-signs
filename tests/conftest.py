"""Tests fixtures."""

import typing as T

import pytest_asyncio
import strawberry
from motor import motor_asyncio

from oak_signs.api import schema
from oak_signs.database.client import init_database
from oak_signs.main import app  # noqa: F401 # Import the created app anyway


async def clear_database(client: motor_asyncio.AsyncIOMotorClient):
    """Clear the database from all documents.

    Args:
        client (AsyncIOMotorClient): motor client.
    """
    for collection in await client.account.list_collections():
        await client.account[collection["name"]].delete_many({})


@pytest_asyncio.fixture()
async def async_schema() -> T.AsyncGenerator[strawberry.Schema, None]:
    """Prepare the database, yield the schema and clean up afterwards.

    Yields:
        Schema: GraphQL schema.
    """
    db_client = await init_database()
    yield schema.schema
    await clear_database(db_client)

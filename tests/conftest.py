"""Tests fixtures."""

import typing as T

import pytest_asyncio
from motor import motor_asyncio

from oak_signs.database.client import init_database
from oak_signs.main import app  # noqa: F401 # Import the created app anyway


async def clear_database(client: motor_asyncio.AsyncIOMotorClient) -> None:
    """Clear the database from all documents.

    Args:
        client (AsyncIOMotorClient): motor client.
    """
    for collection in await client.account.list_collections():
        await client.account[collection["name"]].delete_many({})


@pytest_asyncio.fixture()
async def with_database() -> T.AsyncGenerator[None, None]:
    """Prepare the database, yield nothing and clean up afterwards.

    Yields:
        None: nothing.
    """
    db_client = await init_database()
    yield
    await clear_database(db_client)

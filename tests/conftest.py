"""Tests fixtures."""

import typing as T

import pytest_asyncio
from httpx import AsyncClient
from motor import motor_asyncio

from oak_signs.database.client import init_database
from oak_signs.main import app as base_app


async def clear_database(client: motor_asyncio.AsyncIOMotorClient):
    """Clear the database from all documents.

    Args:
        client (AsyncIOMotorClient): motor client.
    """
    for collection in await client.account.list_collections():
        await client.account[collection["name"]].delete_many({})


@pytest_asyncio.fixture()
async def async_client() -> T.AsyncGenerator:
    """Create an instance of the HTTP client.

    Yields:
        AsyncClient: HTTP client.
    """
    async with AsyncClient(app=base_app, base_url="http://test") as client:
        db_client = await init_database()
        yield client
        await clear_database(db_client)

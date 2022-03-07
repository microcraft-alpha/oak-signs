"""Database utils."""

from beanie import init_beanie
from motor import motor_asyncio

from oak_signs.database import models
from oak_signs.settings import settings


async def init_database() -> motor_asyncio.AsyncIOMotorClient:
    """Initialize the database.

    Returns:
        AsyncIOMotorClient: database client.
    """
    client = motor_asyncio.AsyncIOMotorClient(settings.DATABASE_URL)
    await init_beanie(
        database=client.account,
        document_models=[models.Notification],
    )
    return client

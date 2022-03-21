"""Event consumer-worker."""

import asyncio

import redis
from structlog import get_logger

from oak_signs.database.client import init_database
from oak_signs.events.bus import EventBus
from oak_signs.events.event_types import IncomingEventType
from oak_signs.settings import settings

logger = get_logger(__name__)


def init_redis() -> redis.client.PubSub:
    """Start a redis client and return a pubsub object.

    Returns:
        PubSub: a publish-subscribe object.
    """
    logger.info("Initializing redis")
    client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    return client.pubsub()


async def listen(pubsub: redis.client.PubSub) -> None:
    """Listen to redis events and dispatch them to the event bus.

    Args:
        pubsub (PubSub): a publish-subscribe object.
    """
    channels = [event_type.value for event_type in IncomingEventType]
    logger.info("Starting to listen", channels=channels)
    pubsub.subscribe(*channels)
    for message in pubsub.listen():
        if message["type"] == "message":
            await EventBus.dispatch(message["channel"], message["data"])
        else:
            logger.warning("Non-message event received", message=message)


async def main() -> None:
    """Initialize the database and start listening to redis events."""
    logger.info("Starting redis listener")
    pubsub = init_redis()
    await init_database()
    await listen(pubsub)


if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().new_event_loop()
    loop.run_until_complete(main())
    loop.close()

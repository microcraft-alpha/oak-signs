from unittest import mock

import pytest
import redis

from oak_signs.events.consumer import main as listen

pytestmark = [pytest.mark.asyncio]


@mock.patch("oak_signs.events.consumer.EventBus.dispatch")
@mock.patch.object(
    redis.client.PubSub,
    "listen",
    return_value=[
        {
            "type": "message",
            "channel": "some-channel",
            "data": bytes(),
        },
    ],
)
async def test_redis_consumer(
    mock_listen: mock.Mock,
    mock_dispatch: mock.Mock,
):
    """Check that the redis consumer listens to redis events
    and dispatches them to the event bus.
    """
    await listen()
    mock_dispatch.assert_called_once_with("some-channel", bytes())


@mock.patch("oak_signs.events.consumer.EventBus.dispatch")
@mock.patch.object(
    redis.client.PubSub,
    "listen",
    return_value=[{"type": "subscribe"}],
)
async def test_redis_consumer_non_message(
    mock_listen: mock.Mock,
    mock_dispatch: mock.Mock,
):
    """Check that the redis consumer ignores non-message events."""
    await listen()
    mock_dispatch.assert_not_called()

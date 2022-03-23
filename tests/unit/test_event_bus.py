import json
from dataclasses import asdict
from unittest import mock

import pytest
import redis

from oak_signs.domain.events.event_types import Event
from oak_signs.events.bus import EventBus, eventclass

pytestmark = [pytest.mark.asyncio]


def test_eventclass_registering_event():
    """Check that the eventclass is registered in the event bus."""
    event_type = "lol-became-a-good-game"
    mocked_enum = mock.MagicMock(value=event_type)

    assert EventBus.events.get(event_type) is None

    @eventclass(mocked_enum)
    class LolBecameAGoodGame(Event):
        ...

    assert EventBus.events.get(event_type) is LolBecameAGoodGame


def test_eventclass_as_a_dataclass():
    """Check that eventclass works as a dataclass."""
    event_type = "wow-is-free-now"
    mocked_enum = mock.MagicMock(value=event_type)

    @eventclass(mocked_enum)
    class WowIsFree(Event):
        date: str

        async def handle(self) -> None:
            ...

    event = WowIsFree(date="2020-01-01")

    assert event.date == "2020-01-01"


@mock.patch.object(redis.Redis, "publish")
async def test_publishing_event(mock_publish: mock.Mock):
    """Check that the event bus publishes events to redis."""
    event_type = "lost-ark-has-no-queues-anymore"
    mocked_enum = mock.MagicMock(value=event_type)

    @eventclass(mocked_enum)
    class LostArkHasNoQueues(Event):
        async def handle(self) -> None:
            ...

    event = LostArkHasNoQueues()
    await EventBus.publish(event)

    mock_publish.assert_called_once_with(
        event_type,
        json.dumps(asdict(event), default=str),
    )


async def test_dispatching_event():
    """Check that the event bus dispatches events to the correct handler."""
    event_type = "fifa-is-f2p"
    mocked_enum = mock.MagicMock(value=event_type)
    mocked_handle = mock.MagicMock()

    @eventclass(mocked_enum)
    class FifaIsF2P(Event):
        points: int

        async def handle(self) -> None:
            mocked_handle(points=self.points)

    await EventBus.dispatch(
        bytes(mocked_enum.value, encoding="utf-8"),
        bytes('{"points": 100}', encoding="utf-8"),
    )

    mocked_handle.assert_called_once_with(points=100)


@mock.patch.object(redis.Redis, "publish")
async def test_publishing_not_registered_event(mock_publish: mock.Mock):
    """Check that the event bus ignores events that are not registered."""
    event_type = "battlefield-has-no-bugs"
    mocked_enum = mock.MagicMock(value=event_type)

    class BfHasNoBugs(Event):
        event_type = mocked_enum

        async def handle(self) -> None:
            ...

    await EventBus.publish(BfHasNoBugs())

    mock_publish.assert_not_called()


async def test_dispatching_not_registered_event():
    """Check that the event bus ignores events that are not registered."""
    event_type = "warzone-gets-small-update"
    mocked_enum = mock.MagicMock(value=event_type)
    mocked_handle = mock.MagicMock()

    class WarzoneGetsSmallUpdate(Event):
        async def handle(self) -> None:
            mocked_handle()

    await EventBus.dispatch(bytes(mocked_enum.value, encoding="utf-8"), bytes())

    mocked_handle.assert_not_called()

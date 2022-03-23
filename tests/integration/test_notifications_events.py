import uuid

import pytest

from oak_signs.domain.events import incoming as events
from oak_signs.domain.notifications import repository, service

pytestmark = [pytest.mark.asyncio, pytest.mark.usefixtures("with_database")]


async def test_monster_created_event():
    """Check that the event handler for monster creation creates a notification."""
    repo = repository.NotificationsOdmRepository()
    srv = service.NotificationService(repository=repo)

    await events.MonsterCreated(id=uuid.uuid4(), name="Zombie").handle()

    notifications = await srv.collect()

    assert len(notifications) == 1
    assert "Zombie" in notifications[0].message


async def test_monster_deleted_event():
    """Check that the event handler for monster deletion creates a notification."""
    repo = repository.NotificationsOdmRepository()
    srv = service.NotificationService(repository=repo)
    pk = uuid.uuid4()

    await events.MonsterDeleted(id=pk).handle()

    notifications = await srv.collect()

    assert len(notifications) == 1
    assert pk in notifications[0].entities


async def test_item_created_event():
    """Check that the event handler for item creation creates a notification."""
    repo = repository.NotificationsOdmRepository()
    srv = service.NotificationService(repository=repo)

    await events.ItemCreated(id=uuid.uuid4(), name="Sword").handle()

    notifications = await srv.collect()

    assert len(notifications) == 1
    assert "Sword" in notifications[0].message


async def test_item_deleted_event():
    """Check that the event handler for item deletion creates a notification."""
    repo = repository.NotificationsOdmRepository()
    srv = service.NotificationService(repository=repo)
    pk = uuid.uuid4()

    await events.ItemDeleted(id=pk).handle()

    notifications = await srv.collect()

    assert len(notifications) == 1
    assert pk in notifications[0].entities

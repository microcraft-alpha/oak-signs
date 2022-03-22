import uuid

import pytest

from oak_signs.domain.events.incoming import MonsterCreated
from oak_signs.domain.notifications import repository, service

pytestmark = [pytest.mark.asyncio, pytest.mark.usefixtures("with_database")]


async def test_monster_created_event():
    """Check that the event handler for monster creation creates a notification."""
    repo = repository.NotificationsOdmRepository()
    srv = service.NotificationService(repository=repo)

    await MonsterCreated(id=uuid.uuid4(), name="Zombie").handle()

    notifications = await srv.collect()

    assert len(notifications) == 1
    assert "Zombie" in notifications[0].message

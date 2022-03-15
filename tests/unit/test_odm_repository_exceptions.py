import uuid

import pytest

from oak_signs.api.v1 import fields
from oak_signs.domain.notifications.repository import NotificationsOdmRepository
from oak_signs.domain.repositories import exceptions

pytestmark = [pytest.mark.asyncio, pytest.mark.usefixtures("with_database")]


async def test_odm_repository_get_not_exist():
    """Check that exception is raised when trying to get a non-existing entry."""
    repo = NotificationsOdmRepository()
    with pytest.raises(exceptions.DoesNotExistError):
        await repo.get_by_id(uuid.uuid4())


async def test_odm_repository_delete_not_exist():
    """Check that exception is raised when trying to delete a non-existing entry."""
    repo = NotificationsOdmRepository()
    with pytest.raises(exceptions.DoesNotExistError):
        await repo.delete(uuid.uuid4())


async def test_odm_repository_update_not_exist():
    """Check that exception is raised when trying to update a non-existing entry."""
    repo = NotificationsOdmRepository()
    with pytest.raises(exceptions.DoesNotExistError):
        await repo.update(uuid.uuid4(), fields.NotificationUpdate(message=""))

import pytest

from oak_signs.api.v1 import fields
from oak_signs.domain.notifications import repository, service

pytestmark = [pytest.mark.asyncio, pytest.mark.usefixtures("with_database")]


async def create_notifications(
    srv: service.NotificationService,
    n: int,
) -> list[fields.NotificationOut]:
    """Create 'n' notifications and return the created entries.

    Args:
        srv (NotificationService): service to use.
        n (int): number of notifications to create.

    Returns:
        list[NotificationOut]: created notifications.
    """
    return [
        await srv.create(
            fields.NotificationCreate(type=f"Type {i}", message=f"Mess {i}")
        )
        for i in range(n)
    ]


async def test_create_notifications_service_with_mongo_repo():
    """Check creation of notifications with the mongo repository."""
    repo = repository.NotificationsOdmRepository()
    srv = service.NotificationService(repository=repo)

    # Make sure the storage is empty
    entries = await srv.collect()
    assert len(entries) == 0

    entry = await srv.create(
        fields.NotificationCreate(
            type="Conor",
            message="McGregor",
        )
    )
    assert entry.id is not None

    # Check that there is one notification
    entries = await srv.collect()
    assert len(entries) == 1


async def test_retrieve_notification_service_with_mongo_repo():
    """Check retrieval of a single notification with the mongo repository."""
    repo = repository.NotificationsOdmRepository()
    srv = service.NotificationService(repository=repo)

    created_entry = await srv.create(
        fields.NotificationCreate(
            type="Khabib",
            message="Nurmagomedov",
        )
    )

    entry = await srv.get_by_id(created_entry.id)
    assert entry.id == created_entry.id
    assert entry.message == created_entry.message


async def test_collect_notifications_service_with_mongo_repo():
    """Check retrieval of all notifications with the mongo repository."""
    repo = repository.NotificationsOdmRepository()
    srv = service.NotificationService(repository=repo)

    # Make sure the storage is empty
    entries = await srv.collect()
    assert len(entries) == 0

    await create_notifications(srv, 3)

    # Check that there are three notifications
    entries = await srv.collect()
    assert len(entries) == 3


async def test_delete_notification_service_with_mongo_repo():
    """Check deletion of a single notification with the mongo repository."""
    repo = repository.NotificationsOdmRepository()
    srv = service.NotificationService(repository=repo)

    created_entry = await srv.create(
        fields.NotificationCreate(
            type="Khabib",
            message="Nurmagomedov",
        )
    )

    # Check that there is one notification
    entries = await srv.collect()
    assert len(entries) == 1

    await srv.delete(created_entry.id)

    # Check that the notification is not there anymore
    entries = await srv.collect()
    assert len(entries) == 0


async def test_update_notification_service_with_mongo_repo():
    """Check update of a single notification with the mongo repository."""
    repo = repository.NotificationsOdmRepository()
    srv = service.NotificationService(repository=repo)

    created_entry = await srv.create(
        fields.NotificationCreate(
            type="Tupac",
            message="Biggie",
        )
    )

    # Check if the response is correct
    updated_entry = await srv.update(
        created_entry.id,
        fields.NotificationUpdate(
            message="Shakur",
        ),
    )
    assert updated_entry.message == "Shakur"

    # Check if the entry is updated in the database
    entry = await srv.get_by_id(created_entry.id)
    assert entry.message == "Shakur"


async def test_update_many_notifications_service_with_mongo_repo():
    """Check update of many notifications with the mongo repository."""
    repo = repository.NotificationsOdmRepository()
    srv = service.NotificationService(repository=repo)

    created_entries = await create_notifications(srv, 3)

    # Check if the notifications are updated in the response
    entries = await srv.update_many(
        [entry.id for entry in created_entries],
        fields.NotificationUpdate(resolved=True),
    )
    for entry in entries:
        assert entry.resolved is True

    # Check if the entries are updated in the database
    entries = await srv.collect()
    assert len(entries) == 3
    for entry in entries:
        assert entry.resolved is True

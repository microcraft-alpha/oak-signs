"""E2E tests for the notifications API."""

import pytest
import strawberry

from oak_signs.api.v1 import fields
from oak_signs.domain.notifications.registry import registry

pytestmark = pytest.mark.asyncio


async def create_x_notifications(n: int) -> list[str]:
    """Create 'n' number of notifications.

    Args:
        n (int): number of notifications to create.

    Returns:
        list[str]: list of notification ids (as strings).
    """
    return [
        str(
            (
                await registry.odm_service.create(
                    fields.NotificationCreate(
                        type=f"Type {i}",
                        message=f"Mess {i}",
                        resolved=False,
                    )
                )
            ).id
        )
        for i in range(n)
    ]


async def test_get_notifications(async_schema: strawberry.Schema):
    """Check that the notifications are returned in the response."""
    # Create 3 notifications.
    await create_x_notifications(3)

    query = """
        query Query {
            notifications {
                id
            }
        }
    """

    response = await async_schema.execute(query)

    assert response.errors is None
    assert response.data is not None
    assert len(response.data["notifications"]) == 3


async def test_mark_notifications_as_resolved(async_schema: strawberry.Schema):
    """Check that the notifications are marked as resolved."""
    # Create 3 notifications.
    ids = await create_x_notifications(3)

    mutation = """
        mutation Mutation($ids: [UUID!]!) {
            markNotificationsAsResolved(ids: $ids) {
                resolved
            }
        }
    """

    response = await async_schema.execute(
        mutation, variable_values={"ids": ids}
    )

    # Check that the notifications are marked as resolved in the response.
    assert response.errors is None
    assert response.data is not None
    for notification in response.data["markNotificationsAsResolved"]:
        assert notification["resolved"] is True

    # Check that the notifications are marked as resolved in the database.
    notifications = await registry.odm_service.collect()
    for notification in notifications:
        assert notification.resolved is True

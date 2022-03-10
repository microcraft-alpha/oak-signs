"""GraphQL resolver functions."""

import uuid

from oak_signs.api.v1 import fields
from oak_signs.domain.notifications.registry import registry

srv = registry.odm_service


async def get_notifications() -> list[fields.NotificationOut]:
    """Fetch all the notifications.

    Returns:
        list[Notification]: retrieved notifications.
    """
    return await srv.collect()


async def mark_notifications_as_resolved(
    ids: list[uuid.UUID],
) -> list[fields.NotificationOut]:
    """Fetch notifications by the IDs and mark them as resolved.

    Args:
        ids (list[uuid.UUID]): list of notification IDs.

    Returns:
        list[Notification]: updated notifications.
    """
    return await srv.update_many(
        ids,
        fields.NotificationUpdate(resolved=True),
    )

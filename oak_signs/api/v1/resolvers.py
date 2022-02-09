"""GraphQL resolver functions."""

import uuid

from oak_signs.api.v1 import fields


def get_notifications() -> list[fields.Notification]:
    """Fetch all the notifications.

    Returns:
        list[Notification]: retrieved notifications.
    """
    return []


def mark_notifications_as_resolved(
    ids: list[uuid.UUID],
) -> list[fields.Notification]:
    """Fetch notifications by the IDs and mark them as resolved.

    Args:
        ids (list[uuid.UUID]): list of notification IDs.

    Returns:
        list[Notification]: updated notifications.
    """
    return []

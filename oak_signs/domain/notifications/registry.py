"""Set of pre-instantiated dependencies for the notifications domain."""

from oak_signs.domain.notifications.repository import NotificationsRepository
from oak_signs.domain.notifications.service import NotificationService


class NotificationsRegistry:
    """Registry of dependencies for the notifications domain."""

    odm_service = NotificationService(repository=NotificationsRepository())


registry = NotificationsRegistry()

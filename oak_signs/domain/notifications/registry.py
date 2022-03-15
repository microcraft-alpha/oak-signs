"""Set of pre-instantiated dependencies for the notifications domain."""

from oak_signs.domain.notifications.repository import NotificationsOdmRepository
from oak_signs.domain.notifications.service import NotificationService


class NotificationsRegistry:
    """Registry of dependencies for the notifications domain."""

    service = NotificationService(repository=NotificationsOdmRepository())


notifications_registry = NotificationsRegistry()

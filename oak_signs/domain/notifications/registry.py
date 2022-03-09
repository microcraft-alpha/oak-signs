"""Set of pre-instantiated dependencies for the notifications domain."""

from oak_signs.domain.notifications.repository import NotificationsRepository


class NotificationsRegistry:
    """Registry of dependencies for the notifications domain."""

    repository = (
        NotificationsRepository()
    )  # todo: replace this with a service asap


registry = NotificationsRegistry()

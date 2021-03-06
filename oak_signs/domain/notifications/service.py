"""Model logic for the notifications domain."""

import uuid

from structlog import get_logger

from oak_signs.api.v1 import fields
from oak_signs.domain.events.outgoing import NotificationCreated
from oak_signs.domain.repositories import generic
from oak_signs.events.bus import EventBus

logger = get_logger(__name__)


class NotificationService:
    """Orchestrator for the notifications domain.

    Contains the business logic around the notifications model operations.
    """

    def __init__(self, repository: generic.Repository) -> None:
        self.repository = repository

    async def create(
        self,
        data_object: fields.NotificationCreate,
    ) -> fields.NotificationOut:
        """Create a new notification.

        Args:
            data_object (NotificationCreate): input data.

        Returns:
            NotificationOut: representation of the created notification.
        """
        logger.info("Creating notification", data=data_object)
        notification = await self.repository.create(data_object)
        await EventBus.publish(NotificationCreated(**notification.to_dict()))
        logger.info("Created notification", entry=notification)
        return notification

    async def get_by_id(self, pk: uuid.UUID) -> fields.NotificationOut:
        """Get a notification by its ID.

        Args:
            pk (UUID): notification ID.

        Returns:
            NotificationOut: representation of the notification.
        """
        logger.info("Getting notification", id=pk)
        notification = await self.repository.get_by_id(pk)
        logger.info("Got notification by ID", entry=notification)
        return notification

    async def collect(self) -> list[fields.NotificationOut]:
        """Collect all notifications.

        Returns:
            list[NotificationOut]: list of notifications.
        """
        logger.info("Collecting notifications")
        notifications = await self.repository.collect()
        logger.info("Collected notifications", qty=len(notifications))
        return notifications

    async def delete(self, pk: uuid.UUID) -> None:
        """Delete a notification.

        Args:
            pk (UUID): notification ID.
        """
        logger.info("Deleting notification", id=pk)
        await self.repository.delete(pk)
        logger.info("Deleted notification", id=pk)

    async def update(
        self,
        pk: uuid.UUID,
        data_object: fields.NotificationUpdate,
    ) -> fields.NotificationOut:
        """Update a notification.

        Args:
            pk (UUID): notification ID.
            data_object (NotificationUpdate): input data.

        Returns:
            NotificationOut: updated notification.
        """
        logger.info("Updating notification", id=pk, data=data_object)
        notification = await self.repository.update(pk, data_object)
        logger.info("Updated notification", entry=notification)
        return notification

    async def update_many(
        self,
        ids: list[uuid.UUID],
        data_object: fields.NotificationUpdate,
    ) -> list[fields.NotificationOut]:
        """Update many notifications.

        Args:
            ids (list[UUID]): list of notification IDs.
            data_object (NotificationUpdate): input data.

        Returns:
            list[NotificationOut]: list of updated notifications.
        """
        logger.info("Updating notifications", ids=ids, data=data_object)
        notifications = await self.repository.update_many(ids, data_object)
        logger.info("Updated notifications", qty=len(notifications))
        return notifications

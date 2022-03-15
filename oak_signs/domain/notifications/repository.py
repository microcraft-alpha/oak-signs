"""Repositories for the notifications domain."""

from oak_signs.api.v1 import fields
from oak_signs.database import models
from oak_signs.domain.repositories import database


class NotificationsOdmRepository(
    database.MongoRepository[
        models.Notification,
        fields.NotificationCreate,
        fields.NotificationUpdate,
        fields.NotificationOut,
    ],
):
    """Notifications ODM repository."""

    table = models.Notification
    schema = fields.NotificationOut

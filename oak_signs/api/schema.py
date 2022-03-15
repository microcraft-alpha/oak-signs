"""GraphQL schema and its dependencies."""

import strawberry

from oak_signs.api.v1 import fields, resolvers


@strawberry.type
class Query:
    """GraphQL query."""

    notifications: list[fields.NotificationOut] = strawberry.field(
        resolver=resolvers.get_notifications,
    )


@strawberry.type
class Mutation:
    """GraphQL mutation."""

    mark_notifications_as_resolved: fields.NotificationOut = (
        strawberry.mutation(
            resolver=resolvers.mark_notifications_as_resolved,
        )
    )


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)

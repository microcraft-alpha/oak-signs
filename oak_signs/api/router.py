"""GraphQL routing."""

from strawberry.fastapi import GraphQLRouter

from oak_signs.api.schema import schema

graphql_router = GraphQLRouter(schema)

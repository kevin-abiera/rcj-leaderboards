import graphene
from graphene import relay

from ..leagues.schema import Query as LeaguesQuery
from ..teams.schema import Query as TeamsQuery


class Query(LeaguesQuery, TeamsQuery):
    node = relay.NodeField()


schema = graphene.Schema(
    name='GraphQL Schema',
    query=Query,
)

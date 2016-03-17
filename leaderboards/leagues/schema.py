from graphene import relay, ObjectType, resolve_only_args
from graphene.contrib.django.types import DjangoNode
from graphene.contrib.django.fields import DjangoConnectionField

from .models import FleaLeague, RedditLeague, RedditLeagueDivision


class RedditLeagueNode(DjangoNode):
    class Meta:
        model = RedditLeague


class RedditLeagueDivisionNode(DjangoNode):
    class Meta:
        model = RedditLeagueDivision


class FleaLeagueNode(DjangoNode):
    class Meta:
        model = FleaLeague


class Query(ObjectType):
    class Meta:
        abstract = True

    flea_league = relay.NodeField(FleaLeagueNode)
    all_flea_leagues = DjangoConnectionField(FleaLeagueNode)
    reddit_league = relay.NodeField(RedditLeagueNode)
    all_reddit_leagues = DjangoConnectionField(RedditLeagueNode)
    reddit_league_division = relay.NodeField(RedditLeagueDivisionNode)
    all_reddit_league_divisions = DjangoConnectionField(RedditLeagueDivisionNode)

    @resolve_only_args
    def resolve_all_flea_leagues(self):
        return FleaLeague.objects.all()

    @resolve_only_args
    def resolve_all_reddit_leagues(self):
        return RedditLeague.objects.all()

    @resolve_only_args
    def resolve_all_reddit_league_divisions(self):
        return RedditLeagueDivision.objects.all()

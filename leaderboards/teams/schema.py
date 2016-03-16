from graphene import relay, ObjectType, resolve_only_args
from graphene.contrib.django.types import DjangoNode
from graphene.contrib.django.fields import DjangoConnectionField

import graphene

from .models import FleaTeam, FleaOwner


class FleaTeamNode(DjangoNode):
    class Meta:
        model = FleaTeam

    stat_flea_league_overall_pts = graphene.Int()
    stat_flea_league_overall_rank = graphene.Int()
    stat_flea_league_rank_fgpct100 = graphene.Int()
    stat_flea_league_rank_ftpct100 = graphene.Int()
    stat_flea_league_rank_3pt = graphene.Int()
    stat_flea_league_rank_reb = graphene.Int()
    stat_flea_league_rank_stl = graphene.Int()
    stat_flea_league_rank_blk = graphene.Int()
    stat_flea_league_rank_ast = graphene.Int()
    stat_flea_league_rank_to = graphene.Int()
    stat_flea_league_rank_pts = graphene.Int()
    stat_division_overall_pts = graphene.Int()
    stat_division_overall_rank = graphene.Int()
    stat_division_rank_fgpct100 = graphene.Int()
    stat_division_rank_ftpct100 = graphene.Int()
    stat_division_rank_3pt = graphene.Int()
    stat_division_rank_reb = graphene.Int()
    stat_division_rank_stl = graphene.Int()
    stat_division_rank_blk = graphene.Int()
    stat_division_rank_ast = graphene.Int()
    stat_division_rank_to = graphene.Int()
    stat_division_rank_pts = graphene.Int()


class FleaOwnerNode(DjangoNode):
    class Meta:
        model = FleaOwner

    @resolve_only_args
    def resolve_fleateam(self):
        return self.fleateam_set.all()


class Query(ObjectType):
    class Meta:
        abstract = True

    flea_team = relay.NodeField(FleaTeamNode)
    all_flea_teams = DjangoConnectionField(FleaTeamNode)
    flea_owner = relay.NodeField(FleaOwnerNode)
    all_flea_owners = relay.ConnectionField(FleaOwnerNode)

    @resolve_only_args
    def resolve_all_flea_teams(self):
        return FleaTeam.objects.select_related('league', 'owner')

    @resolve_only_args
    def resolve_all_flea_owners(self):
        return FleaOwner.objects.all()

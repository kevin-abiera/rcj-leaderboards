from graphene import relay, ObjectType, resolve_only_args
from graphene.contrib.django.types import DjangoNode
from graphene.contrib.django.fields import DjangoConnectionField

from .models import FleaTeam, FleaOwner


class FleaTeamNode(DjangoNode):
    class Meta:
        model = FleaTeam


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
        return FleaTeam.objects.all()

    @resolve_only_args
    def resolve_all_flea_owners(self):
        return FleaOwner.objects.all()

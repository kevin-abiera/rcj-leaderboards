from django.db import models

from ..core.models import UUIDModel
from ..core.utils import get_team_from_division_list, get_team_from_league_list


class FleaOwner(UUIDModel):
    name = models.CharField(max_length=128)
    url = models.URLField(unique=True)
    reddit_username = models.CharField(blank=True, null=True, max_length=128)
    active = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or '--Unowned--'


class FleaTeam(UUIDModel):
    name = models.CharField(max_length=128)
    url = models.URLField(unique=True)
    owner = models.ForeignKey('FleaOwner', null=True)
    league = models.ForeignKey('leagues.FleaLeague', related_name='teams')
    stat_fgpct100 = models.PositiveIntegerField(default=0)
    stat_ftpct100 = models.PositiveIntegerField(default=0)
    stat_3pt = models.PositiveIntegerField(default=0)
    stat_reb = models.PositiveIntegerField(default=0)
    stat_stl = models.PositiveIntegerField(default=0)
    stat_blk = models.PositiveIntegerField(default=0)
    stat_ast = models.PositiveIntegerField(default=0)
    stat_to = models.PositiveIntegerField(default=0)
    stat_pts = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    team_by_division = None
    team_by_league = None

    def __str__(self):
        return self.name

    def get_division_stat(self, stat):
        self.team_by_division = self.team_by_division or get_team_from_division_list(self.league.division.id, self.id)
        return getattr(self.team_by_division, stat)

    def get_league_stat(self, stat):
        self.team_by_league = self.team_by_league or get_team_from_league_list(self.league.id, self.id)
        return getattr(self.team_by_league, stat)

    def __getattr__(self, item):
        if type(item) is str:
            valid = ['overall_pts', 'overall_rank', 'rank_fgpct100', 'rank_ftpct100', 'rank_3pt', 'rank_reb',
                     'rank_stl', 'rank_blk', 'rank_ast', 'rank_to', 'rank_pts']
            if item.startswith('stat_division_'):
                stat = item.replace('stat_division_', '')
                assert stat in valid, 'Invalid stat'
                return self.get_division_stat(stat)
            elif item.startswith('stat_flea_league_'):
                stat = item.replace('stat_flea_league_', '')
                assert stat in valid, 'Invalid stat'
                return self.get_league_stat(stat)
        return super(FleaTeam, self).__getattr__(item)

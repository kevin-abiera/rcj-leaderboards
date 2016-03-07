from django.db import models

from lxml import html
import requests

from ..core.models import UUIDModel
from ..teams.models import FleaOwner


class RedditLeague(UUIDModel):
    name = models.CharField(max_length=128)
    url = models.URLField(unique=True)
    last_updated = models.DateTimeField(auto_now=True)


class RedditLeagueDivision(UUIDModel):
    name = models.CharField(max_length=128)
    url = models.URLField(blank=True, null=True)
    league = models.ForeignKey('RedditLeague', related_name='divisions')
    last_updated = models.DateTimeField(auto_now=True)


class FleaLeague(UUIDModel):
    name = models.CharField(max_length=128)
    url = models.URLField(unique=True, null=False, blank=False)
    division = models.ForeignKey('RedditLeagueDivision', related_name='leagues')
    last_updated = models.DateTimeField(auto_now=True)

    def fetch_league(self):
        flea = requests.get(self.url)
        assert flea.ok
        tree = html.fromstring(flea.content)  # MOVE THIS for memoization to work

        self.name = tree.xpath('//*[@id="top-bar"]/ul/li[2]/text()')[0]

        # Fetch teams
        teams = tree.xpath('//*[@id="table_0"]/tr')
        for team in teams:
            team_name = team.xpath('td/div[contains(@class, "league-name")]/a/text()')[0]
            team_url = team.xpath('td/div[contains(@class, "league-name")]/a/@href')[0]
            if team.xpath('td/a/text()') == ['Take Over']:
                # Team is not owned
                team_owner_name = ''
                team_owner_url = team.xpath('td/a/@href')
                team_owner_active = False
            else:
                team_owner_name = team.xpath('td/span/a[contains(@class, "user-name")]/text()')[0]
                team_owner_url = team.xpath('td/span/a[contains(@class, "user-name")]/@href')[0]
                team_owner_active = team.xpath(
                    'td/span/a[contains(@class, "user-name")]/@class'
                )[0].find('inactive') == -1

            (team_owner, _) = FleaOwner.objects.update_or_create(  # update because active could change
                url=team_owner_url,
                defaults={
                    'name': team_owner_name,
                    'active': team_owner_active,
                },
            )

            stat_vars = [  # Should be ordered accordingly
                'stat_fgpct100', 'stat_ftpct100', 'stat_3pt', 'stat_reb',
                'stat_stl', 'stat_blk', 'stat_ast', 'stat_to', 'stat_pts',
            ]

            stat_from_ff = team.xpath('td[contains(@class, "right")]/span/text()')

            # Transform (Remove commas and decimals (only for percentages))
            for idx, val in enumerate(stat_from_ff):
                val = val.replace(',', '')
                if stat_vars[idx] in ['stat_fgpct100', 'stat_ftpct100']:
                    stat_from_ff[idx] = int(float(val) * 100)
                else:
                    stat_from_ff[idx] = int(val)

            stats = dict(zip(
                stat_vars,
                stat_from_ff,
            ))

            self.teams.update_or_create(
                url=team_url,
                defaults={
                    'name': team_name,
                    'owner': team_owner,
                    **stats,
                },
            )

        self.save()

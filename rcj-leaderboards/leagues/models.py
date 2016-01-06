from django.db import models

from ..core.models import UUIDModel


class RedditLeague(UUIDModel):
    name = models.CharField(max_length=128)
    url = models.URLField(unique=True)
    last_updated = models.DateTimeField(auto_now=True)


class RedditLeagueDivision(UUIDModel):
    name = models.CharField(max_length=128)
    url = models.URLField(blank=True, null=True)
    league = models.ForeignKey('RedditLeague')
    last_updated = models.DateTimeField(auto_now=True)


class FleaLeague(UUIDModel):
    name = models.CharField(max_length=128)
    url = models.URLField(unique=True)
    division = models.ForeignKey('RedditLeagueDivision')
    last_updated = models.DateTimeField(auto_now=True)

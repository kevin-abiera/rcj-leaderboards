from django.db import models
from django.db.models.lookups import BuiltinLookup

from django.http import Http404

import uuid
import shortuuid


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

    @property
    def shortuuid(self):
        return shortuuid.encode(self.id)

    def __str__(self):
        return self.shortuuid


@models.UUIDField.register_lookup
class ShortUUIDLookup(BuiltinLookup):
    lookup_name = 'shortuuid'

    def process_rhs(self, compiler, connection):
        # Decode shortuuid to hex
        try:
            short_uuid = shortuuid.decode(self.rhs).hex
        except ValueError:
            raise Http404('Invalid ID')

        self.rhs = short_uuid

        return super(ShortUUIDLookup, self).process_rhs(compiler, connection)

    def get_rhs_op(self, connection, rhs):
            return connection.operators['exact'] % rhs

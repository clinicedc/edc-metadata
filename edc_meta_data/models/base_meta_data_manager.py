from django.db import models

from edc_constants.constants import UNKEYED, KEYED


class BaseMetaDataManager(models.Manager):

    def unkeyed(self, appointment):
        return self.filter(appointment=appointment, entry_status=UNKEYED)

    def keyed(self, appointment):
        return self.filter(appointment=appointment, entry_status=KEYED)

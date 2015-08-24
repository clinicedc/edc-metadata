from django.db import models

from edc_visit_schedule.models import VisitDefinition
from django.contrib.contenttypes.models import ContentType


class EntryManager(models.Manager):

    def get_by_natural_key(self, visit_definition_code, app_label, model):
        """Returns the instance using the natural key."""
        visit_definition = VisitDefinition.objects.get_by_natural_key(visit_definition_code)
        content_type = ContentType.objects.get_by_natural_key(app_label, model)
        return self.get(content_type=content_type, visit_definition=visit_definition)

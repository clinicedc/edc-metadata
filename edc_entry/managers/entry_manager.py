from django.db import models
from edc.core.bhp_content_type_map.models import ContentTypeMap
from edc.subject.visit_schedule.models import VisitDefinition


class EntryManager(models.Manager):

    def get_by_natural_key(self, visit_definition_code, app_label, model):
        """Returns the instance using the natural key."""
        visit_definition = VisitDefinition.objects.get_by_natural_key(visit_definition_code)
        content_type_map = ContentTypeMap.objects.get_by_natural_key(app_label, model)
        return self.get(content_type_map=content_type_map, visit_definition=visit_definition)

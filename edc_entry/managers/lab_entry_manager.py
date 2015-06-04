from django.apps import apps as django_apps
from django.db import models


class LabEntryManager(models.Manager):

    def get_by_natural_key(self, visit_definition_code, name):
        VisitDefinition = django_apps.get_model('edc_visit_schedule', 'VisitDefinition')
        RequisitionPanel = django_apps.get_model('edc_entry', 'RequisitionPanel')
        visit_definition = VisitDefinition.objects.get_by_natural_key(visit_definition_code)
        requisition_panel = RequisitionPanel.objects.get_by_natural_key(name)
        return self.get(requisition_panel=requisition_panel, visit_definition=visit_definition)

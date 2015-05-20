from django.db import models


class LabEntryManager(models.Manager):

    def get_by_natural_key(self, visit_definition_code, name):
        VisitDefinition = models.get_model('visit_schedule', 'VisitDefinition')
        RequisitionPanel = models.get_model('entry', 'RequisitionPanel')
        visit_definition = VisitDefinition.objects.get_by_natural_key(visit_definition_code)
        requisition_panel = RequisitionPanel.objects.get_by_natural_key(name)
        return self.get(requisition_panel=requisition_panel, visit_definition=visit_definition)

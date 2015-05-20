from django.db import models

from edc.base.model.models import BaseModel

from ..managers import RequisitionPanelManager


class RequisitionPanel(BaseModel):
    """Relates to 'lab_entry' to indicate the requisition panel.

    This is usually kept in line with the protocol specific panel model data."""
    name = models.CharField(max_length=50, unique=True)

    aliquot_type_alpha_code = models.CharField(max_length=4)

    rule_group_name = models.CharField(
        max_length=50,
        help_text='reference used on rule groups. Defaults to name.')

    objects = RequisitionPanelManager()

    def __unicode__(self):
        return self.name

    def natural_key(self):
        return (self.name,)

    def save(self, *args, **kwargs):
        if not self.rule_group_name:
            self.rule_group_name = self.name
        super(RequisitionPanel, self).save(*args, **kwargs)

    class Meta:
        app_label = 'entry'

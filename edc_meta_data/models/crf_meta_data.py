from django.db import models

from edc_appointment.models import Appointment

from .base_meta_data import BaseMetaData

from .crf_entry import CrfEntry


class CrfMetaDataManager(models.Manager):

    def get_by_natural_key(
            self, visit_instance, visit_definition_code, subject_identifier_as_pk, code2, app_label, model):
        appointment = Appointment.objects.get_by_natural_key(
            visit_instance, visit_definition_code, subject_identifier_as_pk)
        crf_entry = CrfEntry.objects.get_by_natural_key(visit_definition_code, app_label, model)
        return self.get(appointment=appointment, crf_entry=crf_entry)


class CrfMetaData(BaseMetaData):
    """Subject-specific list of required and scheduled entry as per normal visit schedule."""

    appointment = models.ForeignKey(Appointment, related_name='+')

    crf_entry = models.ForeignKey(CrfEntry)

    objects = CrfMetaDataManager()

    def __unicode__(self):
        return unicode(self.current_entry_title) or u''

    def natural_key(self):
        return self.appointment.natural_key() + self.crf_entry.natural_key()

    def deserialize_get_missing_fk(self, attrname):
        retval = None
        if attrname == 'registered_subject':
            return self.registered_subject
        if attrname == 'appointment':
            return self.appointment
        return retval

    class Meta:
        app_label = 'edc_meta_data'
        verbose_name = "Crf Metadata"
        verbose_name_plural = "Crf Metadata"
        ordering = ['registered_subject', 'crf_entry', 'appointment']
        unique_together = ['registered_subject', 'crf_entry', 'appointment']

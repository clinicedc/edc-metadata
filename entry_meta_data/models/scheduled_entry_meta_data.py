from django.db import models

from edc.subject.appointment.models import Appointment
from edc.subject.entry.models import Entry

from .base_entry_meta_data import BaseEntryMetaData


class NaturalKeyEntryMetaDataManager(models.Manager):

    def get_by_natural_key(self, visit_instance, visit_definition_code, subject_identifier_as_pk, code2, app_label, model):
        Appointment = models.get_model('appointment', 'Appointment')
        Entry = models.get_model('entry', 'Entry')
        appointment = Appointment.objects.get_by_natural_key(visit_instance, visit_definition_code, subject_identifier_as_pk)
        entry = Entry.objects.get_by_natural_key(visit_definition_code, app_label, model)
        return self.get(appointment=appointment, entry=entry)


class ScheduledEntryMetaData(BaseEntryMetaData):
    """Subject-specific list of required and scheduled entry as per normal visit schedule."""

    appointment = models.ForeignKey(Appointment, related_name='+')

    entry = models.ForeignKey(Entry)

    objects = NaturalKeyEntryMetaDataManager()

    def __unicode__(self):
        return unicode(self.current_entry_title) or u''

    def natural_key(self):
        return self.appointment.natural_key() + self.entry.natural_key()

    def deserialize_get_missing_fk(self, attrname):
        retval = None
        if attrname == 'registered_subject':
            return self.registered_subject
        if attrname == 'appointment':
            return self.appointment
        return retval

    class Meta:
        app_label = 'entry_meta_data'
        verbose_name = "Scheduled Entry Metadata"
        ordering = ['registered_subject', 'entry', 'appointment']
        unique_together = ['registered_subject', 'entry', 'appointment']

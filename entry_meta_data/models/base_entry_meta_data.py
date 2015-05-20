from django.db import models

from edc.constants import NOT_REQUIRED
from edc.device.sync.models import BaseSyncUuidModel
from edc.subject.registration.models import RegisteredSubject
from edc.subject.entry.choices import ENTRY_STATUS


class BaseEntryMetaData(BaseSyncUuidModel):

    """ Base model for list of required entries by registered_subject. """

    registered_subject = models.ForeignKey(RegisteredSubject, related_name='+')
    current_entry_title = models.CharField(
        max_length=250,
        null=True)
    entry_status = models.CharField(
        max_length=25,
        choices=ENTRY_STATUS,
        default='NEW',
        db_index=True)
    due_datetime = models.DateTimeField(
        null=True,
        blank=True)
    report_datetime = models.DateTimeField(
        null=True,
        blank=True)
    entry_comment = models.TextField(
        max_length=250,
        null=True,
        blank=True)
    close_datetime = models.DateTimeField(
        null=True,
        blank=True)
    fill_datetime = models.DateTimeField(
        null=True,
        blank=True)

    def is_required(self):
        return self.entry_status != NOT_REQUIRED

    def is_not_required(self):
        return not self.is_required()

    def include_for_dispatch(self):
        return True

    class Meta:
        abstract = True

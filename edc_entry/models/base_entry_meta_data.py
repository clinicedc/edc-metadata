from django.db import models

from edc_base.model.models import BaseUuidModel
from edc_constants.constants import NEW
from edc_registration.models import RegisteredSubject
try:
    from edc_sync.mixins import SyncMixin
except ImportError:
    SyncMixin = type('SyncMixin', (object, ), {})

from ..choices import ENTRY_STATUS


class BaseEntryMetaData(SyncMixin, BaseUuidModel):

    """ Base model for list of required entries by registered_subject. """

    registered_subject = models.ForeignKey(RegisteredSubject, related_name='+')

    entry_status = models.CharField(
        max_length=25,
        choices=ENTRY_STATUS,
        default=NEW,
        db_index=True)

    report_datetime = models.DateTimeField(
        null=True,
        blank=True)

    entry_comment = models.TextField(
        max_length=250,
        null=True,
        blank=True)

    due_datetime = models.DateTimeField(
        null=True,
        blank=True)

    closed_datetime = models.DateTimeField(
        null=True,
        blank=True)

    def include_for_dispatch(self):
        return True

    class Meta:
        abstract = True

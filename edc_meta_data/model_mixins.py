from django.db import models

from edc_registration.model_mixins import RegisteredSubjectMixin

from .choices import ENTRY_STATUS
from .constants import NOT_REQUIRED, UNKEYED


class MetaDataModelMixin(RegisteredSubjectMixin, models.Model):

    """ Mixin for CrfMetaData and RequisitionMetaData models to be created in the local app.

    Use the specific model mixins below.
    """

    schedule_name = models.CharField(max_length=25, null=True)

    app_label = models.CharField(max_length=25, null=True)

    model_name = models.CharField(max_length=25, null=True)

    visit_code = models.CharField(max_length=25, null=True)

    current_entry_title = models.CharField(
        max_length=250,
        null=True)

    entry_status = models.CharField(
        max_length=25,
        choices=ENTRY_STATUS,
        default=UNKEYED,
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

    def natural_key(self):
        return (self.subject_identifier, self.visit_code) + self.crf_entry.natural_key()

    def is_required(self):
        return self.entry_status != NOT_REQUIRED

    def is_not_required(self):
        return not self.is_required()

    def include_for_dispatch(self):
        return True

    class Meta:
        abstract = True
        unique_together = ['subject_identifier', 'visit_code', 'appointment']


class CrfMetaDataModelMixin(MetaDataModelMixin):
    """Subject-specific list of required and scheduled entry as per normal visit schedule

    For example:

        class CrfMetaData(CrfMetaDataModelMixin, BaseUuidModel):

            registered_subject = models.ForeignKey(MyRegisteredSubject)

            appointment = models.ForeignKey(MyAppointment, related_name='+')

            class Meta:
                app_label = 'my_app'
    """

    def __str__(self):
        return str(self.current_entry_title) or ''

    class Meta:
        abstract = True
        verbose_name = "Crf Metadata"
        verbose_name_plural = "Crf Metadata"
        ordering = ['registered_subject', 'crf_entry', 'appointment']
        unique_together = ['registered_subject', 'crf_entry', 'appointment']


class RequisitionMetaDataModelMixin(MetaDataModelMixin):

    """Subject-specific list of required and scheduled lab as per normal visit schedule.

        class RequisitionMetaData(RequisitionMetaDataModelMixin, BaseUuidModel):

            registered_subject = models.ForeignKey(MyRegisteredSubject)

            appointment = models.ForeignKey(MyAppointment, related_name='+')

            class Meta:
                app_label = 'my_app'
    """

    schedule_name = models.CharField(max_length=25, null=True)

    app_label = models.CharField(max_length=25, null=True)

    model_name = models.CharField(max_length=25, null=True)

    panel_name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return '%s: %s' % (self.registered_subject.subject_identifier, self.panel_name)

#     def natural_key(self):
#         return self.appointment.natural_key() + self.lab_entry.natural_key()

    class Meta:
        abstract = True
        verbose_name = "Requisition Meta Data"
        verbose_name_plural = "Requisition Meta Data"
        ordering = ['registered_subject', 'lab_entry__requisition_panel__name', 'appointment', ]
        unique_together = ['registered_subject', 'lab_entry', 'appointment', ]

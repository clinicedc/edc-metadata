from django.db import models

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured

from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc_constants.constants import NOT_REQUIRED, REQUIRED
from edc_visit_schedule.models import VisitDefinition

from ..choices import ENTRY_CATEGORY, ENTRY_WINDOW, ENTRY_STATUS
from ..managers import LabEntryManager, EntryManager
from .requisition_panel import RequisitionPanel
from .base_window_period_item import BaseWindowPeriodItem


class BaseEntry(BaseWindowPeriodItem):

    """Links a model to a visit definition.

    The model class it links to must have the EntryMetaDataManager defined, see exception in save. """

    visit_definition = models.ForeignKey(VisitDefinition)

    content_type = models.ForeignKey(ContentType)

    app_label = models.CharField(
        max_length=50,
        editable=False,
        help_text='Updated by content_type on save',
    )

    model = models.CharField(
        max_length=50,
        editable=False,
        help_text='Updated by content_type on save',
    )

    name = models.CharField(
        max_length=100,
        editable=False,
        help_text='Updated by content_type on save'
    )

    visit_code = models.CharField(
        max_length=10,
        editable=False,
        help_text='Updated by visit_definition on save')

    entry_order = models.IntegerField()

    custom_name = models.CharField(
        verbose_name='Custom form title',
        max_length=100,
        null=True,
        blank=True
    )

    group_title = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text='for example, may be used to add to the form title on the change form to group serveral forms'
    )

    entry_category = models.CharField(
        max_length=25,
        choices=ENTRY_CATEGORY,
        default='CLINIC'
    )

    entry_window_calculation = models.CharField(
        max_length=25,
        choices=ENTRY_WINDOW,
        default='VISIT',
        help_text=('Base the edc_entry window period on the visit window period'
                   'or specify a form specific window period')
    )

    default_entry_status = models.CharField(
        max_length=25,
        choices=ENTRY_STATUS,
        default=REQUIRED
    )

    additional = models.BooleanField(
        default=False,
        help_text='If True lists the entry in the additional entries section'
    )

    def save(self, *args, **kwargs):
        self.app_label = self.content_type.app_label
        self.model = self.content_type.model
        self.name = self.content_type.name
        self.visit_code = self.visit_definition.code
        self.verify_entry_form_model_manager()
        super().save(*args, **kwargs)

    def resync_contenttype(self):
        """Sync this entry to its content type assuming the content type PK has changed.

        This could be called if Entry loaded from a fixture built using a ContentType
        from another installation."""
        content_type = ContentType.objects.get_by_natural_key(self.app_label, self.model)
        if content_type.id != self.content_type.id:
            self.content_type = content_type
            self.name = content_type.name
            self.save(update_fields=['content_type', 'name'])

    def natural_key(self):
        return self.visit_definition.natural_key() + (self.app_label, self.model)

    def verify_entry_form_model_manager(self):
        """Raises an error if entry form model is incorrectly configured."""
        try:
            self.entry_form_model.entry_meta_data_manager
        except AttributeError:
            raise ImproperlyConfigured(
                'Model {0}.{1} is missing a meta-data manager. Models represented by an Entry class '
                'require a meta data manager.'
                'Add entry_meta_data_manager=EntryMetaDataManager() to model class first.'.format(
                    self.app_label, self.model))

    @property
    def entry_form_model(self):
        """Returns the model class for this Entry from content type."""
        model = self.content_type.model_class()
        if self.name != model._meta.verbose_name:
            self.resync_contenttype()
            model = self.content_type.model_class()
        return model

    @property
    def entry_form_title(self):
        return self.custom_name or self.name

    def entry_form_object(self, pk):
        return self.entry_form_model(pk=pk)

    @property
    def required(self):
        return self.default_entry_status != NOT_REQUIRED

    @property
    def not_required(self):
        return not self.required

    class Meta:
        abstract = True


class Entry(BaseEntry):

    objects = EntryManager()
#
#     def __str__(self):
#         return '{0}: {1}'.format(self.visit_code, self.entry_form_title)

    class Meta:
        app_label = 'edc_entry'
        verbose_name = "Entry"
        verbose_name_plural = "Entries"
        ordering = ['visit_code', 'entry_order']
        unique_together = (('visit_code', 'app_label', 'model'), ('visit_code', 'entry_order'))


class LabEntry(BaseEntry):

    requisition_panel = models.ForeignKey(RequisitionPanel, null=True)

    objects = LabEntryManager()

#     def __unicode__(self):
#         return '{0}.{1}'.format(self.visit_definition.code, self.requisition_panel.name)

    def save(self, *args, **kwargs):
        self.custom_name = self.requisition_panel.name
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'edc_entry'
        verbose_name = "LabEntry"
        verbose_name_plural = "Lab Entries"
        ordering = ['visit_code', 'entry_order']
        unique_together = (('visit_code', 'app_label', 'model'), ('visit_code', 'entry_order'))

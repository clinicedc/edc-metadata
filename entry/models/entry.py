from django.db import models

from edc.constants import NOT_REQUIRED, REQUIRED
from edc.core.bhp_content_type_map.models import ContentTypeMap
from edc.subject.visit_schedule.models import BaseWindowPeriodItem, VisitDefinition

from ..choices import ENTRY_CATEGORY, ENTRY_WINDOW, ENTRY_STATUS
from ..exceptions import EntryManagerError
from ..managers import EntryManager


class Entry(BaseWindowPeriodItem):

    """Links a model to a visit definition.

    The model class it links to must have the EntryMetaDataManager defined, see exception in save. """

    visit_definition = models.ForeignKey(VisitDefinition)
    content_type_map = models.ForeignKey(ContentTypeMap,
        related_name='+',
        verbose_name='entry form / model')
    entry_order = models.IntegerField()
    group_title = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text='for example, may be used to add to the form title on the change form to group serveral forms')
    entry_category = models.CharField(
        max_length=25,
        choices=ENTRY_CATEGORY,
        default='CLINIC',
        db_index=True)
    entry_window_calculation = models.CharField(
        max_length=25,
        choices=ENTRY_WINDOW,
        default='VISIT',
        help_text='Base the entry window period on the visit window period or specify a form specific window period')
    default_entry_status = models.CharField(
        max_length=25,
        choices=ENTRY_STATUS,
        default=REQUIRED)
    additional = models.BooleanField(default=False, help_text='If True lists the entry in additional entries')
    app_label = models.CharField(max_length=50, null=True)

    model_name = models.CharField(max_length=50, null=True)

    objects = EntryManager()

    def save(self, *args, **kwargs):
        if not self.app_label:
            self.app_label = self.content_type_map.app_label
        if not self.model_name:
            self.model_name = self.content_type_map.model
        model = models.get_model(self.app_label, self.model_name)
        try:
            model.entry_meta_data_manager
        except AttributeError:
            raise EntryManagerError('Models linked by the Entry class require a meta data manager. Add entry_meta_data_manager=EntryMetaDataManager() to model {0}.{1}'.format(self.app_label, self.model_name))
        super(Entry, self).save(*args, **kwargs)

    def natural_key(self):
        return self.visit_definition.natural_key() + self.content_type_map.natural_key()

    def get_model(self):
        return models.get_model(self.app_label, self.model_name)

    def form_title(self):
        self.content_type_map.content_type.model_class()._meta.verbose_name

    def __unicode__(self):
        return '{0}: {1}'.format(self.visit_definition.code, self.content_type_map.content_type)

    @property
    def required(self):
        return self.default_entry_status != NOT_REQUIRED

    @property
    def not_required(self):
        return not self.required

    class Meta:
        app_label = 'entry'
        verbose_name = "Entry"
        ordering = ['visit_definition__code', 'entry_order', ]
        unique_together = ['visit_definition', 'content_type_map', ]

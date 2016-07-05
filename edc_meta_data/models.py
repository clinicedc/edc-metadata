from django.db import models
from django.apps import apps as django_apps
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from edc_base.model.models import BaseUuidModel
from edc_constants.constants import DEAD, OFF_STUDY, NOT_REQUIRED, REQUIRED
from edc_content_type_map.models import ContentTypeMap
from edc_meta_data.helpers import CrfMetaDataHelper, RequisitionMetaDataHelper
from edc_rule_groups.classes import site_rule_groups
from edc_visit_schedule.models import VisitDefinition
from edc_visit_tracking.models import VisitModelMixin

from .choices import ENTRY_CATEGORY, ENTRY_WINDOW, ENTRY_STATUS
from .exceptions import MetaDataManagerError


class RequisitionPanelManager(models.Manager):

    def get_by_natural_key(self, name):
        return self.get(name=name)


class RequisitionPanel(models.Model):
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
        app_label = 'edc_meta_data'


class EntryManager(models.Manager):

    def get_by_natural_key(self, visit_definition_code, app_label, model):
        """Returns the instance using the natural key."""
        visit_definition = VisitDefinition.objects.get_by_natural_key(visit_definition_code)
        content_type_map = ContentTypeMap.objects.get_by_natural_key(app_label, model)
        return self.get(content_type_map=content_type_map, visit_definition=visit_definition)


class CrfEntry(BaseUuidModel):

    """Links a model to a visit definition.

    The model class it links to must have the CrfMetaDataManager defined, see exception in save. """

    visit_definition = models.ForeignKey(VisitDefinition)

    content_type_map = models.ForeignKey(
        ContentTypeMap,
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
        model = django_apps.get_model(self.app_label, self.model_name)
        try:
            model.entry_meta_data_manager
        except AttributeError:
            raise MetaDataManagerError(
                'Models linked by the Entry class require a meta data manager. '
                'Add entry_meta_data_manager=CrfMetaDataManager(VisitModel) to model {0}.{1}'.format(
                    self.app_label, self.model_name))
        super(CrfEntry, self).save(*args, **kwargs)

    def natural_key(self):
        return self.visit_definition.natural_key() + self.content_type_map.natural_key()

    def get_model(self):
        return django_apps.get_model(self.app_label, self.model_name)

    def form_title(self):
        self.content_type_map.content_type.model_class()._meta.verbose_name

    def __str__(self):
        return '{0}: {1}'.format(self.visit_definition.code, self.content_type_map.content_type)

    @property
    def required(self):
        return self.default_entry_status != NOT_REQUIRED

    @property
    def not_required(self):
        return not self.required

    class Meta:
        app_label = 'edc_meta_data'
        verbose_name = "Crf Entry"
        verbose_name_plural = "Crf Entries"
        ordering = ['visit_definition__code', 'entry_order', ]
        unique_together = ['visit_definition', 'content_type_map', ]


class LabEntryManager(models.Manager):

    def get_by_natural_key(self, visit_definition_code, name):
        visit_definition = VisitDefinition.objects.get_by_natural_key(visit_definition_code)
        requisition_panel = RequisitionPanel.objects.get_by_natural_key(name)
        return self.get(requisition_panel=requisition_panel, visit_definition=visit_definition)


class LabEntry(BaseUuidModel):

    visit_definition = models.ForeignKey(VisitDefinition)

    requisition_panel = models.ForeignKey(RequisitionPanel, null=True)

    app_label = models.CharField(max_length=50, null=True, help_text='requisition_panel app_label')

    model_name = models.CharField(max_length=50, null=True, help_text='requisition_panel model_name')

    entry_order = models.IntegerField()

    entry_category = models.CharField(
        max_length=25,
        choices=ENTRY_CATEGORY,
        default='CLINIC')

    entry_window_calculation = models.CharField(
        max_length=25,
        choices=ENTRY_WINDOW,
        default='VISIT',
        help_text=('Base the entry window period on the visit window period '
                   'or specify a form specific window period'))

    default_entry_status = models.CharField(
        max_length=25,
        choices=ENTRY_STATUS,
        default=REQUIRED)

    additional = models.BooleanField(
        default=False,
        help_text='If True lists the lab_entry in additional requisitions')

    objects = LabEntryManager()

    def save(self, *args, **kwargs):
        model = django_apps.get_model(self.app_label, self.model_name)
        if not model:
            raise TypeError('Lab Entry \'{2}\' cannot determine requisition_panel model '
                            'from app_label=\'{0}\' and model_name=\'{1}\''.format(
                                self.app_label, self.model_name, self))
        try:
            model.entry_meta_data_manager
        except AttributeError:
            raise MetaDataManagerError(
                'Models linked by the LabEntry class require a meta data manager. '
                'Add entry_meta_data_manager=RequisitionMetaDataManager() to '
                'model {0}.{1}'.format(self.app_label, self.model_name))
        super(LabEntry, self).save(*args, **kwargs)

    def natural_key(self):
        return self.visit_definition.natural_key() + self.requisition_panel.natural_key()

    def get_model(self):
        return django_apps.get_model(self.app_label, self.model_name)

    def form_title(self):
        self.content_type_map.content_type.model_class()._meta.verbose_name

    def __unicode__(self):
        return '{0}.{1}'.format(self.visit_definition.code, self.requisition_panel.name)

    @property
    def required(self):
        return self.default_entry_status != NOT_REQUIRED

    @property
    def not_required(self):
        return not self.required

    class Meta:
        app_label = 'edc_meta_data'
        verbose_name = "Lab Entry"
        verbose_name_plural = "Lab Entries"
        ordering = ['visit_definition__code', 'entry_order', ]
        unique_together = ['visit_definition', 'requisition_panel', ]


@receiver(post_save, weak=False, dispatch_uid="meta_data_on_post_save")
def meta_data_on_post_save(sender, instance, raw, created, using, update_fields, **kwargs):
    if not raw:
        if isinstance(instance, VisitModelMixin):
            # These are visit models
            crf_meta_data_helper = CrfMetaDataHelper(instance.appointment, visit_instance=instance)
            crf_meta_data_helper.add_or_update_for_visit()
            requisition_meta_data_helper = RequisitionMetaDataHelper(instance.appointment, instance)
            requisition_meta_data_helper.add_or_update_for_visit()
            # update rule groups through the rule group controller, instance is a visit_instance
            RegisteredSubject = django_apps.get_app_config('edc_registration').model
            site_rule_groups.update_rules_for_source_model(RegisteredSubject, instance)
            site_rule_groups.update_rules_for_source_fk_model(RegisteredSubject, instance)

            instance = instance.custom_post_update_crf_meta_data()  # see CrfMetaDataMixin for visit model

            if instance.survival_status == DEAD:
                instance.require_death_report()
            else:
                instance.undo_require_death_report()
            if instance.study_status == OFF_STUDY:
                instance.require_off_study_report()
            else:
                instance.undo_require_off_study_report()
        else:
            try:
                change_type = 'I' if created else 'U'
                sender.entry_meta_data_manager.instance = instance
                sender.entry_meta_data_manager.visit_instance = getattr(
                    instance, sender.entry_meta_data_manager.visit_attr_name)
                try:
                    sender.entry_meta_data_manager.target_requisition_panel = getattr(instance, 'panel')
                except AttributeError as e:
                    if 'target_requisition_panel' in str(e):
                        pass
                sender.entry_meta_data_manager.update_meta_data(change_type)
                if sender.entry_meta_data_manager.instance:
                    sender.entry_meta_data_manager.run_rule_groups()
            except AttributeError as e:
                if 'entry_meta_data_manager' in str(e):
                    pass


@receiver(pre_delete, weak=False, dispatch_uid="meta_data_on_pre_delete")
def meta_data_on_pre_delete(sender, instance, using, **kwargs):
    """Delete metadata if the visit tracking instance is deleted."""
    if isinstance(instance, VisitModelMixin):
        app_config = django_apps.get_app_config('edc_meta_data')
        app_config.crf_meta_data
        app_config.crf_meta_data.objects.filter(appointment=instance.appointment).delete()
        app_config.requisition_meta_data.objects.filter(appointment=instance.appointment).delete()
    else:
        try:
            sender.entry_meta_data_manager.instance = instance
            sender.entry_meta_data_manager.visit_instance = getattr(
                instance, sender.entry_meta_data_manager.visit_attr_name)
            try:
                sender.entry_meta_data_manager.target_requisition_panel = getattr(instance, 'panel')
            except AttributeError as e:
                pass
            sender.entry_meta_data_manager.update_meta_data('D')
        except AttributeError as e:
            if 'entry_meta_data_manager' in str(e):
                pass
            else:
                raise

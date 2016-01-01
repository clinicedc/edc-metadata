from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from edc_rule_groups.classes import site_rule_groups
from edc_registration.models import RegisteredSubject
from edc_visit_tracking.models import VisitModelMixin

from .crf_meta_data import CrfMetaData
from .crf_meta_data_helper import CrfMetaDataHelper
from .requisition_meta_data import RequisitionMetaData
from .requisition_meta_data_helper import RequisitionMetaDataHelper


@receiver(post_save, weak=False, dispatch_uid="meta_data_on_post_save")
def meta_data_on_post_save(sender, instance, raw, created, using, update_fields, **kwargs):
    if not raw:
        if isinstance(instance, VisitModelMixin):
            # These are visit models
            crf_meta_data_helper = CrfMetaDataHelper(instance.appointment, instance)
            crf_meta_data_helper.add_or_update_for_visit()
            requisition_meta_data_helper = RequisitionMetaDataHelper(instance.appointment, instance)
            requisition_meta_data_helper.add_or_update_for_visit()
            # update rule groups through the rule group controller, instance is a visit_instance
            site_rule_groups.update_rules_for_source_model(RegisteredSubject, instance)
            site_rule_groups.update_rules_for_source_fk_model(RegisteredSubject, instance)

            # call custom meta data changes on this visit tracking instance.
            # see MetaDataMixin for visit model
            try:
                instance.custom_post_update_crf_meta_data()
            except AttributeError as e:
                if 'custom_post_update_crf_meta_data' not in str(e):
                    raise AttributeError('Exception in {}.\'custom_post_update_crf_meta_data\'. Got {}'.format(
                        instance._meta.model_name, str(e)))
        else:
            # These are subject models covered by a consent.
            try:
                change_type = 'I'
                if not created:
                    change_type = 'U'
                sender.entry_meta_data_manager.instance = instance
                sender.entry_meta_data_manager.visit_instance = getattr(
                    instance, sender.entry_meta_data_manager.visit_attr_name)
                try:
                    sender.entry_meta_data_manager.target_requisition_panel = getattr(instance, 'panel')
                except AttributeError as e:
                    pass
                sender.entry_meta_data_manager.update_meta_data(change_type)
                if sender.entry_meta_data_manager.instance:
                    sender.entry_meta_data_manager.run_rule_groups()
            except AttributeError as e:
                if 'entry_meta_data_manager' in str(e):
                    pass
                else:
                    raise


@receiver(pre_delete, weak=False, dispatch_uid="meta_data_on_pre_delete")
def meta_data_on_pre_delete(sender, instance, using, **kwargs):
    """Delete metadata if the visit tracking instance is deleted."""
    if isinstance(instance, VisitModelMixin):
        CrfMetaData.objects.filter(appointment=instance.appointment).delete()
        RequisitionMetaData.objects.filter(appointment=instance.appointment).delete()
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

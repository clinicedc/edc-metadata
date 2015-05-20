from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from edc.subject.registration.models import RegisteredSubject
from edc.subject.rule_groups.classes import site_rule_groups
from edc.subject.visit_tracking.models import BaseVisitTracking

from .requisition_meta_data import RequisitionMetaData
from .scheduled_entry_meta_data import ScheduledEntryMetaData


@receiver(post_save, weak=False, dispatch_uid="entry_meta_data_on_post_save")
def entry_meta_data_on_post_save(sender, instance, raw, created, using, update_fields, **kwargs):
    if not raw:
        if isinstance(instance, BaseVisitTracking):
            from ..helpers import ScheduledEntryMetaDataHelper, RequisitionMetaDataHelper
            scheduled_entry_helper = ScheduledEntryMetaDataHelper(instance.appointment, instance)
            scheduled_entry_helper.add_or_update_for_visit()
            requisition_meta_data_helper = RequisitionMetaDataHelper(instance.appointment, instance)
            requisition_meta_data_helper.add_or_update_for_visit()
            # update rule groups through the rule group controller, instance is a visit_instance
            site_rule_groups.update_rules_for_source_model(RegisteredSubject, instance)
            site_rule_groups.update_rules_for_source_fk_model(RegisteredSubject, instance)
        else:
            try:
                change_type = 'I'
                if not created:
                    change_type = 'U'
                sender.entry_meta_data_manager.instance = instance
                sender.entry_meta_data_manager.visit_instance = getattr(instance, sender.entry_meta_data_manager.visit_attr_name)
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


@receiver(pre_delete, weak=False, dispatch_uid="entry_meta_data_on_pre_delete")
def entry_meta_data_on_pre_delete(sender, instance, using, **kwargs):
    """Delete metadata if the visit tracking instance is deleted."""
    if isinstance(instance, BaseVisitTracking):
        ScheduledEntryMetaData.objects.filter(appointment=instance.appointment).delete()
        RequisitionMetaData.objects.filter(appointment=instance.appointment).delete()
    else:
        try:
            sender.entry_meta_data_manager.instance = instance
            sender.entry_meta_data_manager.visit_instance = getattr(instance, sender.entry_meta_data_manager.visit_attr_name)
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

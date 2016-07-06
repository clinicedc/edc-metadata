from django.apps import apps as django_apps
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from edc_constants.constants import DEAD, OFF_STUDY
from edc_meta_data.helpers import CrfMetaDataHelper, RequisitionMetaDataHelper
from edc_rule_groups.classes import site_rule_groups
from edc_visit_tracking.models import VisitModelMixin

from edc_visit_schedule.site_visit_schedules import site_visit_schedules


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

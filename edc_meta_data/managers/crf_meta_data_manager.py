from django.core.exceptions import ImproperlyConfigured

from ..models import CrfMetaData, CrfEntry

from .base_meta_data_manager import BaseMetaDataManager


class CrfMetaDataManager(BaseMetaDataManager):

    meta_data_model = CrfMetaData
    entry_model = CrfEntry
    entry_attr = 'crf_entry'

    def __repr__(self):
        return 'CrfMetaDataManager({0.instance!r})'.format(self)

    def __str__(self):
        return '({0.instance!r})'.format(self)

    def create_meta_data(self):
        """Creates a meta_data instance for the model at the time point (appointment)
        for the given registered_subject.

        Might return None and meta data not created based on visit reason (e.g. missed)."""
        if self.visit_instance.reason not in self.skip_create_visit_reasons:
            try:
                crf_entry = self.entry_model.objects.get(
                    app_label=self.model._meta.app_label.lower(),
                    model_name=self.model._meta.object_name.lower(),
                    visit_definition=self.appointment_zero.visit_definition)
            except self.entry_model.DoesNotExist:
                raise ImproperlyConfigured(
                    'Entry matching query does not exist in visit {0}. Model {1}.Check your'
                    ' visit schedule configuration or rule groups.'.format(
                        self.appointment_zero.visit_definition, self.model))
            return self.meta_data_model.objects.create(
                appointment=self.appointment_zero,
                registered_subject=self.appointment_zero.registered_subject,
                due_datetime=crf_entry.visit_definition.get_upper_window_datetime(
                    self.visit_instance.report_datetime),
                crf_entry=crf_entry,
                entry_status=crf_entry.default_entry_status)
        return None

    @property
    def default_entry_status(self):
        return self.meta_data_instance.entry.default_entry_status

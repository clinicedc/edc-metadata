from django.apps.config import AppConfig as DjangoAppConfig
from django.apps import apps as django_apps
from django.core.exceptions import ImproperlyConfigured


class AppConfig(DjangoAppConfig):
    name = 'edc_meta_data'
    model_attrs = None  # list of [(app_label, crfmetadata), (app_label, requisitionmetadata)]
    crf_meta_data_model_name = 'crfmetadata'
    requisition_meta_data_model_name = 'requisitionmetadata'

    @property
    def crf_meta_data_model(self):
        model_attrs = None
        try:
            model_attrs = [attrs for attrs in self.model_attrs if attrs[1] == self.crf_meta_data_model_name][0]
        except TypeError:
            raise ImproperlyConfigured(
                'Expected list of tuples for model_attrs. Got {}. See {}'.format(self.model_attrs, self.__class__))
        return django_apps.get_model(*model_attrs)

    @property
    def requisition_meta_data_model(self):
        model_attrs = [attrs for attrs in self.model_attrs if attrs[1] == self.requisition_meta_data_model_name][0]
        return django_apps.get_model(*model_attrs)

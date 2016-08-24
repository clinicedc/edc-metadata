import sys

from django.apps.config import AppConfig as DjangoAppConfig
from django.apps import apps as django_apps


class AppConfig(DjangoAppConfig):
    name = 'edc_meta_data'
    app_label = 'edc_meta_data'
    crf_meta_data_model_name = 'crfmetadata'
    requisition_meta_data_model_name = 'requisitionmetadata'

    def ready(self):
        sys.stdout.write('Loading {} ...\n'.format(self.verbose_name))
        if self.app_label == self.name:
            sys.stdout.write('  * using default meta_data models from \'{}\'\n'.format(self.app_label))
        else:
            sys.stdout.write('  * using custom meta_data models from \'{}\'\n'.format(self.app_label))
        sys.stdout.write(' Done loading {}.\n'.format(self.verbose_name))

    @property
    def crf_meta_data_model(self):
        return django_apps.get_model(self.app_label, self.crf_meta_data_model_name)

    @property
    def requisition_meta_data_model(self):
        return django_apps.get_model(self.app_label, self.requisition_meta_data_model_name)

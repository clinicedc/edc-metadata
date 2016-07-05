from django.apps import AppConfig

from edc_appointment.apps import EdcAppointmentAppConfig as EdcAppointmentAppConfigParent
from edc_meta_data.apps import EdcMetaDataAppConfig as EdcMetaDataAppConfigParent


class ExampleAppConfig(AppConfig):
    name = 'example'
    verbose_name = 'Example Project'
    institution = 'Botswana-Harvard AIDS Institute Partnership'


class EdcAppointmentAppConfig(EdcAppointmentAppConfigParent):
    model = ('example', 'appointment')


class EdcMetaDataAppConfig(EdcMetaDataAppConfigParent):
    model_attrs = [('example', 'crfmetadata'), ('example', 'requisitionmetadata')]

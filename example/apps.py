from django.apps import AppConfig as DjangoAppConfig
from edc_consent.apps import AppConfig as EdcConsentAppConfigParent
from edc_visit_tracking.apps import AppConfig as EdcVisitTrackingAppConfigParent
from datetime import datetime
from dateutil.relativedelta import relativedelta


class AppConfig(DjangoAppConfig):
    name = 'example'


class EdcVisitTrackingAppConfig(EdcVisitTrackingAppConfigParent):
    visit_models = {'example': 'subject_visit'}


class EdcConsentAppConfig(EdcConsentAppConfigParent):
    consent_type_setup = [
        {'app_label': 'example',
         'model_name': 'subjectconsent',
         'start_datetime': datetime.today() + relativedelta(years=-1),
         'end_datetime': datetime.today() + relativedelta(years=+1),
         'version': '1'}
    ]

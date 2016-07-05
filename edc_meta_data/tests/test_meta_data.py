from django.test import TestCase
from edc_meta_data.crf_meta_data_mixin import CrfMetaDataMixin
from edc_meta_data.apps import EdcMetaDataAppConfig
from example.models import CrfMetaData, RequisitionMetaData, Appointment, RegisteredSubject
from edc_visit_schedule.models import VisitDefinition
from edc_content_type_map.models import ContentTypeMap
from edc_content_type_map.apps import edc_content_type_callback, EdcContentTypeAppConfig
from edc_appointment.apps import EdcAppointmentAppConfig
from django.utils import timezone


class TestMetaData(TestCase):

    def setUp(self):
        self.sync_content_type_map()

        EdcMetaDataAppConfig.model_attrs = [('example', 'crfmetadata'), ('example', 'requisitionmetadata')]
        EdcAppointmentAppConfig.model = ('example', 'appointment')

        ct = ContentTypeMap.objects.get(content_type__app_label='example', content_type__model='subjectvisit')
        self.visit_defininition = VisitDefinition.objects.create(
            code='1000',
            title='Visit 1000',
            visit_tracking_content_type_map=ct
        )

        registered_subject = RegisteredSubject.objects.create(subject_identifier='123456789')
        self.appointment = Appointment.objects.create(
            registered_subject=registered_subject,
            appt_datetime=timezone.now(),
            visit_definition=self.visit_defininition,
        )

    def sync_content_type_map(self):
        edc_content_type_callback(EdcContentTypeAppConfig, verbose=False)

    def test_finds_crf_meta_data_model(self):
        mixin = CrfMetaDataMixin()
        self.assertTrue(mixin.crf_meta_data_model == CrfMetaData)

    def test_finds_requisition_meta_data_model(self):
        mixin = CrfMetaDataMixin()
        self.assertTrue(mixin.requisition_meta_data_model == RequisitionMetaData)

    def test_creates_meta_data(self):
        mixin = CrfMetaDataMixin()
        appointment = Appointment(
            visit_definition=VisitDefinition())
        mixin.create_crf_meta_data(appointment, '', '', '')

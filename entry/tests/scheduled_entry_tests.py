# from datetime import datetime
# 
# from django.test import TestCase
# from django.db import models
# 
# from edc.core.bhp_content_type_map.classes import ContentTypeMapHelper
# from edc.core.bhp_content_type_map.models import ContentTypeMap
# from edc.core.bhp_variables.tests.factories import StudySpecificFactory, StudySiteFactory
# from edc.dashboard.subject.classes import RegisteredSubjectDashboard
# from edc.subject.appointment.models import Appointment
# from edc.subject.consent.tests.factories import ConsentCatalogueFactory
# from edc.subject.entry.tests.factories import EntryFactory
# from edc.subject.lab_entry.tests.factories import LabEntryFactory
# from edc.subject.lab_entry.models import ScheduledLabEntryMetaData
# from edc.subject.lab_tracker.classes import site_lab_tracker
# from edc.subject.registration.models import RegisteredSubject
# from edc.subject.visit_schedule.tests.factories import MembershipFormFactory, ScheduleGroupFactory, VisitDefinitionFactory
# from edc.testing.models import TestConsent
# from edc.testing.tests.factories import TestConsentWithMixinFactory, TestVisitFactory
# 
# from ..models import ScheduledEntryMetaData
# 
# 
# class ScheduledEntryTests(TestCase):
# 
#     app_label = 'testing'
#     consent_catalogue_name = 'v1'
# 
#     def setUp(self):
#         site_lab_tracker.autodiscover()
#         study_specific = StudySpecificFactory()
#         StudySiteFactory()
#         content_type_map_helper = ContentTypeMapHelper()
#         content_type_map_helper.populate()
#         content_type_map_helper.sync()
#         content_type_map = ContentTypeMap.objects.get(content_type__model='TestConsentWithMixin'.lower())
#         ConsentCatalogueFactory(
#             name=self.app_label,
#             consent_type='study',
#             content_type_map=content_type_map,
#             version=1,
#             start_datetime=study_specific.study_start_datetime,
#             end_datetime=datetime(datetime.today().year + 5, 1, 1),
#             add_for_app=self.app_label)
#         membership_form = MembershipFormFactory(content_type_map=content_type_map, category='subject')
#         schedule_group = ScheduleGroupFactory(membership_form=membership_form, group_name='GROUP_NAME', grouping_key='GROUPING_KEY')
#         visit_tracking_content_type_map = ContentTypeMap.objects.get(content_type__model='testvisit')
#         visit_definition = VisitDefinitionFactory(code='T0', title='T0', grouping='subject', visit_tracking_content_type_map=visit_tracking_content_type_map)
#         visit_definition.schedule_group.add(schedule_group)
# 
#         # add entries
#         content_type_map = ContentTypeMap.objects.get(app_label='testing', model='testscheduledmodel1')
#         EntryFactory(content_type_map=content_type_map, visit_definition=visit_definition, entry_order=100, entry_category='clinic')
#         content_type_map = ContentTypeMap.objects.get(app_label='testing', model='testscheduledmodel2')
#         EntryFactory(content_type_map=content_type_map, visit_definition=visit_definition, entry_order=110, entry_category='clinic')
#         content_type_map = ContentTypeMap.objects.get(app_label='testing', model='testscheduledmodel3')
#         EntryFactory(content_type_map=content_type_map, visit_definition=visit_definition, entry_order=120, entry_category='clinic')
# 
#         # add requisitions
#         LabEntryFactory(visit_definition=visit_definition, entry_order=100)
#         LabEntryFactory(visit_definition=visit_definition, entry_order=110)
#         LabEntryFactory(visit_definition=visit_definition, entry_order=120)
# 
#         self.test_consent = TestConsentWithMixinFactory(gender='M')
# 
#         self.registered_subject = RegisteredSubject.objects.get(subject_identifier=self.test_consent.subject_identifier)
#         self.appointment = Appointment.objects.get(registered_subject=self.registered_subject)
#         self.test_visit = TestVisitFactory(appointment=self.appointment)
# 
#     def test_p1(self):
#         """All entries should be set to New."""
#         # create a dashboard
#         TestVisit = models.get_model('testing', 'TestVisit')
#         dashboard = RegisteredSubjectDashboard(
#                         dashboard_type='subject',
#                         dashboard_id=self.test_visit.pk,
#                         dashboard_model='visit',
#                         dashboard_type_list=['subject'],
#                         dashboard_models={'testconsent': TestConsent, 'visit': TestVisit},
#                         membership_form_category='subject',
#                         visit_model=TestVisit,
#                         registered_subject=self.registered_subject,
#                         show='forms',
#                         has_requisition_model=True)
#         dashboard.render_scheduled_forms()
# 
#         self.assertEqual(ScheduledEntryMetaData.objects.count(), 3)
#         self.assertEqual(ScheduledLabEntryMetaData.objects.count(), 3)
# 
#     def test_p2(self):
#         """Add a model instance, ScheduledEntryMetaData is updated to KEYED."""
#         pass
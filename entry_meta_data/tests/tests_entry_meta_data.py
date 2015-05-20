from django.test import TestCase

from edc.core.bhp_variables.models import StudySite
from edc.entry_meta_data.models import ScheduledEntryMetaData, RequisitionMetaData
from edc.subject.appointment.models import Appointment
from edc.subject.entry.models import LabEntry
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.registration.models import RegisteredSubject
from edc.subject.visit_schedule.models import VisitDefinition
from edc.testing.models import TestPanel, TestAliquotType, TestScheduledModel1
from edc.testing.classes import TestVisitSchedule, TestAppConfiguration
from edc.testing.classes import TestLabProfile
from edc.testing.tests.factories import TestConsentWithMixinFactory, TestScheduledModel1Factory, TestRequisitionFactory
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.testing.tests.factories import TestVisitFactory


class TestsEntryMetaData(TestCase):

    app_label = 'testing'
    consent_catalogue_name = 'v1'

    def setUp(self):
        try:
            site_lab_profiles.register(TestLabProfile())
        except AlreadyRegisteredLabProfile:
            pass
        site_lab_tracker.autodiscover()

        TestAppConfiguration()

        TestVisitSchedule().rebuild()

        self.test_visit_factory = TestVisitFactory
        self.study_site = StudySite.objects.all()[0]
        self.visit_definition = VisitDefinition.objects.get(code='1000')
        self.test_consent = TestConsentWithMixinFactory(gender='M', study_site=self.study_site)
        self.registered_subject = RegisteredSubject.objects.get(subject_identifier=self.test_consent.subject_identifier)
        self.appointment_count = VisitDefinition.objects.all().count()
        self.appointment = Appointment.objects.get(registered_subject=self.registered_subject, visit_definition__code='1000')

    def test_creates_meta_data1(self):
        """No meta data if visit tracking form is not entered."""
        self.assertEqual(ScheduledEntryMetaData.objects.filter(registered_subject=self.registered_subject).count(), 0)

    def test_creates_requisition_meta_data(self):
        """Meta data is created when visit tracking form is added, each instance set to NEW."""
        self.assertTrue(LabEntry.objects.all().count() > 0)
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        self.assertEqual(RequisitionMetaData.objects.filter(registered_subject=self.registered_subject).count(), 3)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NEW', registered_subject=self.registered_subject).count(), 3)

    def test_creates_requisition_meta_data2(self):
        """Meta data is unchanged if you re-save visit."""
        self.assertTrue(LabEntry.objects.all().count() > 0)
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        self.test_visit.save()
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NEW', registered_subject=self.registered_subject).count(), 3)

    def test_updates_requisition_meta_data(self):
        """Asserts metadata is updated if requisition model is keyed."""
        self.assertEquals(RequisitionMetaData.objects.all().count(), 0)
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        self.assertEquals(RequisitionMetaData.objects.all().count(), 3)
        self.assertEqual([obj.entry_status for obj in RequisitionMetaData.objects.all()], ['NEW', 'NEW', 'NEW'])
        self.assertEquals(RequisitionMetaData.objects.filter(entry_status='NEW').count(), 3)
        requisition_panel = RequisitionMetaData.objects.filter(registered_subject=self.registered_subject)[0].lab_entry.requisition_panel
        panel = TestPanel.objects.get(name=requisition_panel.name)
        aliquot_type = TestAliquotType.objects.get(alpha_code=requisition_panel.aliquot_type_alpha_code)
        self.assertEqual(RequisitionMetaData.objects.filter(
            entry_status='NEW',
            registered_subject=self.registered_subject,
            lab_entry__app_label='testing',
            lab_entry__model_name='testrequisition',
            lab_entry__requisition_panel__name=panel.name).count(), 1)
        obj = TestRequisitionFactory(site=self.study_site, test_visit=self.test_visit, panel=panel, aliquot_type=aliquot_type, requisition_identifier='WJ000001')
        #obj.save(), site=self.study_site
        self.assertEqual(RequisitionMetaData.objects.filter(
            entry_status='KEYED',
            registered_subject=self.registered_subject,
            lab_entry__app_label='testing',
            lab_entry__model_name='testrequisition',
            lab_entry__requisition_panel__name=obj.panel.name).count(), 1)

    def test_updates_requisition_meta_data2(self):
        """Meta data is set to KEYED and is unchanged if you re-save requisition or re-save visit."""
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        requisition_panel = RequisitionMetaData.objects.filter(registered_subject=self.registered_subject)[0].lab_entry.requisition_panel
        panel = TestPanel.objects.get(name=requisition_panel.name)
        aliquot_type = TestAliquotType.objects.get(alpha_code=requisition_panel.aliquot_type_alpha_code)
        obj = TestRequisitionFactory(site=self.study_site, test_visit=self.test_visit, panel=panel, aliquot_type=aliquot_type, requisition_identifier='WJ0000002')
        obj.save()
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='KEYED',
                                                            registered_subject=self.registered_subject,
                                                            lab_entry__app_label='testing',
                                                            lab_entry__model_name='testrequisition',
                                                            lab_entry__requisition_panel__name=obj.panel.name).count(), 1)
        self.test_visit.save()
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='KEYED',
                                                            registered_subject=self.registered_subject,
                                                            lab_entry__app_label='testing',
                                                            lab_entry__model_name='testrequisition',
                                                            lab_entry__requisition_panel__name=obj.panel.name).count(), 1)
        obj.save()
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='KEYED',
                                                            registered_subject=self.registered_subject,
                                                            lab_entry__app_label='testing',
                                                            lab_entry__model_name='testrequisition',
                                                            lab_entry__requisition_panel__name=obj.panel.name).count(), 1)

    def test_updates_requisition_meta_data3(self):
        """Meta data is set to KEYED and is unchanged if you re-save requisition or re-save visit."""
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        self.assertEqual(RequisitionMetaData.objects.filter(registered_subject=self.registered_subject).count(), 3)
        requisition_panel = RequisitionMetaData.objects.filter(registered_subject=self.registered_subject)[0].lab_entry.requisition_panel
        panel = TestPanel.objects.get(name=requisition_panel.name)
        aliquot_type = TestAliquotType.objects.get(alpha_code=requisition_panel.aliquot_type_alpha_code)
        obj = TestRequisitionFactory(site=self.study_site, test_visit=self.test_visit, panel=panel, aliquot_type=aliquot_type, requisition_identifier='WJ0000003')
        obj.save()
        self.assertEqual(RequisitionMetaData.objects.filter(
            entry_status='KEYED',
            registered_subject=self.registered_subject,
            lab_entry__app_label='testing',
            lab_entry__model_name='testrequisition',
            lab_entry__requisition_panel__name=panel.name).count(), 1)
        obj.delete()
        self.assertEqual(RequisitionMetaData.objects.filter(
            entry_status='NEW',
            registered_subject=self.registered_subject,
            lab_entry__app_label='testing',
            lab_entry__model_name='testrequisition',
            lab_entry__requisition_panel__name=panel.name).count(), 1)

    def test_creates_meta_data2(self):
        """Meta data is created when visit tracking form is added, each instance set to NEW."""
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', registered_subject=self.registered_subject).count(), 3)

    def test_creates_meta_data3(self):
        """ """
        self.assertEqual(ScheduledEntryMetaData.objects.filter(registered_subject=self.registered_subject).count(), 0)
        test_visit = self.test_visit_factory(appointment=self.appointment)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(registered_subject=self.registered_subject).count(), 3)
        TestScheduledModel1Factory(test_visit=test_visit)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED', registered_subject=self.registered_subject).count(), 1)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', registered_subject=self.registered_subject).count(), 2)

    def test_creates_meta_data4(self):
        """Meta data is deleted when visit tracking form is deleted."""
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        self.assertEqual(RequisitionMetaData.objects.filter(registered_subject=self.registered_subject).count(), 3)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(registered_subject=self.registered_subject).count(), 3)
        self.test_visit.delete()
        self.assertEqual(ScheduledEntryMetaData.objects.filter(registered_subject=self.registered_subject).count(), 0)
        self.assertEqual(RequisitionMetaData.objects.filter(registered_subject=self.registered_subject).count(), 0)

    def test_creates_meta_data5(self):
        """Meta data is not created if visit reason is missed. See 'skip_create_visit_reasons class' attribute"""
        self.test_visit = self.test_visit_factory(appointment=self.appointment, reason='missed')
        self.assertEqual(ScheduledEntryMetaData.objects.filter(registered_subject=self.registered_subject).count(), 0)

    def test_updates_meta_data4(self):
        """Meta data instance linked to the model is updated if model is entered."""
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        TestScheduledModel1Factory(test_visit=self.test_visit)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED', registered_subject=self.registered_subject, entry__content_type_map__model='testscheduledmodel1').count(), 1)

    def test_updates_meta_data5(self):
        """Meta data instance linked to the model is updated if model is entered and then updated."""
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        obj = TestScheduledModel1Factory(test_visit=self.test_visit)
        obj.save()
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED',
                                                               registered_subject=self.registered_subject,
                                                               entry__app_label='testing',
                                                               entry__model_name='testscheduledmodel1').count(), 1)

    def test_updates_meta_data6(self):
        """Meta data instance linked to the model is updated if model is deleted."""
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        obj = TestScheduledModel1Factory(test_visit=self.test_visit)
        obj.delete()
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='NEW', registered_subject=self.registered_subject, entry__content_type_map__model='testscheduledmodel1').count(), 1)

    def test_updates_meta_data7(self):
        """Meta data instance linked to the model is created if missing, knows model is KEYED."""
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        ScheduledEntryMetaData.objects.filter(entry_status='NEW', registered_subject=self.registered_subject, entry__model_name='testscheduledmodel1').delete()
        TestScheduledModel1Factory(test_visit=self.test_visit)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED', registered_subject=self.registered_subject, entry__model_name='testscheduledmodel1').count(), 1)

    def test_requisition_meta_data1(self):
        """"""
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        self.assertEqual(RequisitionMetaData.objects.filter(registered_subject=self.registered_subject).count(), 3)
        requisition_panels = [requisition_meta_data.lab_entry.requisition_panel for requisition_meta_data in RequisitionMetaData.objects.filter(registered_subject=self.registered_subject)]
        for requisition_panel in requisition_panels:
            panel = TestPanel.objects.get(name=requisition_panel.name)
            aliquot_type = TestAliquotType.objects.get(alpha_code=requisition_panel.aliquot_type_alpha_code)
            obj = TestRequisitionFactory(site=self.study_site,
                                         test_visit=self.test_visit,
                                         panel=panel,
                                         aliquot_type=aliquot_type,
                                         requisition_identifier='WJ0000003')
            obj.save()
            self.assertEqual(RequisitionMetaData.objects.filter(
                entry_status='KEYED',
                registered_subject=self.registered_subject,
                lab_entry__app_label='testing',
                lab_entry__model_name='testrequisition',
                lab_entry__requisition_panel__name=panel.name).count(), 1)
            self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NEW',
                                                                registered_subject=self.registered_subject).count(), 2)
            self.assertEqual(RequisitionMetaData.objects.filter(entry_status='KEYED',
                                                                registered_subject=self.registered_subject).count(), 1)
            obj.delete()
            self.assertEqual(RequisitionMetaData.objects.filter(
                entry_status='NEW',
                registered_subject=self.registered_subject,
                lab_entry__app_label='testing',
                lab_entry__model_name='testrequisition',
                lab_entry__requisition_panel__name=panel.name).count(), 1)
            self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NEW',
                                                                registered_subject=self.registered_subject).count(), 3)

    def test_new_meta_data_never_keyed(self):
        """Meta data instance linked to the model is updated if model is deleted."""
        self.assertTrue(TestScheduledModel1.objects.all().count() == 0)
        self.assertEqual(ScheduledEntryMetaData.objects.filter(registered_subject=self.registered_subject).count(), 0)
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        for obj in ScheduledEntryMetaData.objects.filter(registered_subject=self.registered_subject):
            print obj.entry_status, obj.entry
        self.assertEqual(ScheduledEntryMetaData.objects.filter(entry_status='KEYED', registered_subject=self.registered_subject).count(), 0)

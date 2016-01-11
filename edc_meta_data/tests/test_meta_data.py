from __future__ import print_function

from edc_constants.constants import KEYED, UNKEYED, MISSED_VISIT
from edc_meta_data.models import CrfMetaData, RequisitionMetaData
from edc_meta_data.models import LabEntry
from edc_testing.models import TestVisit, TestPanel, TestAliquotType, TestScheduledModel1
from edc_testing.tests.factories import TestScheduledModel1Factory, TestRequisitionFactory

from .base_test_case import BaseTestCase
from django.utils import timezone


class TestMetaData(BaseTestCase):

    def test_creates_meta_data1(self):
        """No meta data if visit tracking form is not entered."""
        self.assertEqual(CrfMetaData.objects.filter(
            registered_subject=self.registered_subject).count(), 0)

    def test_creates_requisition_meta_data(self):
        """Meta data is created when visit tracking form is added, each instance set to NEW."""
        self.assertTrue(LabEntry.objects.all().count() > 0)
        self.test_visit = TestVisit.objects.create(
            appointment=self.appointment,
            report_datetime=timezone.now())
        self.assertEqual(RequisitionMetaData.objects.filter(
            registered_subject=self.registered_subject).count(), 3)
        self.assertEqual(RequisitionMetaData.objects.filter(
            entry_status=UNKEYED, registered_subject=self.registered_subject).count(), 3)

    def test_creates_requisition_meta_data2(self):
        """Meta data is unchanged if you re-save visit."""
        self.assertTrue(LabEntry.objects.all().count() > 0)
        self.test_visit = TestVisit.objects.create(
            appointment=self.appointment,
            report_datetime=timezone.now())
        self.test_visit.save()
        self.assertEqual(RequisitionMetaData.objects.filter(
            entry_status=UNKEYED, registered_subject=self.registered_subject).count(), 3)

    def test_updates_requisition_meta_data(self):
        """Asserts metadata is updated if requisition model is keyed."""
        self.assertEquals(RequisitionMetaData.objects.filter(
            registered_subject=self.appointment.registered_subject).count(), 0)
        self.test_visit = TestVisit.objects.create(
            appointment=self.appointment,
            report_datetime=timezone.now())
        self.assertEquals(RequisitionMetaData.objects.filter(
            registered_subject=self.appointment.registered_subject,
            entry_status=UNKEYED).count(), 3)
        requisition_panel = RequisitionMetaData.objects.filter(
            registered_subject=self.registered_subject)[0].lab_entry.requisition_panel
        panel = TestPanel.objects.get(name=requisition_panel.name)
        aliquot_type = TestAliquotType.objects.get(alpha_code=requisition_panel.aliquot_type_alpha_code)
        self.assertEqual(RequisitionMetaData.objects.filter(
            registered_subject=self.appointment.registered_subject,
            entry_status=UNKEYED,
            lab_entry__app_label='edc_testing',
            lab_entry__model_name='testrequisition',
            lab_entry__requisition_panel__name=panel.name).count(), 1)
        obj = TestRequisitionFactory(
            study_site=self.study_site,
            test_visit=self.test_visit,
            panel=panel,
            aliquot_type=aliquot_type,
            requisition_identifier='WJ000001')

        self.assertEqual(RequisitionMetaData.objects.filter(
            entry_status=KEYED,
            registered_subject=self.registered_subject,
            lab_entry__app_label='edc_testing',
            lab_entry__model_name='testrequisition',
            lab_entry__requisition_panel__name=obj.panel.name).count(), 1)

    def test_updates_requisition_meta_data2(self):
        """Meta data is set to KEYED and is unchanged if you re-save requisition or re-save visit."""
        self.test_visit = TestVisit.objects.create(
            appointment=self.appointment,
            report_datetime=timezone.now())
        requisition_panel = RequisitionMetaData.objects.filter(
            registered_subject=self.registered_subject)[0].lab_entry.requisition_panel
        panel = TestPanel.objects.get(name=requisition_panel.name)
        aliquot_type = TestAliquotType.objects.get(alpha_code=requisition_panel.aliquot_type_alpha_code)
        obj = TestRequisitionFactory(
            study_site=self.study_site,
            test_visit=self.test_visit,
            panel=panel,
            aliquot_type=aliquot_type,
            requisition_identifier='WJ0000002')
        obj.save()
        self.assertEqual(RequisitionMetaData.objects.filter(
            entry_status=KEYED,
            registered_subject=self.registered_subject,
            lab_entry__app_label='edc_testing',
            lab_entry__model_name='testrequisition',
            lab_entry__requisition_panel__name=obj.panel.name).count(), 1)
        self.test_visit.save()
        self.assertEqual(RequisitionMetaData.objects.filter(
            entry_status=KEYED,
            registered_subject=self.registered_subject,
            lab_entry__app_label='edc_testing',
            lab_entry__model_name='testrequisition',
            lab_entry__requisition_panel__name=obj.panel.name).count(), 1)
        obj.save()
        self.assertEqual(RequisitionMetaData.objects.filter(
            entry_status=KEYED,
            registered_subject=self.registered_subject,
            lab_entry__app_label='edc_testing',
            lab_entry__model_name='testrequisition',
            lab_entry__requisition_panel__name=obj.panel.name).count(), 1)

    def test_updates_requisition_meta_data3(self):
        """Meta data is set to KEYED and is unchanged if you re-save requisition or re-save visit."""
        self.test_visit = TestVisit.objects.create(
            appointment=self.appointment,
            report_datetime=timezone.now())
        self.assertEqual(RequisitionMetaData.objects.filter(registered_subject=self.registered_subject).count(), 3)
        requisition_panel = RequisitionMetaData.objects.filter(
            registered_subject=self.registered_subject)[0].lab_entry.requisition_panel
        panel = TestPanel.objects.get(name=requisition_panel.name)
        aliquot_type = TestAliquotType.objects.get(alpha_code=requisition_panel.aliquot_type_alpha_code)
        obj = TestRequisitionFactory(
            study_site=self.study_site,
            test_visit=self.test_visit,
            panel=panel,
            aliquot_type=aliquot_type,
            requisition_identifier='WJ0000003')
        obj.save()
        self.assertEqual(RequisitionMetaData.objects.filter(
            entry_status=KEYED,
            registered_subject=self.registered_subject,
            lab_entry__app_label='edc_testing',
            lab_entry__model_name='testrequisition',
            lab_entry__requisition_panel__name=panel.name).count(), 1)
        obj.delete()
        self.assertEqual(RequisitionMetaData.objects.filter(
            entry_status=UNKEYED,
            registered_subject=self.registered_subject,
            lab_entry__app_label='edc_testing',
            lab_entry__model_name='testrequisition',
            lab_entry__requisition_panel__name=panel.name).count(), 1)

    def test_creates_meta_data2(self):
        """Meta data is created when visit tracking form is added, each instance set to NEW."""
        self.test_visit = TestVisit.objects.create(
            appointment=self.appointment,
            report_datetime=timezone.now())
        self.assertEqual(
            CrfMetaData.objects.filter(
                entry_status=UNKEYED,
                registered_subject=self.registered_subject,
                crf_entry__app_label='edc_testing').count(), 3)

    def test_creates_meta_data3(self):
        """ """
        self.assertEqual(CrfMetaData.objects.filter(registered_subject=self.registered_subject).count(), 0)
        test_visit = TestVisit.objects.create(
            appointment=self.appointment,
            report_datetime=timezone.now())
        self.assertEqual(CrfMetaData.objects.filter(registered_subject=self.registered_subject).count(), 3)
        TestScheduledModel1.objects.create(test_visit=test_visit)
        self.assertEqual(CrfMetaData.objects.filter(
            entry_status=KEYED, registered_subject=self.registered_subject).count(), 1)
        self.assertEqual(CrfMetaData.objects.filter(
            entry_status=UNKEYED, registered_subject=self.registered_subject).count(), 2)

    def test_creates_meta_data4(self):
        """Meta data is deleted when visit tracking form is deleted."""
        test_visit = TestVisit.objects.create(
            appointment=self.appointment,
            report_datetime=timezone.now())
        self.assertEqual(RequisitionMetaData.objects.filter(registered_subject=self.registered_subject).count(), 3)
        self.assertEqual(CrfMetaData.objects.filter(registered_subject=self.registered_subject).count(), 3)
        test_visit.delete()
        self.assertEqual(CrfMetaData.objects.filter(registered_subject=self.registered_subject).count(), 0)
        self.assertEqual(RequisitionMetaData.objects.filter(registered_subject=self.registered_subject).count(), 0)

    def test_creates_meta_data5(self):
        """Meta data is not created if visit reason is missed. See 'skip_create_visit_reasons class' attribute"""
        TestVisit.objects.create(
            appointment=self.appointment,
            report_datetime=timezone.now(),
            reason=MISSED_VISIT)
        self.assertEqual(
            CrfMetaData.objects.filter(registered_subject=self.registered_subject).count(), 0)

    def test_updates_meta_data4(self):
        """Meta data instance linked to the model is updated if model is entered."""
        self.test_visit = TestVisit.objects.create(
            appointment=self.appointment,
            report_datetime=timezone.now())
        TestScheduledModel1Factory(test_visit=self.test_visit)
        self.assertEqual(CrfMetaData.objects.filter(
            entry_status=KEYED,
            registered_subject=self.registered_subject,
            crf_entry__app_label='edc_testing',
            crf_entry__model_name='testscheduledmodel1').count(), 1)

    def test_updates_meta_data5(self):
        """Meta data instance linked to the model is updated if model is entered and then updated."""
        self.test_visit = TestVisit.objects.create(
            appointment=self.appointment,
            report_datetime=timezone.now())
        obj = TestScheduledModel1Factory(test_visit=self.test_visit)
        obj.save()
        self.assertEqual(CrfMetaData.objects.filter(
            entry_status=KEYED,
            registered_subject=self.registered_subject,
            crf_entry__app_label='edc_testing',
            crf_entry__model_name='testscheduledmodel1').count(), 1)

    def test_updates_meta_data6(self):
        """Meta data instance linked to the model is updated if model is deleted."""
        self.test_visit = TestVisit.objects.create(
            appointment=self.appointment,
            report_datetime=timezone.now())
        self.assertEqual(CrfMetaData.objects.filter(
            entry_status=UNKEYED,
            registered_subject=self.registered_subject,
            crf_entry__app_label='edc_testing',
            crf_entry__model_name='testscheduledmodel1').count(), 1)
        obj = TestScheduledModel1Factory(test_visit=self.test_visit)
        self.assertEqual(CrfMetaData.objects.filter(
            entry_status=KEYED,
            registered_subject=self.registered_subject,
            crf_entry__app_label='edc_testing',
            crf_entry__model_name='testscheduledmodel1').count(), 1)
        obj.delete()
        self.assertEqual(CrfMetaData.objects.filter(
            entry_status=UNKEYED,
            registered_subject=self.registered_subject,
            crf_entry__app_label='edc_testing',
            crf_entry__model_name='testscheduledmodel1').count(), 1)

    def test_updates_meta_data7(self):
        """Meta data instance linked to the model is created if missing, knows model is KEYED."""
        self.test_visit = TestVisit.objects.create(
            appointment=self.appointment,
            report_datetime=timezone.now())
        CrfMetaData.objects.filter(
            entry_status=UNKEYED,
            registered_subject=self.registered_subject,
            crf_entry__model_name='testscheduledmodel1').delete()
        TestScheduledModel1Factory(test_visit=self.test_visit)
        self.assertEqual(CrfMetaData.objects.filter(
            entry_status=KEYED,
            registered_subject=self.registered_subject,
            crf_entry__app_label='edc_testing',
            crf_entry__model_name='testscheduledmodel1').count(), 1)

    def test_requisition_meta_data1(self):
        """"""
        self.test_visit = TestVisit.objects.create(
            appointment=self.appointment,
            report_datetime=timezone.now())
        self.assertEqual(
            RequisitionMetaData.objects.filter(registered_subject=self.registered_subject).count(), 3)
        requisition_panels = [
            requisition_meta_data.lab_entry.requisition_panel
            for requisition_meta_data in RequisitionMetaData.objects.filter(
                registered_subject=self.registered_subject)]
        for requisition_panel in requisition_panels:
            panel = TestPanel.objects.get(name=requisition_panel.name)
            aliquot_type = TestAliquotType.objects.get(alpha_code=requisition_panel.aliquot_type_alpha_code)
            obj = TestRequisitionFactory(
                study_site=self.study_site,
                test_visit=self.test_visit,
                panel=panel,
                aliquot_type=aliquot_type,
                requisition_identifier='WJ0000003')
            obj.save()
            self.assertEqual(RequisitionMetaData.objects.filter(
                entry_status=KEYED,
                registered_subject=self.registered_subject,
                lab_entry__app_label='edc_testing',
                lab_entry__model_name='testrequisition',
                lab_entry__requisition_panel__name=panel.name).count(), 1)
            self.assertEqual(RequisitionMetaData.objects.filter(
                entry_status=UNKEYED,
                registered_subject=self.registered_subject).count(), 2)
            self.assertEqual(RequisitionMetaData.objects.filter(
                entry_status=KEYED,
                registered_subject=self.registered_subject).count(), 1)
            obj.delete()
            self.assertEqual(RequisitionMetaData.objects.filter(
                entry_status=UNKEYED,
                registered_subject=self.registered_subject,
                lab_entry__app_label='edc_testing',
                lab_entry__model_name='testrequisition',
                lab_entry__requisition_panel__name=panel.name).count(), 1)
            self.assertEqual(RequisitionMetaData.objects.filter(
                entry_status=UNKEYED,
                registered_subject=self.registered_subject).count(), 3)

    def test_new_meta_data_never_keyed(self):
        """Meta data instance linked to the model is updated if model is deleted."""
        self.assertTrue(TestScheduledModel1.objects.all().count() == 0)
        self.assertEqual(CrfMetaData.objects.filter(registered_subject=self.registered_subject).count(), 0)
        self.test_visit = TestVisit.objects.create(
            appointment=self.appointment,
            report_datetime=timezone.now())
        self.assertEqual(CrfMetaData.objects.filter(
            entry_status=KEYED, registered_subject=self.registered_subject).count(), 0)

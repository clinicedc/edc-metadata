from __future__ import print_function

from edc.entry_meta_data.models import CrfMetaData, RequisitionMetaData
from edc.entry_meta_data.tests.base_test_entry_meta_data import BaseTestEntryMetaData
from edc.subject.entry.models import LabEntry
from edc_testing.models import TestPanel, TestAliquotType, TestScheduledModel1
from edc_testing.tests.factories import TestScheduledModel1Factory, TestRequisitionFactory
from edc_constants.constants import KEYED, UNKEYED, MISSED_VISIT
from edc_visit_tracking.tests.factories import TestVisitFactory


class TestsEntryMetaData(BaseTestEntryMetaData):

    app_label = 'testing'
    consent_catalogue_name = 'v1'

    def test_creates_meta_data1(self):
        """No meta data if visit tracking form is not entered."""
        self.assertEqual(CrfMetaData.objects.filter(
            registered_subject=self.registered_subject).count(), 0)

    def test_creates_requisition_meta_data(self):
        """Meta data is created when visit tracking form is added, each instance set to NEW."""
        self.assertTrue(LabEntry.objects.all().count() > 0)
        self.test_visit = TestVisitFactory(appointment=self.appointment)
        self.assertEqual(RequisitionMetaData.objects.filter(registered_subject=self.registered_subject).count(), 3)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=UNKEYED, registered_subject=self.registered_subject).count(), 3)

    def test_creates_requisition_meta_data2(self):
        """Meta data is unchanged if you re-save visit."""
        self.assertTrue(LabEntry.objects.all().count() > 0)
        self.test_visit = TestVisitFactory(appointment=self.appointment)
        self.test_visit.save()
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=UNKEYED, registered_subject=self.registered_subject).count(), 3)

    def test_updates_requisition_meta_data(self):
        """Asserts metadata is updated if requisition model is keyed."""
        self.assertEquals(RequisitionMetaData.objects.all().count(), 0)
        self.test_visit = TestVisitFactory(appointment=self.appointment)
        self.assertEquals(RequisitionMetaData.objects.all().count(), 3)
        self.assertEqual([obj.entry_status for obj in RequisitionMetaData.objects.all()], [UNKEYED, UNKEYED, UNKEYED])
        self.assertEquals(RequisitionMetaData.objects.filter(entry_status=UNKEYED).count(), 3)
        requisition_panel = RequisitionMetaData.objects.filter(registered_subject=self.registered_subject)[0].lab_entry.requisition_panel
        panel = TestPanel.objects.get(name=requisition_panel.name)
        aliquot_type = TestAliquotType.objects.get(alpha_code=requisition_panel.aliquot_type_alpha_code)
        self.assertEqual(RequisitionMetaData.objects.filter(
            entry_status=UNKEYED,
            registered_subject=self.registered_subject,
            lab_entry__app_label='testing',
            lab_entry__model_name='testrequisition',
            lab_entry__requisition_panel__name=panel.name).count(), 1)
        obj = TestRequisitionFactory(site=self.study_site, test_visit=self.test_visit, panel=panel, aliquot_type=aliquot_type, requisition_identifier='WJ000001')

        self.assertEqual(RequisitionMetaData.objects.filter(
            entry_status=KEYED,
            registered_subject=self.registered_subject,
            lab_entry__app_label='testing',
            lab_entry__model_name='testrequisition',
            lab_entry__requisition_panel__name=obj.panel.name).count(), 1)

    def test_updates_requisition_meta_data2(self):
        """Meta data is set to KEYED and is unchanged if you re-save requisition or re-save visit."""
        self.test_visit = TestVisitFactory(appointment=self.appointment)
        requisition_panel = RequisitionMetaData.objects.filter(registered_subject=self.registered_subject)[0].lab_entry.requisition_panel
        panel = TestPanel.objects.get(name=requisition_panel.name)
        aliquot_type = TestAliquotType.objects.get(alpha_code=requisition_panel.aliquot_type_alpha_code)
        obj = TestRequisitionFactory(site=self.study_site, test_visit=self.test_visit, panel=panel, aliquot_type=aliquot_type, requisition_identifier='WJ0000002')
        obj.save()
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=KEYED,
                                                            registered_subject=self.registered_subject,
                                                            lab_entry__app_label='testing',
                                                            lab_entry__model_name='testrequisition',
                                                            lab_entry__requisition_panel__name=obj.panel.name).count(), 1)
        self.test_visit.save()
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=KEYED,
                                                            registered_subject=self.registered_subject,
                                                            lab_entry__app_label='testing',
                                                            lab_entry__model_name='testrequisition',
                                                            lab_entry__requisition_panel__name=obj.panel.name).count(), 1)
        obj.save()
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=KEYED,
                                                            registered_subject=self.registered_subject,
                                                            lab_entry__app_label='testing',
                                                            lab_entry__model_name='testrequisition',
                                                            lab_entry__requisition_panel__name=obj.panel.name).count(), 1)

    def test_updates_requisition_meta_data3(self):
        """Meta data is set to KEYED and is unchanged if you re-save requisition or re-save visit."""
        self.test_visit = TestVisitFactory(appointment=self.appointment)
        self.assertEqual(RequisitionMetaData.objects.filter(registered_subject=self.registered_subject).count(), 3)
        requisition_panel = RequisitionMetaData.objects.filter(registered_subject=self.registered_subject)[0].lab_entry.requisition_panel
        panel = TestPanel.objects.get(name=requisition_panel.name)
        aliquot_type = TestAliquotType.objects.get(alpha_code=requisition_panel.aliquot_type_alpha_code)
        obj = TestRequisitionFactory(site=self.study_site, test_visit=self.test_visit, panel=panel, aliquot_type=aliquot_type, requisition_identifier='WJ0000003')
        obj.save()
        self.assertEqual(RequisitionMetaData.objects.filter(
            entry_status=KEYED,
            registered_subject=self.registered_subject,
            lab_entry__app_label='testing',
            lab_entry__model_name='testrequisition',
            lab_entry__requisition_panel__name=panel.name).count(), 1)
        obj.delete()
        self.assertEqual(RequisitionMetaData.objects.filter(
            entry_status=UNKEYED,
            registered_subject=self.registered_subject,
            lab_entry__app_label='testing',
            lab_entry__model_name='testrequisition',
            lab_entry__requisition_panel__name=panel.name).count(), 1)

    def test_creates_meta_data2(self):
        """Meta data is created when visit tracking form is added, each instance set to NEW."""
        self.test_visit = TestVisitFactory(appointment=self.appointment)
        self.assertEqual(CrfMetaData.objects.filter(entry_status=UNKEYED, registered_subject=self.registered_subject).count(), 3)

    def test_creates_meta_data3(self):
        """ """
        self.assertEqual(CrfMetaData.objects.filter(registered_subject=self.registered_subject).count(), 0)
        test_visit = TestVisitFactory(appointment=self.appointment)
        self.assertEqual(CrfMetaData.objects.filter(registered_subject=self.registered_subject).count(), 3)
        TestScheduledModel1Factory(test_visit=test_visit)
        self.assertEqual(CrfMetaData.objects.filter(entry_status=KEYED, registered_subject=self.registered_subject).count(), 1)
        self.assertEqual(CrfMetaData.objects.filter(entry_status=UNKEYED, registered_subject=self.registered_subject).count(), 2)

    def test_creates_meta_data4(self):
        """Meta data is deleted when visit tracking form is deleted."""
        self.test_visit = TestVisitFactory(appointment=self.appointment)
        self.assertEqual(RequisitionMetaData.objects.filter(registered_subject=self.registered_subject).count(), 3)
        self.assertEqual(CrfMetaData.objects.filter(registered_subject=self.registered_subject).count(), 3)
        self.test_visit.delete()
        self.assertEqual(CrfMetaData.objects.filter(registered_subject=self.registered_subject).count(), 0)
        self.assertEqual(RequisitionMetaData.objects.filter(registered_subject=self.registered_subject).count(), 0)

    def test_creates_meta_data5(self):
        """Meta data is not created if visit reason is missed. See 'skip_create_visit_reasons class' attribute"""
        self.test_visit = TestVisitFactory(appointment=self.appointment, reason=MISSED_VISIT)
        self.assertEqual(CrfMetaData.objects.filter(registered_subject=self.registered_subject).count(), 0)

    def test_updates_meta_data4(self):
        """Meta data instance linked to the model is updated if model is entered."""
        self.test_visit = TestVisitFactory(appointment=self.appointment)
        TestScheduledModel1Factory(test_visit=self.test_visit)
        self.assertEqual(CrfMetaData.objects.filter(entry_status=KEYED, registered_subject=self.registered_subject, entry__content_type_map__model='testscheduledmodel1').count(), 1)

    def test_updates_meta_data5(self):
        """Meta data instance linked to the model is updated if model is entered and then updated."""
        self.test_visit = TestVisitFactory(appointment=self.appointment)
        obj = TestScheduledModel1Factory(test_visit=self.test_visit)
        obj.save()
        self.assertEqual(CrfMetaData.objects.filter(entry_status=KEYED,
                                                               registered_subject=self.registered_subject,
                                                               entry__app_label='testing',
                                                               entry__model_name='testscheduledmodel1').count(), 1)

    def test_updates_meta_data6(self):
        """Meta data instance linked to the model is updated if model is deleted."""
        self.test_visit = TestVisitFactory(appointment=self.appointment)
        obj = TestScheduledModel1Factory(test_visit=self.test_visit)
        obj.delete()
        self.assertEqual(CrfMetaData.objects.filter(entry_status=UNKEYED, registered_subject=self.registered_subject, entry__content_type_map__model='testscheduledmodel1').count(), 1)

    def test_updates_meta_data7(self):
        """Meta data instance linked to the model is created if missing, knows model is KEYED."""
        self.test_visit = TestVisitFactory(appointment=self.appointment)
        CrfMetaData.objects.filter(entry_status=UNKEYED, registered_subject=self.registered_subject, entry__model_name='testscheduledmodel1').delete()
        TestScheduledModel1Factory(test_visit=self.test_visit)
        self.assertEqual(CrfMetaData.objects.filter(entry_status=KEYED, registered_subject=self.registered_subject, entry__model_name='testscheduledmodel1').count(), 1)

    def test_requisition_meta_data1(self):
        """"""
        self.test_visit = TestVisitFactory(appointment=self.appointment)
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
                entry_status=KEYED,
                registered_subject=self.registered_subject,
                lab_entry__app_label='testing',
                lab_entry__model_name='testrequisition',
                lab_entry__requisition_panel__name=panel.name).count(), 1)
            self.assertEqual(RequisitionMetaData.objects.filter(entry_status=UNKEYED,
                                                                registered_subject=self.registered_subject).count(), 2)
            self.assertEqual(RequisitionMetaData.objects.filter(entry_status=KEYED,
                                                                registered_subject=self.registered_subject).count(), 1)
            obj.delete()
            self.assertEqual(RequisitionMetaData.objects.filter(
                entry_status=UNKEYED,
                registered_subject=self.registered_subject,
                lab_entry__app_label='testing',
                lab_entry__model_name='testrequisition',
                lab_entry__requisition_panel__name=panel.name).count(), 1)
            self.assertEqual(RequisitionMetaData.objects.filter(entry_status=UNKEYED,
                                                                registered_subject=self.registered_subject).count(), 3)

    def test_new_meta_data_never_keyed(self):
        """Meta data instance linked to the model is updated if model is deleted."""
        self.assertTrue(TestScheduledModel1.objects.all().count() == 0)
        self.assertEqual(CrfMetaData.objects.filter(registered_subject=self.registered_subject).count(), 0)
        self.test_visit = TestVisitFactory(appointment=self.appointment)
        self.assertEqual(CrfMetaData.objects.filter(entry_status=KEYED, registered_subject=self.registered_subject).count(), 0)

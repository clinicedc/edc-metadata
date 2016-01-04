from __future__ import print_function

from django.utils import timezone

from edc_constants.constants import SCHEDULED, NOT_REQUIRED, OFF_STUDY, REQUIRED
from edc_meta_data.models import CrfMetaData, CrfEntry
from edc_testing.models.test_visit import TestVisit

from .base_test_case import BaseTestCase


class TestMetaDataMixin(BaseTestCase):

    def test_changes_to_an_unscheduled_visit(self):
        """Assert changing to unscheduled visit sets all forms to not required."""
        visit = TestVisit.objects.create(
            appointment=self.appointment,
            report_datetime=timezone.now(),
            reason=SCHEDULED)
        self.assertEqual(
            CrfMetaData.objects.filter(
                registered_subject=self.appointment.registered_subject,
                entry_status=REQUIRED).count(), 3)
        visit.change_to_unscheduled_visit(self.appointment)
        self.assertEqual(
            [obj.entry_status for obj in CrfMetaData.objects.filter(
                registered_subject=self.appointment.registered_subject)],
            [NOT_REQUIRED, NOT_REQUIRED, NOT_REQUIRED])

    def test_change_to_off_study(self):
        """Assert changing to death visit adds off study and sets all others to not required."""
        visit = TestVisit.objects.create(
            appointment=self.appointment,
            report_datetime=timezone.now(),
            reason=OFF_STUDY)
        self.assertEqual(
            CrfMetaData.objects.filter(
                registered_subject=self.appointment.registered_subject,
                entry_status=REQUIRED).count(), 3)
        visit.change_to_off_study_visit(
            self.appointment, 'edc_testing', 'testoffstudy')
        self.assertEqual(
            [obj.entry_status for obj in CrfMetaData.objects.filter(
                registered_subject=self.appointment.registered_subject)],
            [REQUIRED, NOT_REQUIRED, NOT_REQUIRED, NOT_REQUIRED])

    def test_change_to_off_study_creates_entry(self):
        """Assert changing to off study creates an Entry for off study."""
        visit = TestVisit.objects.create(
            appointment=self.appointment,
            report_datetime=timezone.now(),
            reason=OFF_STUDY)
        visit.change_to_off_study_visit(
            self.appointment, 'edc_testing', 'testoffstudy')
        crf_entry = CrfEntry.objects.get(
            content_type_map__app_label='edc_testing',
            content_type_map__module_name='testoffstudy')
        self.assertEqual(
            CrfMetaData.objects.filter(crf_entry=crf_entry).count(), 1)

    def test_change_to_death(self):
        """Assert changing to death visit adds offstudy and death and sets all others to not required."""
        visit = TestVisit.objects.create(
            appointment=self.appointment,
            report_datetime=timezone.now(),
            reason=OFF_STUDY)
        visit.change_to_death_visit(
            self.appointment, 'edc_testing', 'testoffstudy', 'testdeathreport')
        self.assertEqual(
            [obj.entry_status for obj in CrfMetaData.objects.filter(
                registered_subject=self.appointment.registered_subject)],
            [REQUIRED, REQUIRED, NOT_REQUIRED, NOT_REQUIRED, NOT_REQUIRED])

    def test_change_to_death_creates_entry(self):
        """Assert changing to off study creates an Entry for death report."""
        visit = TestVisit.objects.create(
            appointment=self.appointment,
            report_datetime=timezone.now(),
            reason=OFF_STUDY)
        visit.change_to_death_visit(
            self.appointment, 'edc_testing', 'testoffstudy', 'testdeathreport')
        crf_entry = CrfEntry.objects.get(
            content_type_map__app_label='edc_testing',
            content_type_map__module_name='testdeathreport')
        self.assertEqual(
            CrfMetaData.objects.filter(crf_entry=crf_entry).count(), 1)

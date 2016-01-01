from __future__ import print_function

from django.db import models
from django.utils import timezone

from edc_constants.constants import SCHEDULED, NOT_REQUIRED, OFF_STUDY, REQUIRED
from edc_meta_data.managers import CrfMetaDataManager
from edc_meta_data.models import CrfMetaData, CrfEntry
from edc_testing.models.test_visit import TestVisit

from .base_test_entry_meta_data import BaseTestEntryMetaData


class DeathReport(models.Model):

    test_visit = models.OneToOneField(TestVisit)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date",
        default=timezone.now)

    entry_meta_data_manager = CrfMetaDataManager(TestVisit)

    class Meta:
        app_label = "testing"


class TestsEntryMetaData(BaseTestEntryMetaData):

    app_label = 'edc_testing'
    consent_catalogue_name = 'v1'

    def test_changes_to_an_unscheduled_visit(self):
        """Assert changing to unscheduled visit sets all forms to not required."""
        visit = TestVisit.objects.create(
            appointment=self.appointment,
            report_datetime=timezone.now(),
            reason=SCHEDULED)
        visit.change_to_unscheduled_visit(self.appointment)
        self.assertEqual(
            [obj.entry_status for obj in CrfMetaData.objects.all()],
            [NOT_REQUIRED, NOT_REQUIRED, NOT_REQUIRED])

    def test_change_to_off_study(self):
        """Assert changing to death visit adds off study and sets all others to not required."""
        visit = TestVisit.objects.create(
            appointment=self.appointment,
            report_datetime=timezone.now(),
            reason=OFF_STUDY)
        visit.change_to_off_study_visit(
            self.appointment, 'edc_testing', 'testoffstudy')
        self.assertEqual(
            [obj.entry_status for obj in CrfMetaData.objects.all()],
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
            self.appointment, 'edc_testing', 'testoffstudy', 'deathreport')
        self.assertEqual(
            [obj.entry_status for obj in CrfMetaData.objects.all()],
            [REQUIRED, REQUIRED, NOT_REQUIRED, NOT_REQUIRED, NOT_REQUIRED])

    def test_change_to_death_creates_entry(self):
        """Assert changing to off study creates an Entry for death report."""
        visit = TestVisit.objects.create(
            appointment=self.appointment,
            report_datetime=timezone.now(),
            reason=OFF_STUDY)
        visit.change_to_death_visit(
            self.appointment, 'edc_testing', 'testoffstudy', 'deathreport')
        crf_entry = CrfEntry.objects.get(
            content_type_map__app_label='edc_testing',
            content_type_map__module_name='deathreport')
        self.assertEqual(
            CrfMetaData.objects.filter(crf_entry=crf_entry).count(), 1)

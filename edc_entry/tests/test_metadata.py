from django.db import models
from django.test.testcases import TransactionTestCase
from django.contrib.contenttypes.models import ContentType

from edc_entry.models import Entry
from edc_visit_schedule.models import VisitDefinition
from edc_entry.managers.entry_meta_data_manager import EntryMetaDataManager
from edc_entry.models.scheduled_entry_meta_data import ScheduledEntryMetaData
from django.utils import timezone


class VisitModel(models.Model):

    appointment = models.CharField(max_length=25)

    report_datetime = models.DateTimeField(
        default=timezone.now)

    class Meta:
        app_label = 'edc_entry'


class TestModel(models.Model):

    field1 = models.CharField(max_length=10)

    entry_meta_data_manager = EntryMetaDataManager(VisitModel)

    class Meta:
        app_label = 'edc_entry'


class TestMetadata(TransactionTestCase):

    def setUp(self):
        self.visit_definition = VisitDefinition(
            code='1000', title='First visit')
        self.visit_definition.save()
        test_model = ContentType.objects.get(app_label="edc_entry", model="testmodel")
        self.entry = Entry(
            content_type=test_model,
            entry_order=10,
            visit_definition=self.visit_definition
        )
        self.entry.save()

    def test_save_creates_meta(self):
        self.assertFalse(ScheduledEntryMetaData.objects.filter(entry=self.entry).exists())
        test_model = TestModel(field1='erik')
        test_model.save()
        self.assertTrue(ScheduledEntryMetaData.objects.filter(entry=self.entry).exists())

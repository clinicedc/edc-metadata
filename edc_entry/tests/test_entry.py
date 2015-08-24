from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.test import TransactionTestCase

from edc_entry.models import Entry
from django.core.exceptions import ImproperlyConfigured
from edc_visit_schedule.models import VisitDefinition
from django.db.utils import IntegrityError


class DummyManager(models.Manager):
    pass


class TestModel(models.Model):

    field1 = models.CharField(max_length=10)

    entry_meta_data_manager = DummyManager()

    class Meta:
        app_label = 'edc_entry'


class TestModelVerbose(models.Model):

    field1 = models.CharField(max_length=10)

    entry_meta_data_manager = DummyManager()

    class Meta:
        app_label = 'edc_entry'
        verbose_name = 'Test Model'


class TestModelNoManager(models.Model):

    field1 = models.CharField(max_length=10)

    class Meta:
        app_label = 'edc_entry'


class TestEntry(TransactionTestCase):

    def setUp(self):
        self.visit_definition = VisitDefinition(code='1000', title='First visit')
        self.visit_definition.save()
        test_model = ContentType.objects.get(app_label="edc_entry", model="testmodel")
        self.entry = Entry(
            content_type=test_model,
            entry_order=10,
            visit_definition=self.visit_definition
        )
        self.entry.save()

    def test_entry_name(self):
        self.assertEqual(self.entry.content_type.name, 'test model')
        test_model_verbose = ContentType.objects.get(app_label="edc_entry", model="testmodelverbose")
        entry = Entry(
            content_type=test_model_verbose,
            entry_order=20,
            visit_definition=self.visit_definition,
        )
        entry.save()
        self.assertEqual(entry.content_type.name, 'Test Model')

    def test_entry_app_label_model(self):
        self.assertEqual(self.entry.content_type.name, 'test model')
        self.assertEqual(self.entry.app_label, 'edc_entry')
        self.assertEqual(self.entry.model, 'testmodel')
        self.assertEqual(self.entry.name, 'test model')

    def test_entry_resync(self):
        """Assert resyncs if method is called."""
        name = self.entry.name
        self.entry.name = 'ERIK'
        self.entry.content_type.id = 0
        self.entry.resync_contenttype()
        self.assertEqual(self.entry.name, name)

    def test_entry_resync_on_getmodel(self):
        """Asserts resyncs if model_class() is called."""
        name = self.entry.name
        self.entry.name = 'ERIK'
        self.entry.content_type.id = 0
        model = self.entry.entry_form_model
        self.assertEqual(self.entry.name, name)
        self.assertEqual(self.entry.name, model._meta.verbose_name)

    def test_no_manager_raises(self):
        model = ContentType.objects.get(app_label="edc_entry", model="testmodelnomanager")
        entry = Entry(
            content_type=model,
            entry_order=20,
            visit_definition=self.visit_definition,
        )
        self.assertRaises(ImproperlyConfigured, entry.save)

    def test_updates_visit_code(self):
        model = ContentType.objects.get(app_label="edc_entry", model="testmodelverbose")
        entry = Entry(
            content_type=model,
            entry_order=20,
            visit_definition=self.visit_definition,
        )
        entry.save()
        self.assertEqual(self.visit_definition.code, entry.visit_code)

    def test_constraint1(self):
        model = ContentType.objects.get(app_label="edc_entry", model="testmodelverbose")
        entry = Entry(
            content_type=model,
            entry_order=20,
            visit_definition=self.visit_definition,
        )
        entry.save()
        entry = Entry(
            content_type=model,
            entry_order=30,
            visit_definition=self.visit_definition,
        )
        self.assertRaises(IntegrityError, entry.save)

    def test_constraint2(self):
        model = ContentType.objects.get(app_label="edc_entry", model="testmodelverbose")
        entry = Entry(
            content_type=model,
            entry_order=10,
            visit_definition=self.visit_definition,
        )
        self.assertRaises(IntegrityError, entry.save)

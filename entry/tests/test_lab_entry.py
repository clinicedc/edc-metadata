from django.test import TestCase

from ..models.lab_entry import LabEntry


class LabEntryTests(TestCase):

    def test_entry_status_is_assigned_not_required(self):
        """ doc """
        lab_entry = LabEntry(default_entry_status='NOT_REQUIRED')
        self.assertFalse(lab_entry.is_required())
        self.assertTrue(lab_entry.is_not_required())

    def test_entry_status_is_anything_but_not_required(self):
        """ doc """
        lab_entry = LabEntry(default_entry_status='NEW')
        self.assertTrue(lab_entry.is_required())
        self.assertFalse(lab_entry.is_not_required())

        lab_entry.default_entry_status = 'KEYED'
        self.assertTrue(lab_entry.is_required())
        self.assertFalse(lab_entry.is_not_required())


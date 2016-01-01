from django.core.exceptions import ImproperlyConfigured
from django.db import models

from edc_constants.constants import REQUIRED, NOT_REQUIRED, KEYED
from edc_content_type_map.models import ContentTypeMap

from .crf_entry import CrfEntry
from .crf_meta_data import CrfMetaData
from .lab_entry import LabEntry
from .requisition_meta_data import RequisitionMetaData
from .requisition_panel import RequisitionPanel


class CrfMetaDataMixin(models.Model):

    """Class to manipulate meta data for CRFs and requisitions."""

    def custom_post_update_crf_meta_data(self):
        raise ImproperlyConfigured(
            'To use the MetaDataMixin override method \'custom_post_update_crf_meta_data\'')

    def crf_is_required(self, appointment, app_label, model_name,
                        message=None, create=None):
        """Saves the CRF status as REQUIRED."""
        self._change_crf_status(
            REQUIRED, appointment, app_label, model_name, message, create)

    def crf_is_not_required(self, appointment, app_label, model_name, message=None):
        """Saves the CRF status as NOT REQUIRED."""
        self._change_crf_status(
            NOT_REQUIRED, appointment, app_label, model_name, message)

    def requisition_is_required(self, appointment, app_label, model_name, panel_name,
                                message=None, create=None):
        self._change_requisition_status(
            REQUIRED, appointment, app_label, model_name, panel_name, message, create)

    def requisition_is_not_required(self, appointment, app_label, model_name, panel_name,
                                    message=None):
        self._change_requisition_status(
            NOT_REQUIRED, appointment, app_label, model_name, panel_name, message)

    def change_to_off_study_visit(self, appointment, off_study_app_label,
                                  off_study_model_name, message=None):
        """Changes the meta data so that only the off study form is required.

        * if the off study form does not exist it will be created.
        * if a form is already KEYED it will not be changed.
        """
        self._change_all_to_not_required(appointment)
        self.crf_is_required(appointment, off_study_app_label, off_study_model_name,
                             message, create=True)

    def change_to_death_visit(self, appointment, app_label, off_study_model_name,
                              death_model_name, message=None):
        """Changes the meta data so that only the death and
        off study forms are required.

        If either form does not exist they will be created."""
        self.change_to_off_study_visit(appointment, app_label, off_study_model_name, message)
        self.crf_is_required(appointment, app_label, death_model_name, message, create=True)

    def change_to_unscheduled_visit(self, appointment, message=None):
        """Changes all meta data to not required."""
        self._change_all_to_not_required(appointment)

    def _change_all_to_not_required(self, appointment):
        """Changes all meta data to not required."""
        base_appointment = self.get_base_appointment(appointment)
        CrfMetaData.objects.filter(
            appointment=base_appointment,
            registered_subject=appointment.registered_subject).exclude(
                entry_status__in=[NOT_REQUIRED, KEYED]).update(
                entry_status=NOT_REQUIRED)
        RequisitionMetaData.objects.filter(
            appointment=base_appointment,
            registered_subject=appointment.registered_subject).exclude(
                entry_status__in=[NOT_REQUIRED, KEYED]).update(
                entry_status=NOT_REQUIRED)

    def _change_crf_status(self, entry_status, appointment, app_label, model_name,
                           message=None, create=None):
        """Changes a CRF's entry status.

        Raises an error if the CRF does not exist unless 'create'
        is True. Except for OFF STUDY there should not be a need
        to create a CRF."""
        try:
            base_appointment = self.get_base_appointment(appointment)
            crf_meta_data = CrfMetaData.objects.get(
                crf_entry__app_label=app_label,
                crf_entry__model_name=model_name,
                appointment=base_appointment
            )
        except CrfMetaData.DoesNotExist as e:
            if create:
                crf_meta_data = self._create_crf(appointment, app_label, model_name)
            else:
                message = message or ''
                raise CrfMetaData.DoesNotExist(
                    '{} {}.{} {}'.format(str(e), app_label, model_name, message))
        self._change_status(crf_meta_data, entry_status)

    def _change_requisition_status(
            self, entry_status, appointment, app_label, model_name, panel_name,
            message=None, create=None):
        """Changes a requisition's entry status.

        Raises an error if the requisition does not exist unless 'create' is True."""
        try:
            base_appointment = self.get_base_appointment(appointment)
            requisition_meta_data = RequisitionMetaData.objects.get(
                lab_entry__app_label=app_label,
                lab_entry__model_name=model_name,
                appointment=base_appointment,
                lab_entry__requisition_panel__name=panel_name
            )
        except RequisitionMetaData.DoesNotExist as e:
            if create:
                requisition_meta_data = self._create_crf(appointment, app_label, model_name)
            else:
                message = message or ''
                raise RequisitionMetaData.DoesNotExist(
                    '{} {}.{}.{} {}'.format(str(e), app_label, model_name, panel_name, message))
        self._change_status(requisition_meta_data, entry_status)

    def _change_status(self, meta_data, entry_status):
        """Changes the entry_status if not already set to the given value."""
        if meta_data.entry_status != entry_status:
            meta_data.entry_status = entry_status
            meta_data.save()

    def _create_crf(self, appointment, app_label, model_name):
        """Creates a form with entry status set to REQUIRED."""
        base_appointment = self.get_base_appointment(appointment)
        try:
            crf_entry = CrfEntry.objects.get(
                app_label=app_label,
                model_name=model_name,
                visit_definition=base_appointment.visit_definition)
        except CrfEntry.DoesNotExist:
            crf_entry = self._create_crf_entry(appointment, app_label, model_name, REQUIRED)
        crf_meta_data = CrfMetaData.objects.create(
            crf_entry=crf_entry,
            appointment=base_appointment,
            registered_subject=base_appointment.registered_subject,
            entry_status=REQUIRED)
        return crf_meta_data

    def _create_requisition(self, appointment, app_label, model_name, panel_name):
        """Creates a requisition with entry status set to REQUIRED."""
        base_appointment = self.get_base_appointment(appointment)
        requisition_panel = RequisitionPanel.objects.get(panel_name=panel_name)
        try:
            lab_entry = LabEntry.objects.get(
                model_name=model_name,
                requisition_panel=requisition_panel,
                visit_definition=base_appointment.visit_definition)
        except LabEntry.DoesNotExist:
            lab_entry = self._create_lab_entry(
                appointment, app_label, model_name, requisition_panel, REQUIRED)
        requisition_meta_data = RequisitionMetaData.objects.create(
            lab_entry=lab_entry,
            appointment=base_appointment,
            lab_entry__requisition_panel=requisition_panel)
        return requisition_meta_data

    def get_base_appointment(self, appointment):
        """Returns the base appointment (CODE.0) or the given appointment
        if it is the base.

        More than one appointments may span for a given visit code.
        The appointments are incremented using a decimal, e.g. 1000.0,
        1000.1, 1000.2 , etc. 1000.0 is the "base" appointment."""
        if appointment.visit_instance != '0':
            appointment = appointment.__class__.objects.get(
                registered_subject=appointment.registered_subject,
                visit_instance='0', visit_definition=appointment.visit_definition)
        return appointment

    def _create_crf_entry(self, appointment, app_label, model_name,
                          entry_status=None, entry_order=None):
        appointment = self.get_base_appointment(appointment)
        content_type_map = ContentTypeMap.objects.get(
            app_label=app_label,
            module_name=model_name.lower())
        return CrfEntry.objects.create(
            content_type_map=content_type_map,
            visit_definition=appointment.visit_definition,
            entry_order=entry_order or 0,
            app_label=app_label.lower(),
            model_name=model_name.lower(),
            default_entry_status=entry_status or NOT_REQUIRED,
            additional=True)

    def _create_lab_entry(self, appointment, app_label, model_name, requisition_panel,
                          entry_status=None, entry_order=None):
        appointment = self.get_base_appointment(appointment)
        return LabEntry.objects.create(
            app_label=app_label,
            model_name=model_name,
            requisition_panel=requisition_panel,
            visit_definition=appointment.visit_definition,
            entry_order=entry_order or 0,
            default_entry_status=entry_status or NOT_REQUIRED,
            additional=True)

    class Meta:
        abstract = True

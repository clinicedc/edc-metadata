from django.apps import apps as django_apps
from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from django.db.utils import IntegrityError

from edc_constants.constants import NO

from .constants import REQUIRED, NOT_REQUIRED, KEYED


class CrfMetaDataMixin:

    """Class for visit model to manipulate meta data after entry_meta_data_manager for CRFs and requisitions.

    For example:

        class SubjectVisit(CrfMetaDataMixin, VisitModelMixin, BaseUuidModel):

            class Meta:
                app_label = 'my_app'
    """

    @property
    def crf_meta_data_model(self):
        return django_apps.get_app_config('edc_meta_data').crf_meta_data_model

    @property
    def requisition_meta_data_model(self):
        return django_apps.get_app_config('edc_meta_data').requisition_meta_data_model

    def custom_post_update_crf_meta_data(self):
        return self

    def crf_is_required(self, appointment, app_label, model_name, create=None):
        """Sets the CRF status to REQUIRED."""
        return self.change_crf_status(
            REQUIRED, appointment, app_label, model_name, create)

    def crf_is_not_required(self, appointment, app_label, model_name, delete=None):
        """Sets the CRF status to NOT REQUIRED."""
        crf_meta_data = None
        if delete:
            try:
                obj = self.crf_meta_data_model.objects.get(
                    crf_entry__app_label=app_label,
                    crf_entry__model_name=model_name,
                    appointment=self.get_base_appointment(appointment),
                    entry_status__in=[REQUIRED, NOT_REQUIRED])
                obj.delete()
            except self.crf_meta_data_model.DoesNotExist:
                pass
        else:
            crf_meta_data = self.change_crf_status(
                NOT_REQUIRED, appointment, app_label, model_name)
        return crf_meta_data

    def requisition_is_required(self, appointment, app_label, model_name, panel_name, create=None):
        """Sets the Requisition status to REQUIRED."""
        self.change_requisition_status(
            REQUIRED, appointment, app_label, model_name, panel_name, create)

    def requisition_is_not_required(self, appointment, app_label, model_name, panel_name, delete=None):
        """Sets the Requisition status to NOT REQUIRED."""
        self.change_requisition_status(
            NOT_REQUIRED, appointment, app_label, model_name, panel_name)
        if delete:
            self.requisition_meta_data_model.objects.filter(
                lab_entry__app_label=app_label,
                lab_entry__model_name=model_name,
                appointment=self.get_base_appointment(appointment),
                lab_entry__requisition_panel__name=panel_name,
                entry_status__in=[REQUIRED, NOT_REQUIRED])

    def require_off_study_report(self):
        """Changes the meta data so that only the off study form is required.

        * if the off study form does not exist it will be created.
        * if a form is already KEYED it will not be changed.
        * if visit.require_crfs, then only the off study meta data is changed.
        """
        # TODO: get the off study model from the schedule
        # maybe find the model in a schedule and return the schedule.off_study_model

        app_label = None
        model_name = None

        if self.require_crfs == NO:
            self.change_all_to_not_required()
        self.crf_is_required(
            self.appointment, app_label, model_name, create=True)

    def require_death_report(self):
        """Changes the meta data so that only the death and
        off study forms are required, unless require_crfs is True."""

        # TODO: get the death report model from the schedule
        # maybe find the model in a schedule and return the schedule.death_report_model

        app_label = None
        model_name = None

        self.crf_is_required(
            self.appointment, app_label, model_name, create=True)

    def undo_require_off_study_report(self):
        """Revert off study CRF to not required.

        off_study_model attr is always set.
        """
        off_study_app_label = self.off_study_model._meta.app_label
        off_study_model_name = self.off_study_model._meta.model_name
        self.crf_is_not_required(
            self.appointment, off_study_app_label, off_study_model_name, delete=True)

    def undo_require_death_report(self):
        """Revert death report CRF to not required.

        death_report_model attr is NOT always set."""
        if self.death_report_model:
            app_label = self.death_report_model._meta.app_label
            death_model_name = self.death_report_model._meta.model_name
            self.crf_is_not_required(self.appointment, app_label, death_model_name, delete=True)

    def change_to_unscheduled_visit(self, appointment):
        """Changes all meta data to not required."""
        self.change_all_to_not_required()

    def change_all_to_not_required(self):
        """Changes all meta data to not required."""
        with transaction.atomic():
            base_appointment = self.get_base_appointment(self.appointment)
            self.crf_meta_data_model.objects.filter(
                appointment=base_appointment,
                registered_subject=self.appointment.registered_subject).exclude(
                    entry_status__in=[NOT_REQUIRED, KEYED]).exclude(
                        crf_entry__model_name=self.death_report_model._meta.model_name).update(
                    entry_status=NOT_REQUIRED)
            self.requisition_meta_data_model.objects.filter(
                appointment=base_appointment,
                registered_subject=self.appointment.registered_subject).exclude(
                    entry_status__in=[NOT_REQUIRED, KEYED]).update(
                    entry_status=NOT_REQUIRED)

    def change_crf_status(self, entry_status, appointment, app_label, model_name, create=None):
        """Toggles a CRF's entry status between REQUIRED / NOT REQUIRED."""
        crf_meta_data = None
        if entry_status in [REQUIRED, NOT_REQUIRED]:
            with transaction.atomic():
                try:
                    crf_meta_data = self.crf_meta_data_model.objects.get(
                        crf_entry__app_label=app_label,
                        crf_entry__model_name=model_name,
                        appointment=self.get_base_appointment(appointment),
                        entry_status__in=[x for x in [REQUIRED, NOT_REQUIRED] if x != entry_status])
                    crf_meta_data.entry_status = entry_status
                    crf_meta_data.save()
                except self.crf_meta_data_model.DoesNotExist:
                    if create:
                        crf_meta_data = self.create_crf_meta_data(
                            appointment, app_label, model_name, entry_status)
        return crf_meta_data

    def change_requisition_status(
            self, entry_status, appointment, app_label, model_name, panel_name, create=None):
        """Toggles a Requisition's entry status between REQUIRED / NOT REQUIRED."""
        if entry_status in [REQUIRED, NOT_REQUIRED]:
            try:
                requisition_meta_data = self.requisition_meta_data_model.objects.get(
                    lab_entry__app_label=app_label,
                    lab_entry__model_name=model_name,
                    appointment=self.get_base_appointment(appointment),
                    lab_entry__requisition_panel__name=panel_name,
                    entry_status__in=[x for x in [REQUIRED, NOT_REQUIRED] if x != entry_status])
                requisition_meta_data.entry_status = entry_status
                requisition_meta_data.save()
            except self.requisition_meta_data_model.DoesNotExist:
                if create:
                    requisition_meta_data = self.create_requisition_meta_data(
                        appointment, app_label, model_name, panel_name,
                        entry_status)

    def create_crf_meta_data(self, appointment, app_label, model_name, entry_status):
        """Creates or updates existing CRF meta data to given entry_status."""
        crf_entry = None
        base_appointment = self.get_base_appointment(appointment)
        try:
            options = dict(
                app_label=app_label,
                model_name=model_name,
                visit_definition=base_appointment.visit_definition)
            crf_entry = CrfEntry.objects.get(**options)
        except CrfEntry.DoesNotExist:
            raise ImproperlyConfigured('Missing CrfEntry. Did you define a visit schedule? Using {}'.format(options))
        try:
            crf_meta_data = self.crf_meta_data_model.objects.create(
                crf_entry=crf_entry,
                appointment=base_appointment,
                registered_subject=base_appointment.registered_subject,
                entry_status=entry_status)
        except IntegrityError:
            crf_meta_data = None
        return crf_meta_data

    def create_requisition_meta_data(self, appointment, app_label, model_name, panel_name, entry_status):
        """Creates or updates existing requisition meta data to given entry_status."""
        lab_entry = None
        base_appointment = self.get_base_appointment(appointment)
        requisition_panel = RequisitionPanel.objects.get(panel_name=panel_name)
        try:
            lab_entry = LabEntry.objects.get(
                model_name=model_name,
                requisition_panel=requisition_panel,
                visit_definition=base_appointment.visit_definition)
        except LabEntry.DoesNotExist:
            raise ImproperlyConfigured('Lab Entry does not exist. Check AppConfiguration. Got {}.{} panel {}.'.format(
                app_label, model_name, requisition_panel.name))
        try:
            requisition_meta_data = self.requisition_meta_data_model.objects.create(
                lab_entry=lab_entry,
                appointment=base_appointment,
                lab_entry__requisition_panel=requisition_panel,
                entry_status=entry_status)
        except IntegrityError:
            requisition_meta_data = None
        return requisition_meta_data

    def get_base_appointment(self, appointment):
        """Returns the base appointment (CODE.0).

        More than one appointments may span for a given visit code.
        The appointments are incremented using a decimal, e.g. 1000.0,
        1000.1, 1000.2 , etc. 1000.0 is the "base" appointment."""
        if appointment.visit_instance != '0':
            appointment = appointment.__class__.objects.get(
                registered_subject=appointment.registered_subject,
                visit_instance='0', visit_definition=appointment.visit_definition)
        return appointment

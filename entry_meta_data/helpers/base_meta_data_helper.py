from datetime import date

from edc.constants import REQUIRED
from edc.core.bhp_common.utils import convert_from_camel
from edc.subject.visit_tracking.models import BaseVisitTracking
from edc.subject.visit_tracking.settings import VISIT_REASON_NO_FOLLOW_UP_CHOICES


class BaseMetaDataHelper(object):
    """ Base class for all classes that manage the entry state of additional, scheduled and unscheduled data."""
    def __init__(self, appointment, visit_instance=None, visit_model_attrname=None):
        self.appointment = appointment
        self.visit_model = self.appointment.visit_definition.visit_tracking_content_type_map.model_class()
        self.visit_model_attrname = visit_model_attrname or convert_from_camel(self.visit_model._meta.object_name)
        self.registered_subject = appointment.registered_subject
        self.visit_instance = visit_instance

    def __repr__(self):
        return 'BaseMetaDataHelper({0.instance!r})'.format(self)

    def __str__(self):
        return '({0.instance!r})'.format(self)

    @property
    def visit_model(self):
        return self._visit_model

    @visit_model.setter
    def visit_model(self, model_or_instance):
        try:
            if issubclass(model_or_instance, BaseVisitTracking):
                self._visit_model = model_or_instance
        except TypeError:
            self._visit_model = model_or_instance.__class__

    @property
    def visit_model_attrname(self):
        return self._visit_model_attrname

    @visit_model_attrname.setter
    def visit_model_attrname(self, attrname):
        self._visit_model_attrname = attrname or convert_from_camel(self.visit_model._meta.object_name)

    @property
    def visit_instance(self):
        return self._visit_instance

    @visit_instance.setter
    def visit_instance(self, model_or_instance):
        if isinstance(model_or_instance, BaseVisitTracking):
            self._visit_instance = model_or_instance
        else:
            self._visit_instance = self.visit_model.objects.get(appointment=self.appointment)

    @property
    def appointment_zero(self):
        if not self.appointment.visit_instance == '0':
            Appointment = self.appointment.__class__
            self._appointment_zero = Appointment.objects.get(
                registered_subject=self.appointment.registered_subject,
                visit_definition=self.appointment.visit_definition,
                visit_instance='0')
        else:
            self._appointment_zero = self.appointment
        return self._appointment_zero

    def show_scheduled_entries(self):
        # TODO: need to clean this up!
        if 'get_visit_reason_no_follow_up_choices' in dir(self.visit_instance):
            visit_reason_no_follow_up_choices = self.visit_instance.get_visit_reason_no_follow_up_choices()
        else:
            visit_reason_no_follow_up_choices = VISIT_REASON_NO_FOLLOW_UP_CHOICES
        show_scheduled_entries = self.visit_instance.reason.lower() not in [x.lower() for x in visit_reason_no_follow_up_choices.itervalues()]
        # possible conditions that override above
        # subject is at the off study visit (lost)
        if self.visit_instance.reason.lower() in self.visit_instance.get_off_study_reason():
            visit_date = date(self.visit_instance.report_datetime.year, self.visit_instance.report_datetime.month, self.visit_instance.report_datetime.day)
            if self.visit_instance.get_off_study_cls().objects.filter(registered_subject=self.registered_subject, offstudy_date=visit_date):
                # has an off study form completed on same day as visit
                off_study_instance = self.visit_instance.get_off_study_cls().objects.get(registered_subject=self.registered_subject, offstudy_date=visit_date)
                show_scheduled_entries = off_study_instance.show_scheduled_entries_on_off_study_date()
        return show_scheduled_entries

    def add_or_update_for_visit(self):
        """ Loops thru the list of entries configured for the visit_definition and calls the entry_meta_data_manager for each model.

        The visit definition comes instance."""
        for entry in self.entry_model.objects.filter(visit_definition=self.visit_instance.appointment.visit_definition):
            model = entry.get_model()
            model.entry_meta_data_manager.visit_instance = self.visit_instance
            try:
                model.entry_meta_data_manager.instance = model.objects.get(**model.entry_meta_data_manager.query_options)
            except model.DoesNotExist:
                model.entry_meta_data_manager.instance = None
            model.entry_meta_data_manager.update_meta_data()
            if model.entry_meta_data_manager.instance:
                model.entry_meta_data_manager.run_rule_groups()

    def get_next_entry_for(self, entry_order):
        """Gets next meta data instance based on the given entry order, used with the save_next button on a form."""
        next_meta_data_instance = None
        options = {
            'registered_subject_id': self.registered_subject.pk,
            'appointment_id': self.appointment_zero.pk,
            'entry_status': REQUIRED,
            '{0}__entry_order__gt'.format(self.entry_attr): entry_order}
        if self.meta_data_model.objects.filter(**options):
            next_meta_data_instance = self.meta_data_model.objects.filter(**options)[0]
        return next_meta_data_instance

    def get_entries_for(self, entry_category, entry_status=None):
        """Returns a list of meta data instances for the given subject and appointment_zero."""
        meta_data_instances = []
        if self.appointment_zero:
            options = {
               'registered_subject_id': self.registered_subject.pk,
               'appointment_id': self.appointment_zero.pk,
               '{0}__entry_category__iexact'.format(self.entry_attr): entry_category,
               }
            if entry_status:
                options.update({'entry_status': entry_status})
            meta_data_instances = self.meta_data_model.objects.filter(**options).order_by('{0}__entry_order'.format(self.entry_attr))
        return meta_data_instances

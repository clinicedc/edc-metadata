from edc_base.utils import convert_from_camel
from edc_constants.constants import REQUIRED, YES
from edc_visit_tracking.constants import VISIT_REASON_NO_FOLLOW_UP_CHOICES
from django.core.exceptions import FieldError


class BaseMetaDataHelper(object):
    """ Base class for all classes that manage the entry state
    of additional, scheduled and unscheduled data."""
    def __init__(self, appointment, visit_instance=None, visit_model_attrname=None):
        self.appointment = appointment
        self.visit_model = self.appointment.visit_definition.visit_tracking_content_type_map.model_class()
        self.visit_model_attrname = visit_model_attrname or convert_from_camel(self.visit_model._meta.object_name)
        self.visit_instance = visit_instance

    def __repr__(self):
        return 'BaseMetaDataHelper({0.instance!r})'.format(self)

    def __str__(self):
        return '({0.instance!r})'.format(self)

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
        if model_or_instance:
            if model_or_instance._meta.model_name != self.visit_model._meta.model_name:
                raise ValueError(
                    '{} expected the visit instance to be an instance of \'{}\' '
                    'as specified in the visit definition. '
                    'Got \'{}\''.format(self.__class__.__name__,
                                        self.visit_model.__name__,
                                        model_or_instance.__class__.__name__))
        try:
            self._visit_instance = self.visit_model.objects.get(appointment=self.appointment)
        except AttributeError as e:
            if 'Manager isn\'t accessible via' not in str(e):
                raise AttributeError(str(e))
            self._visit_instance = model_or_instance

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

    def show_entries(self):
        """Returns True if scheduled forms on the dashboard should be show / links active.

        If the participant os off study, the value of \'has_scheduled_data\' on the
        visit tracking for is used (YES=True, No=False)."""
        try:
            no_follow_up_reasons = self.visit_instance.get_visit_reason_no_follow_up_choices()
        except AttributeError as e:
            if 'get_visit_reason_no_follow_up_choices' not in str(e):
                raise AttributeError(str(e))
            no_follow_up_reasons = VISIT_REASON_NO_FOLLOW_UP_CHOICES
        show_entries = self.visit_instance.reason not in no_follow_up_reasons
        if self.visit_instance.reason in self.visit_instance.get_off_study_reason():
            off_study_model = self.visit_instance.off_study_model
            try:
                options = {'{}'.format(off_study_model.visit_model_attr): self.visit_instance}
                off_study_instance = off_study_model.objects.get(**options)
                show_entries = off_study_instance.has_scheduled_data == YES
            except off_study_model.DoesNotExist:
                pass
        return show_entries

    def add_or_update_for_visit(self):
        """ Loops thru the list of entries configured for the visit_definition
        and calls the entry_meta_data_manager for each model.

        The visit definition comes instance."""
        for entry in self.entry_model.objects.filter(
                visit_definition=self.visit_instance.appointment.visit_definition):
            model = entry.get_model()
            model.entry_meta_data_manager.visit_instance = self.visit_instance
            try:
                model.entry_meta_data_manager.instance = model.objects.get(
                    **model.entry_meta_data_manager.query_options)
            except model.DoesNotExist:
                model.entry_meta_data_manager.instance = None
            except FieldError as e:
                raise FieldError(e, 'Try specifying the correct \'visit_attr_name\' when declaring '
                                 'the entry_meta_data_manager on {}.'.format(model))
            model.entry_meta_data_manager.update_meta_data()
            if model.entry_meta_data_manager.instance:
                model.entry_meta_data_manager.run_rule_groups()

    def get_next_entry_for(self, entry_order):
        """Gets next meta data instance based on the given entry order,
        used with the save_next button on a form."""
        instance = None
        options = {
            'registered_subject_id': self.appointment.registered_subject.pk,
            'appointment_id': self.appointment_zero.pk,
            'entry_status': REQUIRED,
            '{0}__entry_order__gt'.format(self.entry_attr): entry_order}
        if self.meta_data_model.objects.filter(**options):
            instance = self.meta_data_model.objects.filter(**options)[0]
        return instance

    def get_meta_data(self, entry_status=None):
        """Returns a list of meta data instances for the given subject and appointment_zero."""
        if self.appointment_zero:
            options = {
                'registered_subject_id': self.appointment.registered_subject.pk,
                'appointment_id': self.appointment_zero.pk}
            if entry_status:
                options.update({'entry_status': entry_status})
            meta_data = self.meta_data_model.objects.filter(**options).order_by(
                '{0}__entry_order'.format(self.entry_attr))
        else:
            meta_data = []
        return meta_data

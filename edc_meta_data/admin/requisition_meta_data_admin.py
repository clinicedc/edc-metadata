from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from edc_appointment.models import Appointment
from edc_registration.models import RegisteredSubject

from ..forms import RequisitionMetaDataForm
from ..models import RequisitionMetaData, LabEntry


class RequisitionMetaDataAdmin(BaseModelAdmin):

    form = RequisitionMetaDataForm
    search_fields = (
        'registered_subject__subject_identifier', 'lab_entry__visit_definition__code',
        'lab_entry__requisition_panel__name', 'id')
    list_display = (
        'registered_subject', 'lab_entry', 'entry_status', 'fill_datetime', 'due_datetime', 'close_datetime')
    list_filter = (
        'entry_status', 'lab_entry__visit_definition__code', 'fill_datetime',
        'created', 'user_created', 'hostname_created')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "registered_subject":
            kwargs["queryset"] = RegisteredSubject.objects.filter(pk=request.GET.get('registered_subject'))
        if db_field.name == "appointment":
            kwargs["queryset"] = Appointment.objects.filter(pk=request.GET.get('appointment'))
        if db_field.name == "lab_entry":
            kwargs["queryset"] = LabEntry.objects.filter(pk=request.GET.get('lab_entry'))
        return super(RequisitionMetaDataAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(RequisitionMetaData, RequisitionMetaDataAdmin)

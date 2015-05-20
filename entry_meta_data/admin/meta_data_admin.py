from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin
from edc.subject.appointment.models import Appointment
from edc.subject.entry.models import Entry, LabEntry
from edc.subject.registration.models import RegisteredSubject

from ..forms import ScheduledEntryMetaDataForm, RequisitionMetaDataForm
from ..models import ScheduledEntryMetaData, RequisitionMetaData


class ScheduledEntryMetaDataAdmin(BaseModelAdmin):

    form = ScheduledEntryMetaDataForm
    search_fields = ('registered_subject__subject_identifier', 'entry__visit_definition__code', 'entry__content_type_map__model', 'id')
    list_display = ('registered_subject', 'entry', 'entry_status', 'fill_datetime', 'due_datetime', 'close_datetime', 'created', 'hostname_created')
    list_filter = ('entry_status', 'entry__visit_definition__code', 'fill_datetime', 'created', 'user_created', 'hostname_created')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "registered_subject":
            kwargs["queryset"] = RegisteredSubject.objects.filter(pk=request.GET.get('registered_subject'))
        if db_field.name == "appointment":
            kwargs["queryset"] = Appointment.objects.filter(pk=request.GET.get('appointment'))
        if db_field.name == "entry":
            kwargs["queryset"] = Entry.objects.filter(pk=request.GET.get('entry'))
        return super(ScheduledEntryMetaDataAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(ScheduledEntryMetaData, ScheduledEntryMetaDataAdmin)


class RequisitionMetaDataAdmin(BaseModelAdmin):

    form = RequisitionMetaDataForm
    search_fields = ('registered_subject__subject_identifier', 'lab_entry__visit_definition__code', 'lab_entry__requisition_panel__name')
    list_display = ('registered_subject', 'lab_entry', 'entry_status', 'fill_datetime', 'due_datetime', 'close_datetime')
    list_filter = ('entry_status', 'lab_entry__visit_definition__code', 'fill_datetime', 'created', 'user_created', 'hostname_created')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "registered_subject":
            kwargs["queryset"] = RegisteredSubject.objects.filter(pk=request.GET.get('registered_subject'))
        if db_field.name == "appointment":
            kwargs["queryset"] = Appointment.objects.filter(pk=request.GET.get('appointment'))
        if db_field.name == "lab_entry":
            kwargs["queryset"] = LabEntry.objects.filter(pk=request.GET.get('lab_entry'))
        return super(RequisitionMetaDataAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(RequisitionMetaData, RequisitionMetaDataAdmin)

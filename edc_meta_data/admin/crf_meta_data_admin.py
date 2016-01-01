from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin
from edc_appointment.models import Appointment
from edc_registration.models import RegisteredSubject

from ..forms import CrfMetaDataForm
from ..models import CrfMetaData, CrfEntry


class CrfMetaDataAdmin(BaseModelAdmin):

    form = CrfMetaDataForm
    search_fields = (
        'registered_subject__subject_identifier', 'crf_entry__visit_definition__code',
        'entry__content_type_map__model', 'id')
    list_display = (
        'registered_subject', 'crf_entry', 'entry_status', 'fill_datetime',
        'due_datetime', 'close_datetime', 'created', 'hostname_created')
    list_filter = (
        'entry_status', 'crf_entry__visit_definition__code', 'fill_datetime',
        'created', 'user_created', 'hostname_created')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "registered_subject":
            kwargs["queryset"] = RegisteredSubject.objects.filter(pk=request.GET.get('registered_subject'))
        if db_field.name == "appointment":
            kwargs["queryset"] = Appointment.objects.filter(pk=request.GET.get('appointment'))
        if db_field.name == "crf_entry":
            kwargs["queryset"] = CrfEntry.objects.filter(pk=request.GET.get('crf_entry'))
        return super(CrfMetaDataAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(CrfMetaData, CrfMetaDataAdmin)

from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin, BaseTabularInline

from ..models import LabEntry


class LabEntryAdmin(BaseModelAdmin):

    search_fields = ('visit_definition__code', 'requisition_panel__name')

    list_display = ('requisition_panel', 'visit_definition', 'entry_order', 'default_entry_status', 'additional', 'entry_category')

    list_filter = ('entry_category', 'visit_definition__code', 'default_entry_status', 'additional', 'created', 'requisition_panel__name',)

admin.site.register(LabEntry, LabEntryAdmin)


class LabEntryInline (BaseTabularInline):
    model = LabEntry
    extra = 0
    fields = (
        'requisition_panel',
        'entry_order',
        'default_entry_status',
        'additional',
        'entry_category',
        'entry_window_calculation',
        'time_point',
        'lower_window',
        'lower_window_unit',
        'upper_window',
        'upper_window_unit',
    )

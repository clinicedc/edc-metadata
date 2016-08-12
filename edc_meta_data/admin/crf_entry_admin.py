from django.contrib import admin

from edc_base.modeladmin.admin import BaseTabularInline

from .base_model_admin import BaseModelAdmin
from ..models import CrfEntry


class CrfEntryAdmin(BaseModelAdmin):

    search_fields = ('visit_definition__code', 'content_type_map__model', 'id')
    list_display = (
        'content_type_map', 'visit_definition', 'entry_order', 'default_entry_status',
        'additional', 'entry_category', 'group_title')
    list_filter = (
        'entry_category', 'group_title', 'visit_definition__code', 'default_entry_status',
        'additional', 'created', 'content_type_map__model',)
admin.site.register(CrfEntry, CrfEntryAdmin)


class CrfEntryInline (BaseTabularInline):
    model = CrfEntry
    extra = 0
    fields = (
        'content_type_map',
        'entry_order',
        'default_entry_status',
        'additional',
        'entry_category',
        'entry_window_calculation',
        'group_title')

from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin

from ..models import RequisitionPanel


class RequisitionPanelAdmin(BaseModelAdmin):

    search_fields = ('name', 'aliquot_type_alpha_code')

    list_display = ('name', 'aliquot_type_alpha_code')

    list_filter = ('aliquot_type_alpha_code',)

admin.site.register(RequisitionPanel, RequisitionPanelAdmin)

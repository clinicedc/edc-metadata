from django import forms

from edc_constants.constants import QUERY

from ..models import RequisitionMetaData


class RequisitionMetaDataForm (forms.ModelForm):
    def clean(self):
        cleaned_data = super(RequisitionMetaDataForm, self).clean()
        if cleaned_data['entry_status'] == QUERY and not cleaned_data['entry_comment']:
            raise forms.ValidationError(
                "Entry status has been set to 'QUERY', Please provide a short comment to describe the query")
        return cleaned_data

    class Meta:
        model = RequisitionMetaData

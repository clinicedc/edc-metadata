from django import forms

from ..models import CrfMetaData


class CrfMetaDataForm (forms.ModelForm):

    def clean(self):
        cleaned_data = super(CrfMetaDataForm, self).clean()
        if cleaned_data['entry_status'] == 'QUERY' and not cleaned_data['entry_comment']:
            raise forms.ValidationError(
                "Entry status has been set to 'QUERY', Please provide a short comment to describe the query")
        return cleaned_data

    class Meta:
        model = CrfMetaData
        fields = '__all__'

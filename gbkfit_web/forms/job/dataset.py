from django import forms

from gbkfit_web.models import DataSet


class DataSetForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DataSetForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DataSet

        fields = ['type', 'data', 'error', 'mask']

        widgets = {
            'type': forms.Select(
                attrs={'class': 'form-control'},
            ),
            'data': forms.FileInput(
                attrs={'class': "upload"},
            ),
            'error': forms.FileInput(
                attrs={'class': "upload"},
            ),
            'mask': forms.FileInput(
                attrs={'class': "upload"},
            ),
        }

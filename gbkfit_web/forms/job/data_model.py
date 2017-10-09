from django import forms

from gbkfit_web.models import DataModel


class DataModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DataModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DataModel

        fields = ['name', 'type', 'size_x', 'size_y', 'size_z', 'step_x', 'step_y', 'step_z',]

        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'type': forms.Select(
                attrs={'class': 'form-control'},
            ),
            'size_x': forms.TextInput(
                attrs={'class': "form-control"},
            ),
            'size_y': forms.TextInput(
                attrs={'class': "form-control"},
            ),
            'size_z': forms.TextInput(
                attrs={'class': "form-control"},
            ),
            'step_x': forms.TextInput(
                attrs={'class': "form-control"},
            ),
            'step_y': forms.TextInput(
                attrs={'class': "form-control"},
            ),
            'step_z': forms.TextInput(
                attrs={'class': "form-control"},
            ),
        }

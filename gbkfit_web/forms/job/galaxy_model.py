from django import forms

from gbkfit_web.models import GalaxyModel


class GalaxyModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(GalaxyModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = GalaxyModel

        fields = ['name', 'type', 'fprofile_type', 'vprofile_type', 'nrings', 'rsize']

        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'type': forms.Select(
                attrs={'class': 'form-control'},
            ),
            'fprofile_type': forms.Select(
                attrs={'class': "form-control"},
            ),
            'vprofile_type': forms.Select(
                attrs={'class': "form-control"},
            ),
            'nrings': forms.TextInput(
                attrs={'class': "form-control"},
            ),
            'rsize': forms.TextInput(
                attrs={'class': "form-control"},
            ),
        }

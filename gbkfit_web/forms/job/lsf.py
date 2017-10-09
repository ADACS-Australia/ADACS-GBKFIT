from django import forms

from gbkfit_web.models import LSF


class LSFForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(LSFForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LSF

        fields = ['name', 'type', 'fwhm', 'beta']

        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'type': forms.Select(
                attrs={'class': 'form-control'},
            ),
            'fwhm': forms.TextInput(
                attrs={'class': "form-control"},
            ),
            'beta': forms.TextInput(
                attrs={'class': "form-control"},
            ),
        }

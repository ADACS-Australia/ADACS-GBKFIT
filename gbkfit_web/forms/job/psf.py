from django import forms

from gbkfit_web.models import PSF


class PSFForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PSFForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PSF

        fields = ['name', 'type', 'fwhm_x', 'fwhm_y', 'pa', 'beta']

        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'type': forms.Select(
                attrs={'class': 'form-control'},
            ),
            'fwhm_x': forms.TextInput(
                attrs={'class': "form-control"},
            ),
            'fwhm_y': forms.TextInput(
                attrs={'class': "form-control"},
            ),
            'pa': forms.TextInput(
                attrs={'class': "form-control"},
            ),
            'beta': forms.TextInput(
                attrs={'class': "form-control"},
            ),
        }

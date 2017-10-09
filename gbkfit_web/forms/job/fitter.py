from django import forms

from gbkfit_web.models import Fitter


class FitterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FitterForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Fitter

        fields = ['name', 'type',
                  'ftol', 'xtol', 'gtol', 'epsfcn', 'stepfactor', 'covtol', 'maxiter', 'maxfev', 'nprint', 'douserscale', 'nofinitecheck',
                  'efr', 'tol', 'ztol', 'logzero', '_is', 'mmodal', 'ceff', 'nlive', 'maxiter', 'seed', 'outfile',
                  ]
        
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'type': forms.Select(
                attrs={'class': 'form-control'},
            ),
            'ftol': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'xtol': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'gtol': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'epsfcn': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'stepfactor': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'covtol': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'maxiter': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'maxfev': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'nprint': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'douserscale': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'nofinitecheck': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'efr': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'tol': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'ztol': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'logzero': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            '_is': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'mmodal': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'ceff': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'nlive': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'maxiter': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'seed': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'outfile': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
        }

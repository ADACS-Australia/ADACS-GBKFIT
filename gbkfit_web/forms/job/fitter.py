from django import forms
from gbkfit_web.models import Fitter, Job

FIELDS = ['fitter_type',
          'ftol', 'xtol', 'gtol', 'epsfcn', 'stepfactor', 'covtol', 'mpfit_maxiter', 'maxfev', 'nprint', 'douserscale',
          'nofinitecheck',
          'efr', 'tol', 'ztol', 'logzero', '_is', 'mmodal', 'ceff', 'nlive', 'multinest_maxiter', 'seed', 'outfile',
          ]

WIDGETS = {
    'fitter_type': forms.Select(
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
    'mpfit_maxiter': forms.TextInput(
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
    'multinest_maxiter': forms.TextInput(
        attrs={'class': 'form-control'},
    ),
    'seed': forms.TextInput(
        attrs={'class': 'form-control'},
    ),
    'outfile': forms.TextInput(
        attrs={'class': 'form-control'},
    ),
}

class FitterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FitterForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Fitter
        fields = FIELDS
        widgets = WIDGETS

    def save(self):
        self.full_clean()
        data = self.cleaned_data

        id = self.request.session['draft_job']['id']
        job = Job.objects.get(id=id)

        try:
            result = Fitter.objects.create(
                job=job,
                fitter_type=data.get('fitter_type'),
                ftol=data.get('ftol'),
                xtol=data.get('xtol'),
                gtol=data.get('gtol'),
                epsfcn=data.get('epsfcn'),
                stepfactor=data.get('stepfactor'),
                covtol=data.get('covtol'),
                mpfit_maxiter=data.get('mpfit_maxiter'),
                maxfev=data.get('maxfev'),
                nprint=data.get('nprint'),
                douserscale=data.get('douserscale'),
                nofinitecheck=data.get('nofinitecheck'),
                _is=data.get('_is'),
                mmodal=data.get('mmodal'),
                nlive=data.get('nlive'),
                tol=data.get('tol'),
                efr=data.get('efr'),
                ceff=data.get('ceff'),
                ztol=data.get('ztol'),
                logzero=data.get('logzero'),
                multinest_maxiter=data.get('multinest_maxiter'),
                seed=data.get('seed'),
                outfile=data.get('outfile'),
            )
        except:
            result = Fitter.objects.filter(job_id=id).update(
                fitter_type=data.get('fitter_type'),
                ftol=data.get('ftol'),
                xtol=data.get('xtol'),
                gtol=data.get('gtol'),
                epsfcn=data.get('epsfcn'),
                stepfactor=data.get('stepfactor'),
                covtol=data.get('covtol'),
                mpfit_maxiter=data.get('mpfit_maxiter'),
                maxfev=data.get('maxfev'),
                nprint=data.get('nprint'),
                douserscale=data.get('douserscale'),
                nofinitecheck=data.get('nofinitecheck'),
                _is=data.get('_is'),
                mmodal=data.get('mmodal'),
                nlive=data.get('nlive'),
                tol=data.get('tol'),
                efr=data.get('efr'),
                ceff=data.get('ceff'),
                ztol=data.get('ztol'),
                logzero=data.get('logzero'),
                multinest_maxiter=data.get('multinest_maxiter'),
                seed=data.get('seed'),
                outfile=data.get('outfile'),
            )

        self.request.session['fitter'] = Fitter.objects.get(job_id=id).as_json()

class EditFitterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditFitterForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Fitter
        fields = FIELDS
        widgets = WIDGETS

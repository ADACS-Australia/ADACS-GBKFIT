from django import forms
from gbkfit_web.models import Fitter, Job
from django.utils.translation import ugettext_lazy as _

FIELDS = ['fitter_type',
          'ftol', 'xtol', 'gtol', 'epsfcn', 'stepfactor', 'covtol', 'mpfit_maxiter', 'maxfev', 'nprint', 'douserscale',
          'nofinitecheck',
          'efr', 'tol', 'ztol', 'logzero', 'multinest_is', 'mmodal', 'ceff', 'nlive', 'multinest_maxiter', 'seed', 'outfile',
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
    'nprint': forms.CheckboxInput(
        # attrs={'class': 'form-control'},
    ),
    'douserscale': forms.CheckboxInput(
        # attrs={'class': 'form-control'},
    ),
    'nofinitecheck': forms.CheckboxInput(
        # attrs={'class': 'form-control'},
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
    'multinest_is': forms.CheckboxInput(
        # attrs={'class': 'form-control'},
    ),
    'mmodal': forms.CheckboxInput(
        # attrs={'class': 'form-control'},
    ),
    'ceff': forms.CheckboxInput(
        # attrs={'class': 'form-control'},
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
    'outfile': forms.CheckboxInput(
        # attrs={'class': 'form-control'},
    ),
}

LABELS = {
    'fitter_type': _('Type'),
    'ftol': _('ftol'),
    'xtol': _('xtol'),
    'gtol': _('gtol'),
    'epsfcn': _('epsfcn'),
    'stepfactor': _('stepfactor'),
    'covtol': _('covtol'),
    'mpfit_maxiter': _('maxiter'),
    'maxfev': _('maxfev'),
    'nprint': _('nprint'),
    'douserscale': _('douserscale'),
    'nofinitecheck': _('nofinitecheck'),
    'efr': _('efr'),
    'tol': _('tol'),
    'ztol': _('ztol'),
    'logzero': _('logzero'),
    'multinest_is': _('is'),
    'mmodal': _('mmodal'),
    'ceff': _('ceff'),
    'nlive': _('nlive'),
    'multinest_maxiter': _('maxiter'),
    'seed': _('seed'),
    'outfile': _('outfile'),
}


class FitterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.id = kwargs.pop('id', None)
        super(FitterForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Fitter
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS

    def save(self):
        self.full_clean()
        data = self.cleaned_data

        job = Job.objects.get(id=self.id)


        Fitter.objects.create(
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
            multinest_is=data.get('multinest_is'),
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

        self.request.session['fitter'] = self.as_json(data)

    def as_json(self, data):
        """
        Return 'fitter' parameters into a json string (dictionary)

        :return: json dict
        """
        if data.get('fitter_type') == Fitter.MPFIT:
            return dict(
                    type="gbkfit.fitter." + data.get('fitter_type'),
                    ftol = data.get('ftol'),
                    xtol = data.get('xtol'),
                    gtol = data.get('gtol'),
                    epsfcn = data.get('epsfcn'),
                    stepfactor = data.get('stepfactor'),
                    covtol = data.get('covtol'),
                    maxiter = data.get('mpfit_maxiter'),
                    maxfev = data.get('maxfev'),
                    nprint = data.get('nprint'),
                    douserscale = data.get('douserscale'),
                    nofinitecheck = data.get('nofinitecheck')
                )
        else:
            return dict(
                    type="gbkfit.fitter." + data.get('fitter_type'),
                    multinest_is = data.get('multinest_is'),
                    mmodal = data.get('mmodal'),
                    nlive = data.get('nlive'),
                    tol = data.get('tol'),
                    efr = data.get('efr'),
                    ceff = data.get('ceff'),
                    ztol = data.get('ztol'),
                    logzero = data.get('logzero'),
                    maxiter = data.get('multinest_maxiter'),
                    seed = data.get('seed'),
                    outfile = data.get('outfile')
                )

class EditFitterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.job_id = kwargs.pop('job_id', None)
        if self.job_id:
            try:
                self.request.session['fitter'] = Fitter.objects.get(job_id=self.job_id).as_json()
            except:
                pass
        super(EditFitterForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Fitter
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS

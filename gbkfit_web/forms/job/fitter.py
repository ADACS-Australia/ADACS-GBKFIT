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
        attrs={'class': 'form-control has-popover'},
    ),
    'ftol': forms.TextInput(
        attrs={'class': 'form-control has-popover'},
    ),
    'xtol': forms.TextInput(
        attrs={'class': 'form-control has-popover'},
    ),
    'gtol': forms.TextInput(
        attrs={'class': 'form-control has-popover'},
    ),
    'epsfcn': forms.TextInput(
        attrs={'class': 'form-control has-popover'},
    ),
    'stepfactor': forms.TextInput(
        attrs={'class': 'form-control has-popover'},
    ),
    'covtol': forms.TextInput(
        attrs={'class': 'form-control has-popover'},
    ),
    'mpfit_maxiter': forms.TextInput(
        attrs={'class': 'form-control has-popover'},
    ),
    'maxfev': forms.TextInput(
        attrs={'class': 'form-control has-popover'},
    ),
    'nprint': forms.CheckboxInput(
        attrs={'class': 'has-popover'},
    ),
    'douserscale': forms.CheckboxInput(
        attrs={'class': 'has-popover'},
    ),
    'nofinitecheck': forms.CheckboxInput(
        attrs={'class': 'has-popover'},
    ),
    'efr': forms.TextInput(
        attrs={'class': 'form-control has-popover'},
    ),
    'tol': forms.TextInput(
        attrs={'class': 'form-control has-popover'},
    ),
    'ztol': forms.TextInput(
        attrs={'class': 'form-control has-popover'},
    ),
    'logzero': forms.TextInput(
        attrs={'class': 'form-control has-popover'},
    ),
    'multinest_is': forms.CheckboxInput(
        attrs={'class': 'has-popover'},
    ),
    'mmodal': forms.CheckboxInput(
        attrs={'class': 'has-popover'},
    ),
    'ceff': forms.CheckboxInput(
        attrs={'class': 'has-popover'},
    ),
    'nlive': forms.TextInput(
        attrs={'class': 'form-control has-popover'},
    ),
    'multinest_maxiter': forms.TextInput(
        attrs={'class': 'form-control has-popover'},
    ),
    'seed': forms.TextInput(
        attrs={'class': 'form-control has-popover'},
    ),
    'outfile': forms.CheckboxInput(
        attrs={'class': 'has-popover'},
    ),
}

LABELS = {
    'fitter_type': _('Type'),
    'ftol': _('Chi-square criterium'),
    'xtol': _('Parameter criterium'),
    'gtol': _('Orthogonality criterium'),
    'epsfcn': _('Derivative step size'),
    'stepfactor': _('Initial step bound'),
    'covtol': _('Covariance tolerance'),
    'mpfit_maxiter': _('Maximum iterations'),
    'maxfev': _('Maximum function evaluations'),
    'nprint': _('Print information to stdout'),
    'douserscale': _('Scale variables'),
    'nofinitecheck': _('Check for infinite quantities'),

    'efr': _('Sampling efficiency'),
    'tol': _('Evidence tolerance'),
    'ztol': _('Null log-evidence'),
    'logzero': _('Log-zero'),
    'multinest_is': _('Importance Nested Sampling'),
    'mmodal': _('Mode separation'),
    'ceff': _('Constant efficiency'),
    'nlive': _('Live points'),
    'multinest_maxiter': _('Maximum iterations'),
    'seed': _('Seed'),
    'outfile': _('Output to file'),
}

HELP_TEXTS = {
    'fitter_type': _('Type'),
    'ftol': _('Relative chi-square convergence criterium.'),
    'xtol': _('Relative parameter convergence criterium.'),
    'gtol': _('Orthogonality convergence criterium.'),
    'epsfcn': _('Finite derivative step size.'),
    'stepfactor': _('Initial step bound.'),
    'covtol': _('Range tolerance for covariance calculation.'),
    'mpfit_maxiter': _('Maximum number of iterations.'),
    'maxfev': _('Maximum number of function evaluations, or 0 for no limit.'),
    'nprint': _('Print information to stdout.'),
    'douserscale': _('Scale variables by user values.'),
    'nofinitecheck': _('Check for infinite quantities.'),

    'efr': _('Sampling efficiency.'),
    'tol': _('Evidence tolerance factor.'),
    'ztol': _('Null log-evidence.'),
    'logzero': _('Points with log-likelihood < logzero will be ignored by MultiNest.'),
    'multinest_is': _('Enable Importance Nested Sampling. If enabled, mode separation is not possible.'),
    'mmodal': _('Enable mode separation. If enabled, Importance Nested sampling is not possible.'),
    'ceff': _('Enable constant efficiency mode.'),
    'nlive': _('Number of live points'),
    'multinest_maxiter': _('Maximum number of iterations. A non-positive value means infinity.'),
    'seed': _('Random number generator seed.'),
    'outfile': _('Output results to file.'),
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

        for field in self.fields:
            help_text = self.fields[field].help_text
            self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update(
                    {'data-content': help_text, 'data-placement': 'top',
                     'data-container': 'body'})

    class Meta:
        model = Fitter
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS
        help_texts = HELP_TEXTS

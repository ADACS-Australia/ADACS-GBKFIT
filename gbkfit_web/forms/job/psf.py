from django import forms
from gbkfit_web.models import PSF, Job
from django.utils.translation import ugettext_lazy as _

FIELDS = ['psf_type', 'fwhm_x', 'fwhm_y', 'pa', 'beta']

WIDGETS = {
    'psf_type': forms.Select(
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

LABELS = {
    'psf_type': _('Type'),
    'fwhm_x': _('FWHM X'),
    'fwhm_y': _('FWHM Y'),
    'pa': _('pa'),
    'beta': _('beta'),
}


class PSFForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PSFForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PSF
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS

    def save(self):
        self.full_clean()
        data = self.cleaned_data

        try:
            id = self.request.session['draft_job']['id']
        except:
            id = self.request.user.id

        job = Job.objects.get(id=id)

        try:
            result = PSF.objects.create(
                job=job,
                psf_type=data.get('psf_type'),
                fwhm_x=data.get('fwhm_x'),
                fwhm_y=data.get('fwhm_y'),
                pa=data.get('pa'),
                beta=data.get('beta'),
            )
        except:
            result = PSF.objects.filter(job_id=id).update(
                psf_type=data.get('psf_type'),
                fwhm_x=data.get('fwhm_x'),
                fwhm_y=data.get('fwhm_y'),
                pa=data.get('pa'),
                beta=data.get('beta'),
            )
        self.request.session['psf'] = self.as_json(data)
        
    def as_json(self, data):
        if data.get('psf_type') in [PSF.MOFFAT]:
            return dict(
                type=data.get('psf_type'),
                fwhm_x=data.get('fwhm_x'),
                fwhm_y=data.get('fwhm_y'),
                pa=data.get('pa'),
                beta=data.get('beta')
            )
        else:
            return dict(
                type=data.get('psf_type'),
                fwhm_x=data.get('fwhm_x'),
                fwhm_y=data.get('fwhm_y'),
                pa=data.get('pa')
            )

class EditPSFForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditPSFForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PSF
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS
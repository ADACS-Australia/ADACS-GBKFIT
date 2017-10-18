from django import forms
from gbkfit_web.models import PSF, Job

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

class PSFForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PSFForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PSF
        fields = FIELDS
        widgets = WIDGETS

    def save(self):
        self.full_clean()
        data = self.cleaned_data

        id = self.request.session['draft_job']['id']
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
        self.request.session['psf'] = PSF.objects.get(job_id=id).as_json()

class EditPSFForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditPSFForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PSF
        fields = FIELDS
        widgets = WIDGETS

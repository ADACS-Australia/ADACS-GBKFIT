from django import forms
from gbkfit_web.models import LSF, Job

FIELDS = ['lsf_type', 'fwhm', 'beta']

WIDGETS = {
    'lsf_type': forms.Select(
        attrs={'class': 'form-control'},
    ),
    'fwhm': forms.TextInput(
        attrs={'class': "form-control"},
    ),
    'beta': forms.TextInput(
        attrs={'class': "form-control"},
    ),
}

class LSFForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(LSFForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LSF
        fields = FIELDS
        widgets = WIDGETS

    def save(self):
        self.full_clean()
        data = self.cleaned_data

        id = self.request.session['draft_job']['id']
        job = Job.objects.get(id=id)

        try:
            result = LSF.objects.create(
                job=job,
                lsf_type=data.get('lsf_type'),
                fwhm=data.get('fwhm'),
                beta=data.get('beta'),
            )
        except:
            result = LSF.objects.filter(job_id=id).update(
                lsf_type=data.get('lsf_type'),
                fwhm=data.get('fwhm'),
                beta=data.get('beta'),
            )

        self.request.session['lsf'] = LSF.objects.get(job_id=id).as_json()

class EditLSFForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditLSFForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LSF
        fields = FIELDS
        widgets = WIDGETS

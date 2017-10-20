from django import forms
from gbkfit_web.models import LSF, Job
from django.utils.translation import ugettext_lazy as _

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

LABELS = {
    'lsf_type': _('Type'),
    'fwhm': _('FWHM'),
    'beta': _('Beta'),
}


class LSFForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(LSFForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LSF
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS

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

        self.request.session['lsf'] = self.as_json(data)

    def as_json(data):
        if data.get('lsf_type') in [LSF.MOFFAT]:
            return dict(
                type=data.get('lsf_type'),
                fwhm=data.get('fwhm'),
                beta=data.get('beta')
            )
        else:
            return dict(
                type=data.get('lsf_type'),
                fwhm=data.get('fwhm')
            )

class EditLSFForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditLSFForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LSF
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS

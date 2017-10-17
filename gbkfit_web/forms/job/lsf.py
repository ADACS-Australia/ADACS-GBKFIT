from django import forms
from gbkfit_web.models import LSF, Job


class LSFForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(LSFForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LSF

        fields = ['lsf_type', 'fwhm', 'beta']

        widgets = {
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

    def save(self):
        self.full_clean()
        data = self.cleaned_data

        id = self.request.session['draft_job']['id']
        job = Job.objects.get(id=id)

        try:
            LSF.objects.create(
                job=job,
                lsf_type=data.get('lsf_type'),
                fwhm=data.get('fwhm'),
                beta=data.get('beta'),
            )
        except:
            LSF.objects.filter(job_id=id).update(
                lsf_type=data.get('lsf_type'),
                fwhm=data.get('fwhm'),
                beta=data.get('beta'),
            )
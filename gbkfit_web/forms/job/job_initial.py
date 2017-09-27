from django import forms
from django.utils.translation import ugettext_lazy as _

from gbkfit_web.models import Job


class JobInitialForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.field_order = ['job', 'job_name', ]
        super(JobInitialForm, self).__init__(*args, **kwargs)

    job_name = forms.CharField(
        label=_('Job Name'),
        max_length=255,
        widget=forms.TextInput(
            attrs={'class': "form-control"}
        ),
        required=False,
    )

    def clean(self):
        cleaned_data = super(JobInitialForm, self).clean()
        job = cleaned_data.get('job')  # selected job, empty for a the new one
        job_name = cleaned_data.get('job_name')  # new job name

        # the user either needs to select a draft job from the list or enter a new
        # job name for which a draft is going to be created
        if job is None or job == '':
            if job_name is None or job_name == '':
                raise forms.ValidationError(
                    "You must select a job or provide a job name"
                )
            else:
                if Job.objects.filter(
                        user=self.request.user,
                        name=self.cleaned_data.get('job_name')
                ).exists():
                    raise forms.ValidationError(
                        "You already have a job with the same name"
                    )
        return cleaned_data

    def save(self):
        self.full_clean()
        data = self.cleaned_data

        if not data.get('job'):  # creating a new draft job
            job_created = Job.objects.create(
                user=self.request.user,
                name=data.get('job_name')
            )
            self.request.session['draft_job'] = job_created.as_json()
        else:  # will edit an old draft
            self.request.session['draft_job'] = data.get('job').as_json()

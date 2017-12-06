#==============================================================================
#
# This code was developed as part of the Astronomy Data and Computing Services
# (ADACS; https:#adacs.org.au) 2017B Software Support program.
#
# Written by: Dany Vohl, Lewis Lakerink, Shibli Saleheen
# Date:       December 2017
#
# It is distributed under the MIT (Expat) License (see https:#opensource.org/):
#
# Copyright (c) 2017 Astronomy Data and Computing Services (ADACS)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#==============================================================================

from django import forms
from django.utils.translation import ugettext_lazy as _
from gbkfit_web.models import Job

FIELDS = ['name', 'description']

WIDGETS = {
    'name': forms.TextInput(
        attrs={'class': 'form-control'},
    ),
    'description': forms.Textarea(
        attrs={'class': 'form-control'},
    ),
}

LABELS = {
    'name': _('Job name'),
    'description': _('Job description'),
}


class JobInitialForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(JobInitialForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Job
        fields = FIELDS
        widget = WIDGETS
        labels = LABELS

    def clean(self):
        cleaned_data = super(JobInitialForm, self).clean()
        name = cleaned_data.get('name')  # new job name

        # the user either needs to select a draft job from the list or enter a new
        # job name for which a draft is going to be created
        if name is None or name == '':
            raise forms.ValidationError(
                "You must select a job or provide a job name"
            )
        else:
            if Job.objects.filter(
                    user=self.request.user,
                    name=self.cleaned_data.get('name')
            ).exists():
                raise forms.ValidationError(
                    "You already have a job with the same name"
                )
        return cleaned_data

    def save(self):
        self.full_clean()
        data = self.cleaned_data

        try:
            job_created = Job.objects.create(
                user=self.request.user,
                name=data.get('name')
            )
            self.request.session['draft_job'] = job_created.as_json()
        except:
            Job.objects.filter(id=id).update(
                name=data.get('name')
            )
            self.request.session['draft_job'] = Job.objects.filter(id=id).as_json()

class EditJobForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.job_id = kwargs.pop('job_id', None)
        if self.job_id:
            try:
                self.request.session['draft_job'] = Job.objects.get(id=self.job_id).as_json()
            except:
                pass
        super(EditJobForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Job
        fields = FIELDS
        widget = WIDGETS
        labels = LABELS

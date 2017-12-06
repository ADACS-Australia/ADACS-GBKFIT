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
        self.id = kwargs.pop('id', None)
        super(LSFForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LSF
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS

    def save(self):
        self.full_clean()
        data = self.cleaned_data

        job = Job.objects.get(id=self.id)

        LSF.objects.create(
            job=job,
            lsf_type=data.get('lsf_type'),
            fwhm=data.get('fwhm'),
            beta=data.get('beta'),
        )

        self.request.session['lsf'] = self.as_json(data)

    def as_json(self, data):
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
        self.request = kwargs.pop('request', None)
        self.job_id = kwargs.pop('job_id', None)
        if self.job_id:
            try:
                self.request.session['lsf'] = LSF.objects.get(job_id=self.job_id).as_json()
            except:
                pass
        super(EditLSFForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LSF
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS

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
from gbkfit_web.models import GalaxyModel, Job
from django.utils.translation import ugettext_lazy as _

FIELDS = ['gmodel_type', 'flx_profile', 'vel_profile']

WIDGETS = {
    'gmodel_type': forms.Select(
        attrs={'class': 'form-control'},
    ),
    "flx_profile": forms.Select(
        attrs={'class': "form-control"},
    ),
    "vel_profile": forms.Select(
        attrs={'class': "form-control"},
    ),
}

LABELS = {
    'gmodel_type': _('Type'),
    'flx_profile': _('Flux profile'),
    'vel_profile': _('Velocity profile'),
}


class GalaxyModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.id = kwargs.pop('id', None)
        super(GalaxyModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = GalaxyModel
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS

    def save(self):
        self.full_clean()
        data = self.cleaned_data

        job = Job.objects.get(id=self.id)

        GalaxyModel.objects.create(
            job=job,
            gmodel_type=data.get('gmodel_type'),
            flx_profile=data.get('flx_profile'),
            vel_profile=data.get('vel_profile'),
        )

        self.request.session['fitter'] = self.as_json(data)

    def as_json(self, data):
        return dict(
            type=data.get('gmodel_type'),
            flx_profile=data.get('flx_profile'),
            vel_profile=data.get('vel_profile'),
        )
            
class EditGalaxyModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.job_id = kwargs.pop('job_id', None)
        if self.job_id:
            try:
                self.request.session['galaxy_model'] = GalaxyModel.objects.get(job_id=self.job_id).as_json()
            except:
                pass
        super(EditGalaxyModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = GalaxyModel
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS

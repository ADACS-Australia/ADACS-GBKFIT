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
        super(GalaxyModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = GalaxyModel
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS

    def save(self):
        self.full_clean()
        data = self.cleaned_data

        id = self.request.session['draft_job']['id']
        job = Job.objects.get(id=id)

        try:
            result = GalaxyModel.objects.create(
                job=job,
                gmodel_type=data.get('gmodel_type'),
                flx_profile=data.get('flx_profile'),
                vel_profile=data.get('vel_profile'),
            )
        except:
            result = GalaxyModel.objects.filter(job_id=id).update(
                gmodel_type=data.get('gmodel_type'),
                flx_profile=data.get('flx_profile'),
                vel_profile=data.get('vel_profile'),
            )

        self.request.session['fitter'] = self.as_json(data)

    def as_json(data):
        return dict(
            type=data.get('gmodel_type'),
            flx_profile=data.get('flx_profile'),
            vel_profile=data.get('vel_profile'),
        )
            
class EditGalaxyModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditGalaxyModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = GalaxyModel
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS

from django import forms
from gbkfit_web.models import GalaxyModel, Job

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

class GalaxyModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(GalaxyModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = GalaxyModel
        fields = FIELDS
        widgets = WIDGETS

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

        self.request.session['fitter'] = GalaxyModel.objects.get(job_id=id).as_json()
            
class EditGalaxyModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditGalaxyModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = GalaxyModel
        fields = FIELDS
        widgets = WIDGETS

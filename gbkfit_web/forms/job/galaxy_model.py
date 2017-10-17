from django import forms
from gbkfit_web.models import GalaxyModel, Job


class GalaxyModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(GalaxyModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = GalaxyModel

        fields = ['gmodel_type',
                  "flx_profile",
                  "vel_profile",
                  ]

        widgets = {
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

    def save(self):
        self.full_clean()
        data = self.cleaned_data

        id = self.request.session['draft_job']['id']
        job = Job.objects.get(id=id)

        try:
            GalaxyModel.objects.create(
                job=job,
                gmodel_type=data.get('gmodel_type'),
                flx_profile=data.get('flx_profile'),
                vel_profile=data.get('vel_profile'),
            )
        except:
            GalaxyModel.objects.filter(job_id=id).update(
                gmodel_type=data.get('gmodel_type'),
                flx_profile=data.get('flx_profile'),
                vel_profile=data.get('vel_profile'),
            )
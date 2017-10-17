from django import forms
from gbkfit_web.models import DataModel, Job


class DataModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(DataModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DataModel

        fields = ['dmodel_type', 'method', 'scale_x', 'scale_y', 'scale_z', 'step_x', 'step_y', 'step_z']

        widgets = {
            'dmodel_type': forms.Select(
                attrs={'class': 'form-control'},
            ),
            'method': forms.Select(
                attrs={'class': 'form-control'},
            ),
            'scale_x': forms.TextInput(
                attrs={'class': "form-control"},
            ),
            'scale_y': forms.TextInput(
                attrs={'class': "form-control"},
            ),
            'scale_z': forms.TextInput(
                attrs={'class': "form-control"},
            ),
            'step_x': forms.TextInput(
                attrs={'class': "form-control"},
            ),
            'step_y': forms.TextInput(
                attrs={'class': "form-control"},
            ),
            'step_z': forms.TextInput(
                attrs={'class': "form-control"},
            ),
        }

    def save(self):
        self.full_clean()
        data = self.cleaned_data

        id = self.request.session['draft_job']['id']
        job = Job.objects.get(id=id)

        try:
            DataModel.objects.create(
                job=job,
                dmodel_type=data.get('dmodel_type'),
                method=data.get('method'),
                scale_x=data.get('scale_x'),
                scale_y=data.get('scale_y'),
                scale_z=data.get('scale_z'),
                step_x=data.get('step_x'),
                step_y=data.get('step_y'),
                step_z=data.get('step_z'),
            )
        except:
            DataModel.objects.filter(job_id=id).update(
                dmodel_type=data.get('dmodel_type'),
                method=data.get('method'),
                scale_x=data.get('scale_x'),
                scale_y=data.get('scale_y'),
                scale_z=data.get('scale_z'),
                step_x=data.get('step_x'),
                step_y=data.get('step_y'),
                step_z=data.get('step_z'),
            )
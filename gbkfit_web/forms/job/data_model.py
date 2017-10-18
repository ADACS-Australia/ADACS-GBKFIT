from django import forms
from gbkfit_web.models import DataModel, Job

FIELDS = ['dmodel_type', 'method', 'scale_x', 'scale_y', 'scale_z', 'step_x', 'step_y', 'step_z']

WIDGETS = {
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

class DataModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(DataModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DataModel
        fields = FIELDS
        widgets = WIDGETS

    def save(self):
        self.full_clean()
        data = self.cleaned_data

        id = self.request.session['draft_job']['id']
        job = Job.objects.get(id=id)

        try:
            result = DataModel.objects.create(
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
            result = DataModel.objects.filter(job_id=id).update(
                dmodel_type=data.get('dmodel_type'),
                method=data.get('method'),
                scale_x=data.get('scale_x'),
                scale_y=data.get('scale_y'),
                scale_z=data.get('scale_z'),
                step_x=data.get('step_x'),
                step_y=data.get('step_y'),
                step_z=data.get('step_z'),
            )
        self.request.session['data_model'] = DataModel.objects.get(job_id=id).as_json()

class EditDataModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditDataModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DataModel
        fields = FIELDS
        widgets = WIDGETS

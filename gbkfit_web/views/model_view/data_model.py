from django import forms
from gbkfit_web.models import DataModel, Job
from django.utils.translation import ugettext_lazy as _

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

LABELS = {
    'dmodel_type': _('Type'),
    'method': _('Method'),
    'scale_x': _('Scale X'),
    'scale_y': _('Scale Y'),
    'scale_z': _('Scale Z'),
    'step_x': _('Step X'),
    'step_y': _('Step Y'),
    'step_z': _('Step Z'),
}


class DataModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.id = kwargs.pop('id', None)
        super(DataModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DataModel
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS

    def save(self):
        self.full_clean()
        data = self.cleaned_data

        job = Job.objects.get(id=self.id)

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
        self.request.session['data_model'] = self.as_json(data)

    def as_json(self, data):
        if data.get('dmodel_type') in [DataModel.SCUBE_OMP, DataModel.SCUBE_CUDA]:
            return dict(
                type="gbkfit.dmodel." + data.get('dmodel_type'),
                step=[data.get('step_x'), data.get('step_y'), data.get('step_z')],
                scale=[data.get('scale_x'), data.get('scale_y'), data.get('scale_z')]
            )
        else:
            return dict(
                type="gbkfit.dmodel." + data.get('dmodel_type'),
                method=data.get('method'),
                step=[data.get('step_x'), data.get('step_y')],
                scale=[data.get('scale_x'), data.get('scale_y')],
            )

class EditDataModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.job_id = kwargs.pop('job_id', None)
        if self.job_id:
            try:
                self.request.session['data_model'] = DataModel.objects.get(job_id=self.job_id).as_json()
            except:
                pass
        super(EditDataModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DataModel
        fields = FIELDS
        widgets = WIDGETS
        labels = LABELS

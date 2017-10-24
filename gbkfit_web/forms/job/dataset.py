from django import forms
from gbkfit_web.models import DataSet, Job
from django.utils.translation import ugettext_lazy as _

FIELDS = ['dataset1_type', 'datafile1', 'errorfile1', 'maskfile1',
          'dataset2_type', 'datafile2', 'errorfile2', 'maskfile2',]

WIDGET = {
    'dataset1_type': forms.Select(
        attrs={'class': 'form-control'},
    ),
    'datafile1': forms.FileInput(
        attrs={'class': "upload"},
    ),
    'errorfile1': forms.FileInput(
        attrs={'class': "upload"},
    ),
    'maskfile1': forms.FileInput(
        attrs={'class': "upload"},
    ),
    'dataset2_type': forms.Select(
        attrs={'class': 'form-control'},
    ),
    'datafile2': forms.FileInput(
        attrs={'class': "upload"},
    ),
    'errorfile2': forms.FileInput(
        attrs={'class': "upload"},
    ),
    'maskfile2': forms.FileInput(
        attrs={'class': "upload"},
    )
}

LABELS = {
    'dataset1_type': _('Type'),
    'datafile1': _('Data file'),
    'errorfile1': _('Error file'),
    'maskfile1': _('Mask file'),
    'dataset2_type': _('Type'),
    'datafile2': _('Data file'),
    'errorfile2': _('Error file'),
    'maskfile2': _('Mask file'),
}


class DataSetForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.id = kwargs.pop('id', None)
        super(DataSetForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DataSet
        fields = FIELDS
        widgets = WIDGET
        labels = LABELS

    def save(self):
        self.full_clean()
        data = self.cleaned_data

        job = Job.objects.get(id=self.id)

        try:
            result = DataSet.objects.create(
                job=job,
                dataset1_type=data.get('dataset1_type'),
                datafile1=data.get('datafile1'),
                errorfile1=data.get('errorfile1'),
                maskfile1=data.get('maskfile1'),
                dataset2_type=data.get('dataset2_type'),
                datafile2=data.get('datafile2'),
                errorfile2=data.get('errorfile2'),
                maskfile2=data.get('maskfile2'),
            )
        except:
            result = DataSet.objects.filter(job_id=id).update(
                dataset1_type=data.get('dataset1_type'),
                datafile1=data.get('datafile1'),
                errorfile1=data.get('errorfile1'),
                maskfile1=data.get('maskfile1'),
                dataset2_type=data.get('dataset2_type'),
                datafile2=data.get('datafile2'),
                errorfile2=data.get('errorfile2'),
                maskfile2=data.get('maskfile2'),
            )

        self.request.session['dataset'] = self.as_array(data)

    def as_array(self, data):
        # 1st batch of files
        file1_dict = {}
        file1_dict['type'] = data.get('dataset1_type')
        file1_dict['data'] = data.get('datafile1.path')
        try:
            file1_dict['error'] = data.get('errorfile1.path')
        except:
            pass
        try:
            file1_dict['mask'] = data.get('maskfile1.path')
        except:
            pass

        # 2nd batch of files
        file2_dict = {}
        try:
            file2_dict['data'] = data.get('datafile2.path')
            file2_dict['type'] = data.get('dataset1_type')
        except:
            pass
        try:
            file2_dict['error'] = data.get('errorfile2.path')
        except:
            pass
        try:
            file2_dict['mask'] = data.get('maskfile2.path')
        except:
            pass

        # Create the array
        result = [file1_dict]

        if bool(file2_dict):
            result.append(file2_dict)

        return result


class EditDataSetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditDataSetForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DataSet
        fields = FIELDS
        widgets = WIDGET
        labels = LABELS

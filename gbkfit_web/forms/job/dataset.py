from django import forms
from gbkfit_web.models import DataSet, Job

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

FIELDS = ['dataset1_type', 'datafile1', 'errorfile1', 'maskfile1',
          'dataset2_type', 'datafile2', 'errorfile2', 'maskfile2',]

class DataSetForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(DataSetForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DataSet
        fields = FIELDS
        widgets = WIDGET

    def save(self):
        self.full_clean()
        data = self.cleaned_data

        id = self.request.session['draft_job']['id']
        job = Job.objects.get(id=id)

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

        self.request.session['dataset'] = DataSet.objects.get(job_id=id).as_array()


class EditDataSetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditDataSetForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DataSet
        fields = FIELDS
        widgets = WIDGET

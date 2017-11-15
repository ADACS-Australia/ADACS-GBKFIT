from rest_framework import serializers
from gbkfit_web.models import (
    Job, DataSet, DataModel, PSF, LSF,
    GalaxyModel, Fitter, ParameterSet,
    Result, Mode, ModeParameters

)
from gbkfit_web.forms.job.params import (
    XO_FIELDS, YO_FIELDS, PA_FIELDS, INCL_FIELDS, VSYS_FIELDS, VSIG_FIELDS, I0_FIELDS, R0_FIELDS,
    RT_FIELDS, VT_FIELDS, A_FIELDS, B_FIELDS
)
from gbkfit_web.utility.utils import check_path
from json import dump as json_dump

class create_task_json:
    def __init__(self, job_id):
        self.job = Job.objects.get(id=job_id)
        self.dmodel = DataModel.objects.get(job_id=job_id)
        self.dataset = DataSet.objects.get(job_id=job_id)
        self.psf = PSF.objects.get(job_id=job_id)
        self.lsf = LSF.objects.get(job_id=job_id)
        self.gmodel = GalaxyModel.objects.get(job_id=job_id)
        self.fitter = Fitter.objects.get(job_id=job_id)
        self.params = ParameterSet.objects.get(job_id=job_id)

    def as_json(self):
        return dict(
            mode='fit',
            dmodel=self.dmodel.as_json(),
            datasets=self.dataset.as_array(),
            psf=self.psf.as_json(),
            lsf=self.lsf.as_json(),
            gmodel=self.gmodel.as_json(),
            fitter=self.fitter.as_json(),
            params=self.params.as_array(),
        )

    def json_to_file(self, path, filename):
        path = check_path(path)
        with open(path + filename, 'w+') as f:
            json_dump(self.as_json(), f)

class JobSerializer(serializers.Serializer):

    class Meta:
        model = DataModel
        fields = ['name', 'description', 'status', 'submission_date']

class DataModelSerializer(serializers.Serializer):
    class Meta:
        model = DataModel
        fields = ['dmodel_type', 'method', 'scale_x', 'scale_y', 'scale_z', 'step_x', 'step_y', 'step_z']

class DataSetSerializer(serializers.Serializer):
    class Meta:
        model = DataSet
        fields = ['dataset1_type', 'datafile1', 'errorfile1', 'maskfile1']

class PSFSerializer(serializers.Serializer):
    class Meta:
        model = PSF
        fields = ['psf_type', 'fwhm_x', 'fwhm_y', 'pa', 'beta']

class LSFSerializer(serializers.Serializer):
    class Meta:
        model = LSF
        fields = ['psf_type', 'fwhm', 'beta']

class GalaxyModelSerializer(serializers.Serializer):
    class Meta:
        model = GalaxyModel
        fields = ['gmodel_type', 'flx_profile', 'vel_profile']

class FitterSerializer(serializers.Serializer):
    class Meta:
        model = Fitter
        fields = ['fitter_type',
          'ftol', 'xtol', 'gtol', 'epsfcn', 'stepfactor', 'covtol', 'mpfit_maxiter', 'maxfev', 'nprint', 'douserscale',
          'nofinitecheck',
          'efr', 'tol', 'ztol', 'logzero', 'multinest_is', 'mmodal', 'ceff', 'nlive', 'multinest_maxiter', 'seed', 'outfile',
          ]

class ParamsSerializer(serializers.Serializer):
    class Meta:
        model = ParameterSet
        fields = [XO_FIELDS, YO_FIELDS, PA_FIELDS, INCL_FIELDS, VSYS_FIELDS, VSIG_FIELDS,
                  I0_FIELDS, R0_FIELDS, RT_FIELDS, VT_FIELDS, A_FIELDS, B_FIELDS]

class ResultSerializer(serializers.Serializer):
    class Meta:
        model = Result
        fields = ['id', 'job_id', 'dof']

class ModeSerializer(serializers.Serializer):
    class Meta:
        model = Mode
        fields = ['id', 'result_id', 'chisqr', 'rchisqr']

class ModeParametersSerializer(serializers.Serializer):
    class Meta:
        model = ModeParameters
        fields = ['id', 'mode_id', 'name', 'value', 'error']

class ResultFileSerializer(serializers.Serializer):
    class Meta:
        model = ModeParameters
        fields = ['id', 'result_id', 'filename']

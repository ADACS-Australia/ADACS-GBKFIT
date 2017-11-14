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

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255, allow_blank=False, allow_null=False)
    description = serializers.CharField(allow_blank=True, allow_null=True)
    status = serializers.CharField(required=False, allow_blank=True, max_length=100)
    creation_time = serializers.DateTimeField(allow_null=True)
    submission_time = serializers.DateTimeField(allow_null=True)

    def create(self, validated_data):
        """
        Create and return a new `Job` instance, given the validated data.
        """
        return Job.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Job` instance, given the validated data.
        """
        instance.status = validated_data.get('status', instance.status)
        instance.submission_time = validated_data.get('submission_time', instance.submission_time)
        instance.save()
        return instance

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
    id = serializers.IntegerField(read_only=True)
    job_id = serializers.IntegerField(read_only=True)
    dof = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        """
        Create and return a new `Result` instance, given the validated data.
        """
        return Result.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Result` instance, given the validated data.
        """
        instance.dof = validated_data.get('dof', instance.dof)
        instance.save()
        return instance

class ModeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    result_id = serializers.IntegerField(read_only=True)
    chisqr = serializers.FloatField(read_only=True)
    rchisqr = serializers.FloatField(read_only=True)

    def create(self, validated_data):
        """
        Create and return a new `Mode` instance, given the validated data.
        """
        return Mode.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Mode` instance, given the validated data.
        """
        instance.chisqr = validated_data.get('chisqr', instance.chisqr)
        instance.rchisqr = validated_data.get('rchisqr', instance.rchisqr)
        instance.save()
        return instance

class ModeParametersSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    mode_id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255, read_only=True)
    value = serializers.FloatField(read_only=True)
    error = serializers.FloatField(read_only=True)

    def create(self, validated_data):
        """
        Create and return a new `ModeParameters` instance, given the validated data.
        """
        return ModeParameters.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `ModeParameters` instance, given the validated data.
        """

        instance.name = validated_data.get('name', instance.name)
        instance.value = validated_data.get('value', instance.value)
        instance.error = validated_data.get('error', instance.error)
        instance.save()
        return instance

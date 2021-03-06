#==============================================================================
#
# This code was developed as part of the Astronomy Data and Computing Services
# (ADACS; https:#adacs.org.au) 2017B Software Support program.
#
# Written by: Dany Vohl, Lewis Lakerink, Shibli Saleheen
# Date:       December 2017
#
# It is distributed under the MIT (Expat) License (see https:#opensource.org/):
#
# Copyright (c) 2017 Astronomy Data and Computing Services (ADACS)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#==============================================================================

from django.core.files import File
from django.core.files.images import ImageFile
from rest_framework import serializers
from gbkfit_web.models import (
    Job, DataSet, DataModel, PSF, LSF,
    GalaxyModel, Fitter, ParameterSet,
    Result, Mode, ModeParameter, ModeImage

)
from gbkfit_web.forms.job.params import (
    XO_FIELDS, YO_FIELDS, PA_FIELDS, INCL_FIELDS, VSYS_FIELDS, VSIG_FIELDS, I0_FIELDS, R0_FIELDS,
    RT_FIELDS, VT_FIELDS, A_FIELDS, B_FIELDS
)
from gbkfit_web.utility.utils import check_path
from json import load as json_load, dump as json_dump


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



def save_job_results(job_id, json):

    job = Job.objects.get(id=job_id)

    result = Result()
    result.job_id = job.id
    result.dof = json['dof']
    result.save()

    # Save modes
    mode_number = 0
    for mode in json['modes']:
        m = Mode()
        m.mode_number = mode_number
        m.result = result
        m.chisqr = mode['chisqr']
        m.rchisqr = mode['rchisqr']
        m.save()

        # Save mode parameters
        for param in mode['parameters']:
            p = ModeParameter()
            p.mode = m
            p.name = param['name']
            p.value = param['value']
            p.error = param['error']
            p.save()

        # Increase mode number
        mode_number += 1


def save_job_image(job_id, mode_number, image_type, image_file_path):
    result = Result.objects.get(job_id=job_id)
    filterargs = {'result__id': result.id, 'mode_number': mode_number}
    mode = Mode.objects.get(**filterargs)
    mode_image = ModeImage()
    mode_image.mode_id = mode.id
    mode_image.image_type = image_type
    mode_image.image_file = image_file_path
    mode_image.save()

####
# Begining of Job serializers
####
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
####
# End of Job serializers
####

####
# Begining of Result serializers
####
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
        model = ModeParameter
        fields = ['id', 'mode_id', 'name', 'value', 'error']

####
# End of Result serializers
####

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import HttpResponse
import json
from gbkfit_web.models import Job
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe


from collections import OrderedDict

from os.path import basename

from gbkfit_web.models import (
    Job, DataSet, DataModel, PSF as PSF_model, LSF as LSF_model,
    GalaxyModel, Fitter as Fitter_model, ParameterSet as Params
)
from gbkfit.settings.local import MEDIA_ROOT

from gbkfit_web.utility.utils import set_dict_indices

"""

    UTILITIES SECTION

"""
START = 'start'
DATASET = 'data-set'
DMODEL = 'data-model'
PSF = 'psf'
LSF = 'lsf'
GMODEL = 'galaxy-model'
FITTER = 'fitter'
PARAMS = 'params'
LAUNCH = 'launch'
TABS = [START,
        DMODEL,
        DATASET,
        PSF,
        LSF,
        GMODEL,
        FITTER,
        PARAMS,
        LAUNCH]
TABS_INDEXES = set_dict_indices(TABS)

RESULT = 'result'
MODE = 'mode'
MODE_PARAMS = 'mode_parameter'
RESULT_FILE = 'result_file'

RESULTS_PARTS = [RESULT,
                MODE,
                MODE_PARAMS,
                RESULT_FILE]
RESULTS_PARTS_INDEXES = set_dict_indices(RESULTS_PARTS)

"""

    JOB DETAIL/LIST SECTION

"""
class JobDetailView(DetailView):
    model = Job

    def get_context_data(self, **kwargs):
        context = super(JobDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class JobListView(ListView):

    model = Job

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(JobListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

def delete_job(request, id):
    Job.objects.get(pk=id).delete()
    # return response(request)

    if request.method == 'POST' and request.is_ajax():
        return HttpResponse(json.dumps({'message': 'Job {} deleted'.format(id)}), content_type="application/json")

class JobDetailView(DetailView):
    model = Job
    # queryset = Job.objects.get(id=id)

    def get_context_data(self, **kwargs):
        id = self.kwargs['pk']
        context = super(JobDetailView, self).get_context_data(**kwargs)
        context['data_model'] = DataModel.objects.get(job_id=id)
        context['dataset']= DataSet.objects.get(job_id=id)
        context['psf']= PSF_model.objects.get(job_id=id)
        context['lsf']= LSF_model.objects.get(job_id=id)
        context['galaxy_model']= GalaxyModel.objects.get(job_id=id)
        context['fitter']= Fitter_model.objects.get(job_id=id)
        context['params']= Params.objects.get(job_id=id)
        context['now'] = timezone.now()

        return context

"""

    JOB DETAIL/LIST SECTION

"""
def model_instance_to_iterable(object, model=START, views=[]):
    """
    Converts the object returned from a Model query into an iterable object to be used by a template

    :param object: object returned from a Model query
    :param model: Model to be considered (using the tabs convention used in job.py)
    :param views: list of views currently active
    :return: the newly iterable object, or None.
    """
    fields, labels = get_meta(model, views, object)

    try:
        object.fields = OrderedDict(((field.name, [labels[field.name], field.value_to_string(object)])
                             if 'file' not in field.name else
                                     ((field.name, [labels[field.name], basename(field.value_to_string(object))])
                                      if 'filename' not in field.name else
                                      (field.name, [labels[field.name], field.value_to_string(object)])
                                      )
                                     )
                             for field in object._meta.fields if field.name in fields)

        return object
    except:
        return None

def get_meta(model, views, object):
    """
    Get metadata about a model (e.g. fields and labels to be displayed by a template.)
    :param model: Model to be considered (using the tabs convention used in job.py)
    :param views: list of views currently active
    :param object: object returned from a Model query
    :return: fields, labels
    """
    if model == START:
        fields = ['name', 'description']
        labels = {'name': _('Job name'), 'description': _('Job description')}

    if model == DMODEL:
        fields = ['dmodel_type', 'method', 'scale_x', 'scale_y', 'scale_z', 'step_x', 'step_y', 'step_z']
        fields = filter_data_model_fields(fields, object)

        labels = {
            'dmodel_type': _('Type'),
            'method': _('Method'),
            'scale_x': _('Scale X'),
            'scale_y': _('Scale Y'),
            'scale_z': _('Scale Z'),
            'step_x': _('Step X'),
            'step_y': _('Step Y'),
            'step_z': _('Step Z'),
        }

    if model == DATASET:
        fields = ['dataset1_type', 'datafile1', 'errorfile1', 'maskfile1',
                  'dataset2_type', 'datafile2', 'errorfile2', 'maskfile2',]
        labels = {
            'dataset1_type': _('Type'),
            'datafile1': _('Data file'),
            'errorfile1': _('Error file'),
            'maskfile1': _('Mask file'),
            'dataset2_type': _('Type'),
            'datafile2': _('Data file'),
            'errorfile2': _('Error file'),
            'maskfile2': _('Mask file'),
        }

    if model == PSF:
        fields = ['psf_type', 'fwhm_x', 'fwhm_y', 'pa', 'beta']
        fields = filter_psf_fields(fields, object)

        labels = {
            'psf_type': _('Type'),
            'fwhm_x': _('FWHM X'),
            'fwhm_y': _('FWHM Y'),
            'pa': _('PA'),
            'beta': _('Beta'),
        }

    if model == LSF:
        fields = ['lsf_type', 'fwhm', 'beta']
        fields = filter_lsf_fields(fields, object)

        labels = {
            'lsf_type': _('Type'),
            'fwhm': _('FWHM'),
            'beta': _('Beta'),
        }

    if model == GMODEL:
        fields = ['gmodel_type', 'flx_profile', 'vel_profile']
        labels = {
            'gmodel_type': _('Type'),
            'flx_profile': _('Flux profile'),
            'vel_profile': _('Velocity profile'),
        }

    if model == FITTER:
        fields = ['fitter_type',
          'ftol', 'xtol', 'gtol', 'epsfcn', 'stepfactor', 'covtol', 'mpfit_maxiter', 'maxfev', 'nprint', 'douserscale',
          'nofinitecheck',
          'efr', 'tol', 'ztol', 'logzero', 'multinest_is', 'mmodal', 'ceff', 'nlive', 'multinest_maxiter', 'seed', 'outfile',
          ]
        fields = filter_fitter_fields(fields, object)

        labels = {
            'fitter_type': _('Type'),
            'ftol': _('Chi-square criterium'),
            'xtol': _('Parameter criterium'),
            'gtol': _('Orthogonality criterium'),
            'epsfcn': _('Derivative step size'),
            'stepfactor': _('Initial step bound'),
            'covtol': _('Covariance tolerance'),
            'mpfit_maxiter': _('Maximum iterations'),
            'maxfev': _('Maximum function evaluations'),
            'nprint': _('Print information to stdout'),
            'douserscale': _('Scale variables'),
            'nofinitecheck': _('Check for infinite quantities'),

            'efr': _('Sampling efficiency'),
            'tol': _('Evidence tolerance'),
            'ztol': _('Null log-evidence'),
            'logzero': _('Log-zero'),
            'multinest_is': _('Importance Nested Sampling'),
            'mmodal': _('Mode separation'),
            'ceff': _('Constant efficiency'),
            'nlive': _('Live points'),
            'multinest_maxiter': _('Maximum iterations'),
            'seed': _('Seed'),
            'outfile': _('Output to file'),
        }

    if model == PARAMS:
        fields = filter_params_fields(get_ParamsFields(),
                                      object,
                                      views[TABS_INDEXES[GMODEL]],
                                      views[TABS_INDEXES[FITTER]])

        labels = ParamsMeta.LABELS

    if model == RESULT:
        fields = ['dof']
        labels = {'dof': _('Degree of freedom'),}

    if model == MODE:
        fields = [#'chisqr',
                  'rchisqr']
        labels = {#'chisqr': _(mark_safe('&Chi;<sup>2</sup>')),
                  'rchisqr': _(mark_safe('Reduced &Chi;<sup>2</sup>'))}

    if model == MODE_PARAMS:
        fields = ['name', 'value', 'error']
        labels = {'name': _('Name'),
                  'value': _('Value'),
                  'error': _('Error')}

    if model == RESULT_FILE:
        # This will have to be changed to gather the actual file!
        fields = ['filename',
                  #'filetype'
                 ]
        labels = {'filename': _('File name'),
                  #'filetype': _('File type')
                  }

    return fields, labels

def add_fields_to_object(object, fields):
    object.fields = OrderedDict((field.name, field.value_to_string(object))
                         for field in object._meta.fields if field.name in fields)
    return object

def filter_data_model_fields(fields, object):
    object = add_fields_to_object(object, fields)

    fields_loop = fields.copy()
    for field in fields_loop:
        if 'mmaps' in object.fields['dmodel_type']:
            if 'z' in field:
                if field in fields: fields.remove(field)

    return fields

def filter_dataset_fields(fields, object):
    pass

def filter_psf_fields(fields, object):
    object = add_fields_to_object(object, fields)

    fields_loop = fields.copy()
    for field in fields_loop:
        if object.fields['psf_type'] != PSF_model.MOFFAT:
            if 'beta' in field:
                fields.remove(field)

    return fields

def filter_lsf_fields(fields, object):
    object = add_fields_to_object(object, fields)

    fields_loop = fields.copy()
    for field in fields_loop:
        if object.fields['lsf_type'] != PSF_model.MOFFAT:
            if 'beta' in field:
                fields.remove(field)

    return fields

def filter_galaxy_model_fields(fields, object):
    pass

def filter_fitter_fields(fields, object):
    object = add_fields_to_object(object, fields)

    mpfit_fields = ['ftol', 'xtol', 'gtol', 'epsfcn', 'stepfactor', 'covtol', 'mpfit_maxiter',
                        'maxfev', 'nprint', 'douserscale', 'nofinitecheck']


    multinest_fields = ['efr', 'tol', 'ztol', 'logzero', 'multinest_is', 'mmodal', 'ceff', 'nlive',
                    'multinest_maxiter', 'seed', 'outfile']

    fields_loop = fields.copy()
    for field in fields_loop:
        if object.fields['fitter_type'] == Fitter_model.MULTINEST:
            if field in mpfit_fields:
                fields.remove(field)
        if object.fields['fitter_type'] == Fitter_model.MPFIT:
            if field in multinest_fields:
                fields.remove(field)

    return fields

def filter_params_fields(fields, object, galaxy_model, fitter):
    object = add_fields_to_object(object, fields)

    if fitter.fields['fitter_type'][1] == Fitter_model.MPFIT:
        """
        Doesn't use:
            - wrap
        """
        for fields_list in ParamsMeta.FIELDS_LISTS:
            for field in fields_list:
                if 'wrap' in field:
                    if field in fields: fields.remove(field)

    if fitter.fields['fitter_type'][1] == Fitter_model.MULTINEST:
        """
        Doesn't use:
            - step 
            - relstep 
            - side
        """
        for fields_list in ParamsMeta.FIELDS_LISTS:
            for field in fields_list:
                if 'step' in field or 'relstep' in field or 'side' in field:
                    if field in fields:
                        fields.remove(field)

    for fields_list in ParamsMeta.FIELDS_LISTS:
        for field in fields_list:
            prefix = field.split('_')[0]
            try:
                if object.fields[prefix + '_fixed'] == 'True':
                    if 'value' not in field:
                        if field in fields:
                            fields.remove(field)
                else:
                    if fitter.fields['fitter_type'] == Fitter_model.MULTINEST:
                        if 'value' in field:
                            if field in fields:
                                fields.remove(field)
            except KeyError as e:
                pass


    if galaxy_model.fields['vel_profile'][1] != GalaxyModel.EPINAT:
        for field in ParamsMeta.A_FIELDS:
            if field in fields:
                fields.remove(field)
        for field in ParamsMeta.B_FIELDS:
            if field in fields:
                fields.remove(field)

    return fields

class ParamsMeta:
    XO_FIELDS = ['xo_fixed', 'xo_value', 'xo_min', 'xo_max', 'xo_wrap', 'xo_step', 'xo_relstep', 'xo_side', ]
    YO_FIELDS = ['yo_fixed', 'yo_value', 'yo_min', 'yo_max', 'yo_wrap', 'yo_step', 'yo_relstep', 'yo_side', ]
    PA_FIELDS = ['xo_fixed', 'xo_value', 'xo_min', 'xo_max', 'xo_wrap', 'xo_step', 'xo_relstep', 'xo_side', ]
    INCL_FIELDS = ['incl_fixed', 'incl_value', 'incl_min', 'incl_max', 'incl_wrap', 'incl_step', 'incl_relstep',
                   'incl_side', ]
    VSYS_FIELDS = ['vsys_fixed', 'vsys_value', 'vsys_min', 'vsys_max', 'vsys_wrap', 'vsys_step', 'vsys_relstep',
                   'vsys_side', ]
    VSIG_FIELDS = ['vsig_fixed', 'vsig_value', 'vsig_min', 'vsig_max', 'vsig_wrap', 'vsig_step', 'vsig_relstep',
                   'vsig_side', ]
    I0_FIELDS = ['i0_fixed', 'i0_value', 'i0_min', 'i0_max', 'i0_wrap', 'i0_step', 'i0_relstep', 'i0_side', ]
    R0_FIELDS = ['r0_fixed', 'r0_value', 'r0_min', 'r0_max', 'r0_wrap', 'r0_step', 'r0_relstep', 'r0_side', ]
    RT_FIELDS = ['rt_fixed', 'rt_value', 'rt_min', 'rt_max', 'rt_wrap', 'rt_step', 'rt_relstep', 'rt_side', ]
    VT_FIELDS = ['vt_fixed', 'vt_value', 'vt_min', 'vt_max', 'vt_wrap', 'vt_step', 'vt_relstep', 'vt_side', ]
    A_FIELDS = ['a_fixed', 'a_value', 'a_min', 'a_max', 'a_wrap', 'a_step', 'a_relstep', 'a_side', ]
    B_FIELDS = ['b_fixed', 'b_value', 'b_min', 'b_max', 'b_wrap', 'b_step', 'b_relstep', 'b_side', ]

    FIELDS_LISTS = [XO_FIELDS, YO_FIELDS, PA_FIELDS, INCL_FIELDS, VSYS_FIELDS, VSIG_FIELDS,
                    I0_FIELDS, R0_FIELDS, RT_FIELDS, VT_FIELDS, A_FIELDS, B_FIELDS]

    LABELS = {
        #xo
        'xo_fixed': _('Fixed'),
        'xo_value': _('Value'),
        'xo_min': _('Minimum'),
        'xo_max': _('Maximum'),
        'xo_wrap': _('Wrap'),
        'xo_step': _('Step'),
        'xo_relstep': _('Relstep'),
        'xo_side': _('Side'),

        #yo
        'yo_fixed': _('Fixed'),
        'yo_value': _('Value'),
        'yo_min': _('Minimum'),
        'yo_max': _('Maximum'),
        'yo_wrap': _('Wrap'),
        'yo_step': _('Step'),
        'yo_relstep': _('Relstep'),
        'yo_side': _('Side'),

        #pa
        'pa_fixed': _('Fixed'),
        'pa_value': _('Value'),
        'pa_min': _('Minimum'),
        'pa_max': _('Maximum'),
        'pa_wrap': _('Wrap'),
        'pa_step': _('Step'),
        'pa_relstep': _('Relstep'),
        'pa_side': _('Side'),

        #incl
        'incl_fixed': _('Fixed'),
        'incl_value': _('Value'),
        'incl_min': _('Minimum'),
        'incl_max': _('Maximum'),
        'incl_wrap': _('Wrap'),
        'incl_step': _('Step'),
        'incl_relstep': _('Relstep'),
        'incl_side': _('Side'),

        #vsys
        'vsys_fixed': _('Fixed'),
        'vsys_value': _('Value'),
        'vsys_min': _('Minimum'),
        'vsys_max': _('Maximum'),
        'vsys_wrap': _('Wrap'),
        'vsys_step': _('Step'),
        'vsys_relstep': _('Relstep'),
        'vsys_side': _('Side'),

        #vsig
        'vsig_fixed': _('Fixed'),
        'vsig_value': _('Value'),
        'vsig_min': _('Minimum'),
        'vsig_max': _('Maximum'),
        'vsig_wrap': _('Wrap'),
        'vsig_step': _('Step'),
        'vsig_relstep': _('Relstep'),
        'vsig_side': _('Side'),

        'i0_fixed': _('Fixed'),
        'i0_value': _('Value'),
        'i0_min': _('Minimum'),
        'i0_max': _('Maximum'),
        'i0_wrap': _('Wrap'),
        'i0_step': _('Step'),
        'i0_relstep': _('Relstep'),
        'i0_side': _('Side'),

        #r0
        'r0_fixed': _('Fixed'),
        'r0_value': _('Value'),
        'r0_min': _('Minimum'),
        'r0_max': _('Maximum'),
        'r0_wrap': _('Wrap'),
        'r0_step': _('Step'),
        'r0_relstep': _('Relstep'),
        'r0_side': _('Side'),

        #rt
        'rt_fixed': _('Fixed'),
        'rt_value': _('Value'),
        'rt_min': _('Minimum'),
        'rt_max': _('Maximum'),
        'rt_wrap': _('Wrap'),
        'rt_step': _('Step'),
        'rt_relstep': _('Relstep'),
        'rt_side': _('Side'),

        #vt
        'vt_fixed': _('Fixed'),
        'vt_value': _('Value'),
        'vt_min': _('Minimum'),
        'vt_max': _('Maximum'),
        'vt_wrap': _('Wrap'),
        'vt_step': _('Step'),
        'vt_relstep': _('Relstep'),
        'vt_side': _('Side'),

        #a
        'a_fixed': _('Fixed'),
        'a_value': _('Value'),
        'a_min': _('Minimum'),
        'a_max': _('Maximum'),
        'a_wrap': _('Wrap'),
        'a_step': _('Step'),
        'a_relstep': _('Relstep'),
        'a_side': _('Side'),

        #b
        'b_fixed': _('Fixed'),
        'b_value': _('Value'),
        'b_min': _('Minimum'),
        'b_max': _('Maximum'),
        'b_wrap': _('Wrap'),
        'b_step': _('Step'),
        'b_relstep': _('Relstep'),
        'b_side': _('Side'),
    }

def get_ParamsFields():
    fields = []
    for fields_list in ParamsMeta.FIELDS_LISTS:
        for field in fields_list:
            fields.append(field)

    return fields

# def job_overview(request, id):
#     all_models_dict = {
#         "template_name": "contacts/index.html",
#         "job_root": Job.objects.get(id=id),
#         "extra_context": {"data_model": DataModel.objects.get(job_id=id),
#                           "dataset": DataSet.objects.get(job_id=id),
#                           "psf": PSF_model.objects.get(job_id=id),
#                           "lsf": LSF_model.objects.get(job_id=id),
#                           "galaxy_model": GalaxyModel.objects.get(job_id=id),
#                           "fitter": Fitter_model.objects.get(job_id=id),
#                           "params": Params.objects.get(job_id=id),
#                           }
#     }


# class JobDetailView(DetailView):
#     model = Job
#     # queryset = Job.objects.get(id=id)
#
#     def get_context_data(self, **kwargs):
#         id = self.kwargs['pk']
#         context = super(JobDetailView, self).get_context_data(**kwargs)
#         context['data_model'] = DataModel.objects.get(job_id=id)
#         context['dataset']= DataSet.objects.get(job_id=id)
#         context['psf']= PSF_model.objects.get(job_id=id)
#         context['lsf']= LSF_model.objects.get(job_id=id)
#         context['galaxy_model']= GalaxyModel.objects.get(job_id=id)
#         context['fitter']= Fitter_model.objects.get(job_id=id)
#         context['params']= Params.objects.get(job_id=id)
#         context['now'] = timezone.now()
#
#         return context
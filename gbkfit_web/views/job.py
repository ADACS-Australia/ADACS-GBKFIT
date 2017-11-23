from __future__ import unicode_literals

import json
from os.path import basename

from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib import messages

from django.http import HttpResponse, JsonResponse
from wsgiref.util import FileWrapper
import os

from django.shortcuts import render, redirect
from gbkfit_web.forms.job.dataset import DataSetForm, EditDataSetForm
from gbkfit_web.forms.job.job_initial import JobInitialForm, EditJobForm
from gbkfit_web.forms.job.data_model import DataModelForm, EditDataModelForm
from gbkfit_web.forms.job.psf import PSFForm, EditPSFForm
from gbkfit_web.forms.job.lsf import LSFForm, EditLSFForm
from gbkfit_web.forms.job.galaxy_model import GalaxyModelForm, EditGalaxyModelForm
from gbkfit_web.forms.job.fitter import FitterForm, EditFitterForm
from gbkfit_web.forms.job.params import ParamsForm, EditParamsForm
from gbkfit_web.models import (
    Job, DataSet, DataModel, PSF as PSF_model, LSF as LSF_model,
    GalaxyModel, Fitter as Fitter_model, ParameterSet as Params,
    Result, Mode, ModeParameter, ResultFile,
    user_job_input_file_directory_path
)

# from gbkfit.settings.local import MAX_FILE_SIZE

from gbkfit_web.views.job_info import model_instance_to_iterable
from gbkfit_web.utility.utils import set_dict_indices


"""

    UTILITIES SECTION

"""

# Job Creation/Edit/Summary related
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

FORMS_NEW = {START: JobInitialForm,
             DMODEL: DataModelForm,
             DATASET: DataSetForm,
             PSF: PSFForm,
             LSF: LSFForm,
             GMODEL: GalaxyModelForm,
             FITTER: FitterForm,
             PARAMS: ParamsForm}

FORMS_EDIT = {START: EditJobForm,
              DMODEL: EditDataModelForm,
              DATASET: EditDataSetForm,
              PSF: EditPSFForm,
              LSF: EditLSFForm,
              GMODEL: EditGalaxyModelForm,
              FITTER: EditFitterForm,
              PARAMS: EditParamsForm}

MODELS_EDIT = {START: Job,
               DMODEL: DataModel,
               DATASET: DataSet,
               PSF: PSF_model,
               LSF: LSF_model,
               GMODEL: GalaxyModel,
               FITTER: Fitter_model,
               PARAMS: Params}

# Job results related
RESULT = 'result'
MODE = 'mode'
MODE_PARAMS = 'mode_parameter'
RESULT_FILE = 'result_file'

RESULTS_PARTS = [RESULT,
                MODE,
                MODE_PARAMS,
                RESULT_FILE]
RESULTS_PARTS_INDEXES = set_dict_indices(RESULTS_PARTS)

MODELS_RESULTS = {START: Job,
                  RESULT: Result,
                  MODE: Mode,
                  MODE_PARAMS: ModeParameter,
                  RESULT_FILE: ResultFile}


def set_list(l, i, v):
    """
    Set a value v at index i in list l.
    :param l: list
    :param i: index
    :param v: value
    :return: appended list
    """
    try:
        l[i] = v
    except IndexError:
        for _ in range(i - len(l) + 1):
            l.append(None)
        l[i] = v

def previous_tab(active_tab):
    return TABS[TABS_INDEXES[active_tab] - 1]

def next_tab(active_tab):
    return TABS[TABS_INDEXES[active_tab] + 1]

def set_job_menu(request, id=None):
    if id == None:
        return forms.ModelChoiceField(
            label=_('Select Job'),
            queryset=Job.objects.filter(user=request.user, status=Job.DRAFT),
            empty_label=_('New'),
            widget=forms.Select(
                attrs={'class': 'form-control'},
            ),
            required=False,
        )
    else:
        return forms.ModelChoiceField(
            label=_('Select Job'),
            queryset=Job.objects.filter(user=request.user, status=Job.DRAFT, id=id),
            empty_label=_('New'),
            widget=forms.Select(
                attrs={'class': 'form-control'},
            ),
            required=False,
        )

def build_task_json(request):
    # try:
    #     id = request.session['draft_job']['id']
    # except:
    #     id = request.user.id

    # job = Job.objects.get(id=id)
    # dataset = DataSet.objects.get(job_id=id)
    # dmodel = DataModel.objects.get(job_id=id)
    # psf = PSF_model.objects.get(job_id=id)
    # lsf = LSF_model.objects.get(job_id=id)
    # gmodel = GalaxyModel.objects.get(job_id=id)
    # fitter = Fitter_model.objects.get(job_id=id)
    # params = Params.objects.get(job_id=id)

    # task_json = dict(
    #     job=request.session['draft_job'],
    #     task=
    #     dict(
    #         mode='fit',
    #         dmodel=request.session['data_model'],
    #         datasets=request.session['dataset'],
    #         psf=request.session['psf'],
    #         lsf=request.session['lsf'],
    #         gmodel=request.session['galaxy_model'],
    #         fitter=request.session['fitter'],
    #         params=request.session['params'],
    #     )
    # )

    dmodel = request.session.get('data_model', None)
    dataset = request.session.get('dataset', None)
    psf = request.session.get('psf', None)
    lsf = request.session.get('lsf', None)
    gmodel = request.session.get('galaxy_model', None)
    fitter = request.session.get('fitter', None)
    params = request.session.get('params', None)

    task_json = dict(
        mode='fit',
        dmodel=dmodel,
        datasets=dataset,
        psf=psf,
        lsf=lsf,
        gmodel=gmodel,
        fitter=fitter,
        params=params,
    )

    # with open('test.json', 'w+') as outfile:
    #     json.dump(task_json, outfile)

    return json.dumps(task_json)

"""

    JOB CREATION/EDITING  SECTION

"""
def save_form(form, request, active_tab, id=None):
    if active_tab == DATASET:
        try:
            dataset = DataSet.objects.get(job_id=id)
            if dataset.datafile1 == None:
                messages.error(request, "Data file 1 is required. Please upload one.")
            else:
                if 'next' in request.POST:
                    active_tab = next_tab(active_tab)
                if 'previous' in request.POST:
                    active_tab = previous_tab(active_tab)
        except:
            # raise forms.ValidationError({'datafile1': ['Data file is required. Please upload one.']})
            messages.error(request, "Data file 1 is required. Please upload one.")
    if 'skip' in request.POST:
        active_tab = next_tab(active_tab)
    elif form.is_valid():
        form.save()
        if 'next' in request.POST:
            active_tab = next_tab(active_tab)
        if 'previous' in request.POST:
            active_tab = previous_tab(active_tab)
    return active_tab

def act_on_request_method_edit(request, active_tab, id):
    # JobInitialForm.base_fields['job'] = set_job_menu(request, id)

    tab_checker = active_tab
    instance = None
    get_instance = False

    # ACTIVE TAB
    if active_tab != LAUNCH:
        if request.method == 'POST':
            if active_tab == START:
                instance = MODELS_EDIT[active_tab].objects.get(id=id)
                form = FORMS_EDIT[active_tab](request.POST,
                                              instance=instance,
                                              request=request,
                                              job_id=id)
            else:
                if active_tab == DATASET:
                    try:
                        if request.FILES['datafile1']:
                            form = FORMS_NEW[active_tab](request.POST, request.FILES, request=request, id=id)
                        else:
                            form = FORMS_NEW[active_tab](request=request, id=id)
                    except:
                        form = FORMS_NEW[active_tab](request=request, id=id)
                else:
                    try:
                        # Update
                        instance = MODELS_EDIT[active_tab].objects.get(job_id=id)
                        form = FORMS_EDIT[active_tab](request.POST,
                                                      instance=instance,
                                                      request=request,
                                                      job_id=id)
                    except:
                        # Create
                        form = FORMS_NEW[active_tab](request.POST, request=request, id=id)
                        get_instance = True


            active_tab = save_form(form, request, active_tab, id)
            if get_instance:
                if 'next' in request.POST:
                    instance = MODELS_EDIT[previous_tab(active_tab)].objects.get(job_id=id)
                if 'previous' in request.POST:
                    instance = MODELS_EDIT[next_tab(active_tab)].objects.get(job_id=id)


        else:
            if active_tab == START:
                instance = MODELS_EDIT[active_tab].objects.get(id=id)
                form = FORMS_EDIT[active_tab](instance=instance, request=request, job_id=id)
            else:
                try:
                    instance = MODELS_EDIT[active_tab].objects.get(job_id=id)
                    form = FORMS_EDIT[active_tab](instance=instance, request=request, job_id=id)
                except:
                    form = FORMS_NEW[active_tab](request=request, id=id)
    else:
        # Job is being submitted, write the json descriptor for this job

        job = Job.objects.get(id=id)

        # Create the task json descriptor
        task_json = {}
        task_json['mode'] = 'fit'
        task_json['dmodel'] = job.job_data_model.as_json()
        task_json['datasets'] = job.job_data_set.as_array()
        # PSF and LSF are optional.
        try:
            task_json['psf'] = job.job_psf.as_json()
        except:
            pass
        try:
            task_json['lsf'] = job.job_lsf.as_json()
        except:
            pass
        task_json['gmodel'] = job.job_gmodel.as_json()
        task_json['fitter'] = job.job_fitter.as_json()
        task_json['params'] = job.job_parameter_set.as_array()

        # Make sure the directory exists to write the json output
        os.makedirs(os.path.dirname(user_job_input_file_directory_path(job)), exist_ok=True)

        # Write the input json file
        with open(user_job_input_file_directory_path(job), 'w') as outfile:
            json.dump(task_json, outfile)

        if request.method == 'POST':
            job = Job.objects.get(id=id)
            job.user = request.user
            job.status = Job.SUBMITTED
            job.submission_time = now()
            job.save()
            return Job.SUBMITTED, [], []

    # OTHER TABS
    forms = []
    views = []

    job = None
    data_model = None
    dataset = None
    psf = None
    lsf = None
    galaxy_model = None
    fitter = None
    params = None

    if tab_checker != START:
        try:
            job = Job.objects.get(id=id)
            start_form = FORMS_EDIT[START](instance=job, request=request, job_id=id)

        except:
            # If the job is not found, let's go where we can create one!
            return redirect('job_start')
    else:
        start_form = form
        job = instance
    set_list(forms, TABS_INDEXES[START], start_form)
    set_list(views, TABS_INDEXES[START], model_instance_to_iterable(job) if job else None)

    if tab_checker != DMODEL:
        try:
            data_model = DataModel.objects.get(job_id=id)
            data_model_form = FORMS_EDIT[DMODEL](instance=data_model, request=request, job_id=id)
        except:
            data_model_form = FORMS_EDIT[DMODEL](request=request, job_id=id)
    else:
        data_model_form = form
        data_model = instance
    set_list(forms, TABS_INDEXES[DMODEL], data_model_form)
    set_list(views, TABS_INDEXES[DMODEL], model_instance_to_iterable(data_model,
                                                                     model=DMODEL,
                                                                     views=views) if data_model else None)

    if tab_checker != DATASET or tab_checker == DATASET:
        #Always get in here.
        try:
            dataset = DataSet.objects.get(job_id=id)
            dataset_form = FORMS_EDIT[DATASET](instance=dataset, request=request, job_id=id)
        except:
            dataset_form = FORMS_EDIT[DATASET](request=request, job_id=id)
    else:
        dataset_form = form
        dataset = instance
    set_list(forms, TABS_INDEXES[DATASET], dataset_form)
    set_list(views, TABS_INDEXES[DATASET], model_instance_to_iterable(dataset,
                                                                      model=DATASET,
                                                                      views=views) if dataset else None)

    if tab_checker != PSF:
        try:
            psf = PSF_model.objects.get(job_id=id)
            psf_form = FORMS_EDIT[PSF](instance=psf, request=request, job_id=id)
        except:
            psf_form = FORMS_EDIT[PSF](request=request, job_id=id)
    else:
        psf_form = form
        psf = instance
    set_list(forms, TABS_INDEXES[PSF], psf_form)
    set_list(views, TABS_INDEXES[PSF], model_instance_to_iterable(psf,
                                                                  model=PSF,
                                                                  views=views) if psf else None)

    if tab_checker != LSF:
        try:
            lsf = LSF_model.objects.get(job_id=id)
            lsf_form = FORMS_EDIT[LSF](instance=lsf, request=request, job_id=id)
        except:
            lsf_form = FORMS_EDIT[LSF](request=request, job_id=id)
    else:
        lsf_form = form
        lsf = instance
    set_list(forms, TABS_INDEXES[LSF], lsf_form)
    set_list(views, TABS_INDEXES[LSF], model_instance_to_iterable(lsf,
                                                                  model=LSF,
                                                                  views=views) if lsf else None)

    if tab_checker != GMODEL:
        try:
            galaxy_model = GalaxyModel.objects.get(job_id=id)
            galaxy_model_form = FORMS_EDIT[GMODEL](instance=galaxy_model, request=request, job_id=id)
        except:
            galaxy_model_form = FORMS_EDIT[GMODEL](request=request, job_id=id)
    else:
        galaxy_model_form = form
        galaxy_model = instance
    set_list(forms, TABS_INDEXES[GMODEL], galaxy_model_form)
    set_list(views, TABS_INDEXES[GMODEL], model_instance_to_iterable(galaxy_model,
                                                                     model=GMODEL,
                                                                     views=views) if galaxy_model else None)

    if tab_checker != FITTER:
        try:
            fitter = Fitter_model.objects.get(job_id=id)
            fitter_form = FORMS_EDIT[FITTER](instance=fitter, request=request, job_id=id)
        except:
            fitter_form = FORMS_EDIT[FITTER](request=request, job_id=id)
    else:
        fitter_form = form
        fitter = instance
    set_list(forms, TABS_INDEXES[FITTER], fitter_form)
    set_list(views, TABS_INDEXES[FITTER], model_instance_to_iterable(fitter,
                                                                     model=FITTER,
                                                                     views=views) if fitter else None)

    if tab_checker != PARAMS:
        try:
            params = Params.objects.get(job_id=id)
            params_form = FORMS_EDIT[PARAMS](instance=params, request=request, job_id=id)
        except:
            params_form = FORMS_EDIT[PARAMS](request=request, job_id=id)
    else:
        params_form = form
        params = instance
    set_list(forms, TABS_INDEXES[PARAMS], params_form)
    set_list(views, TABS_INDEXES[PARAMS], model_instance_to_iterable(params,
                                                                     model=PARAMS,
                                                                     views=views) if params else None)

    request.session['task'] = build_task_json(request)

    return active_tab, forms, views

@login_required
def start(request):
    active_tab = START
    if request.method == 'POST':
        form = FORMS_NEW[active_tab](request.POST, request=request)
        active_tab = save_form(form, request, active_tab)
    else:
        form = FORMS_NEW[active_tab](request=request)

    if active_tab == START:
        return render(
            request,
            "job/create.html",
            {
                'active_tab': active_tab,
                'disable_other_tabs': True,
                'start_form': form,
            }
        )
    else:
        return redirect('job_data_model_edit', id=request.session['draft_job']['id'])

@login_required
def edit_job_name(request, id):
    active_tab = START
    active_tab, forms, views = act_on_request_method_edit(request, active_tab, id)

    return render(
        request,
        "job/edit.html",
        {
            'job_id': id,
            'active_tab': active_tab,
            'disable_other_tabs': False,

            'start_form': forms[TABS_INDEXES[START]],
            'dataset_form': forms[TABS_INDEXES[DATASET]],
            'data_model_form': forms[TABS_INDEXES[DMODEL]],
            'psf_form': forms[TABS_INDEXES[PSF]],
            'lsf_form': forms[TABS_INDEXES[LSF]],
            'galaxy_model_form': forms[TABS_INDEXES[GMODEL]],
            'fitter_form': forms[TABS_INDEXES[FITTER]],
            'params_form': forms[TABS_INDEXES[PARAMS]],

            'start_view': views[TABS_INDEXES[START]],
            'dataset_view': views[TABS_INDEXES[DATASET]],
            'data_model_view': views[TABS_INDEXES[DMODEL]],
            'psf_view': views[TABS_INDEXES[PSF]],
            'lsf_view': views[TABS_INDEXES[LSF]],
            'galaxy_model_view': views[TABS_INDEXES[GMODEL]],
            'fitter_view': views[TABS_INDEXES[FITTER]],
            'params_view': views[TABS_INDEXES[PARAMS]],
            # 'max_file_size': MAX_FILE_SIZE
        }
    )

@login_required
def edit_job_data_model(request, id):
    active_tab = DMODEL
    active_tab, forms, views = act_on_request_method_edit(request, active_tab, id)

    return render(
        request,
        "job/edit.html",
        {
            'job_id': id,
            'active_tab': active_tab,
            'disable_other_tabs': False,

            'start_form': forms[TABS_INDEXES[START]],
            'dataset_form': forms[TABS_INDEXES[DATASET]],
            'data_model_form': forms[TABS_INDEXES[DMODEL]],
            'psf_form': forms[TABS_INDEXES[PSF]],
            'lsf_form': forms[TABS_INDEXES[LSF]],
            'galaxy_model_form': forms[TABS_INDEXES[GMODEL]],
            'fitter_form': forms[TABS_INDEXES[FITTER]],
            'params_form': forms[TABS_INDEXES[PARAMS]],

            'start_view': views[TABS_INDEXES[START]],
            'dataset_view': views[TABS_INDEXES[DATASET]],
            'data_model_view': views[TABS_INDEXES[DMODEL]],
            'psf_view': views[TABS_INDEXES[PSF]],
            'lsf_view': views[TABS_INDEXES[LSF]],
            'galaxy_model_view': views[TABS_INDEXES[GMODEL]],
            'fitter_view': views[TABS_INDEXES[FITTER]],
            'params_view': views[TABS_INDEXES[PARAMS]],
            # 'max_file_size': MAX_FILE_SIZE
        }
    )

@login_required
def edit_job_dataset(request, id):
    active_tab = DATASET
    active_tab, forms, views = act_on_request_method_edit(request, active_tab, id)

    return render(
        request,
        "job/edit.html",
        {
            'job_id': id,
            'active_tab': active_tab,
            'disable_other_tabs': False,

            'start_form': forms[TABS_INDEXES[START]],
            'dataset_form': forms[TABS_INDEXES[DATASET]],
            'data_model_form': forms[TABS_INDEXES[DMODEL]],
            'psf_form': forms[TABS_INDEXES[PSF]],
            'lsf_form': forms[TABS_INDEXES[LSF]],
            'galaxy_model_form': forms[TABS_INDEXES[GMODEL]],
            'fitter_form': forms[TABS_INDEXES[FITTER]],
            'params_form': forms[TABS_INDEXES[PARAMS]],

            'start_view': views[TABS_INDEXES[START]],
            'dataset_view': views[TABS_INDEXES[DATASET]],
            'data_model_view': views[TABS_INDEXES[DMODEL]],
            'psf_view': views[TABS_INDEXES[PSF]],
            'lsf_view': views[TABS_INDEXES[LSF]],
            'galaxy_model_view': views[TABS_INDEXES[GMODEL]],
            'fitter_view': views[TABS_INDEXES[FITTER]],
            'params_view': views[TABS_INDEXES[PARAMS]],
            # 'max_file_size': MAX_FILE_SIZE
        }
    )

@login_required
def ajax_edit_job_dataset(request, id):
    job = Job.objects.get(id=id)

    filetype = request.POST['filetype']

    # if request.FILES['datafile1']:
    #     form = FORMS_NEW[DATASET](request.POST, request.FILES, request=request, id=id)
    # else:
    #     form = FORMS_NEW[DATASET](request=request, id=id)

    try:
        dataset = DataSet.objects.get(job_id=id)
        if 'datafile1' in request.FILES:
            dataset.datafile1 = request.FILES['datafile1']
        if 'errorfile1' in request.FILES:
            dataset.errorfile1 = request.FILES['errorfile1']
        if 'maskfile1' in request.FILES:
            dataset.maskfile1 = request.FILES['maskfile1']
    except:
        dataset = DataSet()
        dataset.job = job
        if 'datafile1' in request.FILES:
            dataset.datafile1 = request.FILES['datafile1']
        if 'errorfile1' in request.FILES:
            dataset.errorfile1 = request.FILES['errorfile1']
        if 'maskfile1' in request.FILES:
            dataset.maskfile1 = request.FILES['maskfile1']

    try:
        data_file = dataset.save()
        if filetype == 'datafile1':
            data = {'is_valid': True, 'name': basename(dataset.datafile1.name)}
        if filetype == 'errorfile1':
            data = {'is_valid': True, 'name': basename(dataset.errorfile1.name)}
        if filetype == 'maskfile1':
            data = {'is_valid': True, 'name': basename(dataset.maskfile1.name)}
    except:
        data = {'is_valid': False}

    return JsonResponse(data)

@login_required
def edit_job_psf(request, id):
    active_tab = PSF
    active_tab, forms, views = act_on_request_method_edit(request, active_tab, id)

    return render(
        request,
        "job/edit.html",
        {
            'job_id': id,
            'active_tab': active_tab,
            'disable_other_tabs': False,

            'start_form': forms[TABS_INDEXES[START]],
            'dataset_form': forms[TABS_INDEXES[DATASET]],
            'data_model_form': forms[TABS_INDEXES[DMODEL]],
            'psf_form': forms[TABS_INDEXES[PSF]],
            'lsf_form': forms[TABS_INDEXES[LSF]],
            'galaxy_model_form': forms[TABS_INDEXES[GMODEL]],
            'fitter_form': forms[TABS_INDEXES[FITTER]],
            'params_form': forms[TABS_INDEXES[PARAMS]],

            'start_view': views[TABS_INDEXES[START]],
            'dataset_view': views[TABS_INDEXES[DATASET]],
            'data_model_view': views[TABS_INDEXES[DMODEL]],
            'psf_view': views[TABS_INDEXES[PSF]],
            'lsf_view': views[TABS_INDEXES[LSF]],
            'galaxy_model_view': views[TABS_INDEXES[GMODEL]],
            'fitter_view': views[TABS_INDEXES[FITTER]],
            'params_view': views[TABS_INDEXES[PARAMS]],
            # 'max_file_size': MAX_FILE_SIZE
        }
    )

@login_required
def edit_job_lsf(request, id):
    active_tab = LSF
    active_tab, forms, views = act_on_request_method_edit(request, active_tab, id)

    return render(
        request,
        "job/edit.html",
        {
            'job_id': id,
            'active_tab': active_tab,
            'disable_other_tabs': False,

            'start_form': forms[TABS_INDEXES[START]],
            'dataset_form': forms[TABS_INDEXES[DATASET]],
            'data_model_form': forms[TABS_INDEXES[DMODEL]],
            'psf_form': forms[TABS_INDEXES[PSF]],
            'lsf_form': forms[TABS_INDEXES[LSF]],
            'galaxy_model_form': forms[TABS_INDEXES[GMODEL]],
            'fitter_form': forms[TABS_INDEXES[FITTER]],
            'params_form': forms[TABS_INDEXES[PARAMS]],

            'start_view': views[TABS_INDEXES[START]],
            'dataset_view': views[TABS_INDEXES[DATASET]],
            'data_model_view': views[TABS_INDEXES[DMODEL]],
            'psf_view': views[TABS_INDEXES[PSF]],
            'lsf_view': views[TABS_INDEXES[LSF]],
            'galaxy_model_view': views[TABS_INDEXES[GMODEL]],
            'fitter_view': views[TABS_INDEXES[FITTER]],
            'params_view': views[TABS_INDEXES[PARAMS]],
            # 'max_file_size': MAX_FILE_SIZE
        }
    )

@login_required
def edit_job_galaxy_model(request, id):
    active_tab = GMODEL
    active_tab, forms, views = act_on_request_method_edit(request, active_tab, id)

    return render(
        request,
        "job/edit.html",
        {
            'job_id': id,
            'active_tab': active_tab,
            'disable_other_tabs': False,

            'start_form': forms[TABS_INDEXES[START]],
            'dataset_form': forms[TABS_INDEXES[DATASET]],
            'data_model_form': forms[TABS_INDEXES[DMODEL]],
            'psf_form': forms[TABS_INDEXES[PSF]],
            'lsf_form': forms[TABS_INDEXES[LSF]],
            'galaxy_model_form': forms[TABS_INDEXES[GMODEL]],
            'fitter_form': forms[TABS_INDEXES[FITTER]],
            'params_form': forms[TABS_INDEXES[PARAMS]],

            'start_view': views[TABS_INDEXES[START]],
            'dataset_view': views[TABS_INDEXES[DATASET]],
            'data_model_view': views[TABS_INDEXES[DMODEL]],
            'psf_view': views[TABS_INDEXES[PSF]],
            'lsf_view': views[TABS_INDEXES[LSF]],
            'galaxy_model_view': views[TABS_INDEXES[GMODEL]],
            'fitter_view': views[TABS_INDEXES[FITTER]],
            'params_view': views[TABS_INDEXES[PARAMS]],
            # 'max_file_size': MAX_FILE_SIZE
        }
    )

@login_required
def edit_job_fitter(request, id):
    active_tab = FITTER
    active_tab, forms, views = act_on_request_method_edit(request, active_tab, id)

    return render(
        request,
        "job/edit.html",
        {
            'job_id': id,
            'active_tab': active_tab,
            'disable_other_tabs': False,

            'start_form': forms[TABS_INDEXES[START]],
            'dataset_form': forms[TABS_INDEXES[DATASET]],
            'data_model_form': forms[TABS_INDEXES[DMODEL]],
            'psf_form': forms[TABS_INDEXES[PSF]],
            'lsf_form': forms[TABS_INDEXES[LSF]],
            'galaxy_model_form': forms[TABS_INDEXES[GMODEL]],
            'fitter_form': forms[TABS_INDEXES[FITTER]],
            'params_form': forms[TABS_INDEXES[PARAMS]],

            'start_view': views[TABS_INDEXES[START]],
            'dataset_view': views[TABS_INDEXES[DATASET]],
            'data_model_view': views[TABS_INDEXES[DMODEL]],
            'psf_view': views[TABS_INDEXES[PSF]],
            'lsf_view': views[TABS_INDEXES[LSF]],
            'galaxy_model_view': views[TABS_INDEXES[GMODEL]],
            'fitter_view': views[TABS_INDEXES[FITTER]],
            'params_view': views[TABS_INDEXES[PARAMS]],
            # 'max_file_size': MAX_FILE_SIZE
        }
    )

@login_required
def edit_job_params(request, id):
    active_tab = PARAMS
    active_tab, forms, views = act_on_request_method_edit(request, active_tab, id)

    return render(
        request,
        "job/edit.html",
        {
            'job_id': id,
            'active_tab': active_tab,
            'disable_other_tabs': False,

            'start_form': forms[TABS_INDEXES[START]],
            'dataset_form': forms[TABS_INDEXES[DATASET]],
            'data_model_form': forms[TABS_INDEXES[DMODEL]],
            'psf_form': forms[TABS_INDEXES[PSF]],
            'lsf_form': forms[TABS_INDEXES[LSF]],
            'galaxy_model_form': forms[TABS_INDEXES[GMODEL]],
            'fitter_form': forms[TABS_INDEXES[FITTER]],
            'params_form': forms[TABS_INDEXES[PARAMS]],

            'start_view': views[TABS_INDEXES[START]],
            'dataset_view': views[TABS_INDEXES[DATASET]],
            'data_model_view': views[TABS_INDEXES[DMODEL]],
            'psf_view': views[TABS_INDEXES[PSF]],
            'lsf_view': views[TABS_INDEXES[LSF]],
            'galaxy_model_view': views[TABS_INDEXES[GMODEL]],
            'fitter_view': views[TABS_INDEXES[FITTER]],
            'params_view': views[TABS_INDEXES[PARAMS]],
            # 'max_file_size': MAX_FILE_SIZE
        }
    )

@login_required
def launch(request, id):
    active_tab = LAUNCH
    active_tab, forms, views = act_on_request_method_edit(request, active_tab, id)

    if active_tab != Job.SUBMITTED:
        return render(
            request,
            "job/edit.html",
            {
                'job_id': id,
                'active_tab': active_tab,
                'disable_other_tabs': False,

                'start_form': forms[TABS_INDEXES[START]],
                'dataset_form': forms[TABS_INDEXES[DATASET]],
                'data_model_form': forms[TABS_INDEXES[DMODEL]],
                'psf_form': forms[TABS_INDEXES[PSF]],
                'lsf_form': forms[TABS_INDEXES[LSF]],
                'galaxy_model_form': forms[TABS_INDEXES[GMODEL]],
                'fitter_form': forms[TABS_INDEXES[FITTER]],
                'params_form': forms[TABS_INDEXES[PARAMS]],

                'start_view': views[TABS_INDEXES[START]],
                'dataset_view': views[TABS_INDEXES[DATASET]],
                'data_model_view': views[TABS_INDEXES[DMODEL]],
                'psf_view': views[TABS_INDEXES[PSF]],
                'lsf_view': views[TABS_INDEXES[LSF]],
                'galaxy_model_view': views[TABS_INDEXES[GMODEL]],
                'fitter_view': views[TABS_INDEXES[FITTER]],
                'params_view': views[TABS_INDEXES[PARAMS]],
                # 'max_file_size': MAX_FILE_SIZE
            }
        )
    else:
        return redirect('job_list')

    # task_json = build_task_json(request)
    #
    # request.session['task'] = task_json
    #
    # return HttpResponse(task_json, content_type='application/json')

"""

    JOB RESULTS

"""

def get_model_objects(model, job_id):
    return MODELS_RESULTS[model].objects.filter(job_id=job_id)

def set_iterable_views(model, views, instance):
    return set_list(views, RESULTS_PARTS_INDEXES[model], model_instance_to_iterable(instance,
                                                                      model=model,
                                                                      views=views) if instance else None)

# Should require that you have access to this job id too.
@login_required
def results(request, id):
    active_tab = LAUNCH
    # This could be cleaned to avoid getting forms and only gather the one view we need
    # (which also requires info from gmodel and fitter).
    active_tab, forms, views = act_on_request_method_edit(request, active_tab, id)

    job = model_instance_to_iterable(Job.objects.get(id=id), model=START)
    job.result = model_instance_to_iterable(Result.objects.get(job_id=id), model=RESULT)

    filterargs = {'result__id': job.result.id, 'filetype': ResultFile.IMAGE_FILE}
    job.result.image_field = model_instance_to_iterable(ResultFile.objects.filter(**filterargs), model=RESULT_FILE)

    job.result.modes = {}
    i=0
    for mode in Mode.objects.filter(result__id = job.result.id):
        job.result.modes[i] = model_instance_to_iterable(mode, model=MODE)
        job.result.modes[i].params = {}
        j=0
        for params in ModeParameter.objects.filter(mode__id=job.result.modes[i].id):
            job.result.modes[i].params[j] = model_instance_to_iterable(params, model=MODE_PARAMS)
            j+=1
        i+=1

    return render(
        request,
        "job/job_result.html",
        {
            'job_id': id,
            'job_view': job,
            'params_view': views[TABS_INDEXES[PARAMS]],
        }
    )

@login_required
def download_results_tar(request, id):

    print ("job_id", id)

    # job = Job.objects.get(id=id)
    result = Result.objects.get(job_id = id)

    filterargs = {'result__id': result.id, 'filetype': ResultFile.TAR_FILE}
    tar_file = ResultFile.objects.filter(**filterargs)
    # filename = 'job_{}_results.tar'.format(job.id)
    content = FileWrapper(tar_file.file)
    response = HttpResponse(content, content_type='application/gzip')
    response['Content-Length'] = tar_file.size
    response['Content-Disposition'] = 'attachment; filename=%s' % tar_file.name
    return response

@login_required
def job_overview(request, id):
    active_tab = LAUNCH
    # This could be cleaned to avoid getting forms and only gather views.
    active_tab, forms, views = act_on_request_method_edit(request, active_tab, id)

    return render(
        request,
        "job/job_overview.html",
        {
            'job_id': id,

            'start_view': views[TABS_INDEXES[START]],
            'dataset_view': views[TABS_INDEXES[DATASET]],
            'data_model_view': views[TABS_INDEXES[DMODEL]],
            'psf_view': views[TABS_INDEXES[PSF]],
            'lsf_view': views[TABS_INDEXES[LSF]],
            'galaxy_model_view': views[TABS_INDEXES[GMODEL]],
            'fitter_view': views[TABS_INDEXES[FITTER]],
            'params_view': views[TABS_INDEXES[PARAMS]],
        }
    )

@login_required
def job_duplicate(request, id):

    job = Job.objects.get(id = id)
    job.pk = None
    # TODO: Need a mechanism to ensure name unique constraint.
    job.name = job.name + '_copy'
    job.submission_time = None
    job.status = Job.DRAFT
    job.save()

    # Other models may not be existing. In such a case, pass.
    try:
        dmodel = DataModel.objects.get(job_id=id)
        dmodel.pk = None
        dmodel.job_id = job.id
        dmodel.save()
    except:
        pass

    try:
        dataset = DataSet.objects.get(job_id=id)
        dataset.pk = None
        dataset.job_id = job.id
        dataset.save()
    except:
        pass

    try:
        psf = PSF_model.objects.get(job_id=id)
        psf.pk = None
        psf.job_id = job.id
        psf.save()
    except:
        pass

    try:
        lsf = LSF_model.objects.get(job_id=id)
        lsf.pk = None
        lsf.job_id = job.id
        lsf.save()
    except:
        pass

    try:
        gmodel = GalaxyModel.objects.get(job_id=id)
        gmodel.pk = None
        gmodel.job_id = job.id
        gmodel.save()
    except:
        pass

    try:
        fitter = Fitter_model.objects.get(job_id=id)
        fitter.pk = None
        fitter.job_id = job.id
        fitter.save()
    except:
        pass

    try:
        params = Params.objects.get(job_id=id)
        params.pk = None
        params.job_id = job.id
        params.save()
    except:
        pass

    return redirect('job_name_edit', id=job.id)

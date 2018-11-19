# ==============================================================================
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
# ==============================================================================

from __future__ import unicode_literals

import json
from os.path import basename

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404

from django_hpc_job_controller.client.scheduler.status import JobStatus
from gbkfit_web.forms.job.data_model import DataModelForm, EditDataModelForm
from gbkfit_web.forms.job.dataset import DataSetForm, EditDataSetForm
from gbkfit_web.forms.job.fitter import FitterForm, EditFitterForm
from gbkfit_web.forms.job.galaxy_model import GalaxyModelForm, EditGalaxyModelForm
from gbkfit_web.forms.job.job_initial import JobInitialForm, EditJobForm
from gbkfit_web.forms.job.lsf import LSFForm, EditLSFForm
from gbkfit_web.forms.job.params import ParamsForm, EditParamsForm
from gbkfit_web.forms.job.psf import PSFForm, EditPSFForm
from gbkfit_web.models import (
    Job, DataSet, DataModel, PSF as PSF_model, LSF as LSF_model,
    GalaxyModel, Fitter as Fitter_model, ParameterSet as Params, Result, Mode, ModeParameter, ModeImage)
# from gbkfit.settings.local import MAX_FILE_SIZE
from gbkfit_web.serializers import save_job_results, save_job_image
from gbkfit_web.utility.utils import set_dict_indices
from gbkfit_web.views.job_info import model_instance_to_iterable

# from gbkfit.settings.local import MEDIA_ROOT, MEDIA_URL


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
SUBMITTED = 'submitted'

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
                  MODE_PARAMS: ModeParameter}


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
    """
    This function is used to access the tab preceding the active tab (global TABS list).
    Given an active_tab (corresponding to one of START, DATASET, ...), it returns the previous element of the array.

    :param active_tab: A tab value (e.g. START, DATASET, DMODEL, ...)
    :return: The previous tab in the TABS list
    """
    return TABS[TABS_INDEXES[active_tab] - 1]


def next_tab(active_tab):
    """
        This function is used to access the tab following the active tab (global TABS list).
        Given an active_tab (corresponding to one of START, DATASET, ...), it returns the previous element of the array.

        :param active_tab: A tab value (e.g. START, DATASET, DMODEL, ...)
        :return: The next tab in the TABS list
        """
    return TABS[TABS_INDEXES[active_tab] + 1]


"""

    JOB CREATION/EDITING  SECTION

"""


def check_permission_save(form, request, active_tab, id):
    """
    Check if user has write permission for the related request

    :param form: current form
    :param request: current request
    :param active_tab: active tab (A tab value (e.g. START, DATASET, DMODEL, ...))
    :param id: job id
    :return: current active tab
    """

    job = Job.objects.get(id=id)
    if job.user_id == request.user.id:
        active_tab = save_form(form, request, active_tab, id)

    return active_tab


def save_form(form, request, active_tab, id=None):
    """
    Save the content of a form to database

    :param form: current form
    :param request: current request
    :param active_tab: active tab
    :param id: job id
    :return: active tab (possibly de/incremented)
    """

    if active_tab == DATASET:
        try:
            dataset = DataSet.objects.get(job_id=id)
            if dataset.datafile1 == None:
                messages.error(request, "Data file 1 is required. Please upload one.")
            else:
                dataset.dataset1_type = request.POST['dataset1_type']
                dataset.dataset2_type = request.POST['dataset2_type']
                dataset.save()

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
    """
    This function acts on a request (post or get). If post, does all the checks and actions to save to database.
    The function also fills a forms and views lists with content to be rendered for each models.

    :param request: current request
    :param active_tab: current active tab
    :param id: job id
    :return: the active_tab, the forms list, and the views list
    """

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

            active_tab = check_permission_save(form, request, active_tab, id)
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
        if 'previous' in request.POST:
            active_tab = previous_tab(active_tab)
        else:
            if request.method == 'POST':
                # Job is being submitted, write the json descriptor for this job
                job = Job.objects.get(id=id)

                # Check write permission
                if job.user_id == request.user.id:
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

                    # Now actually submit the job
                    job.user = request.user
                    job.submit(task_json)

                    return SUBMITTED, [], []

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
        # Always get in here.
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

    return active_tab, forms, views


@login_required
def start(request):
    """
    Start form (job creation)
    :param request: current request (post or get)
    :return: a page to be rendered, or to redirect
    """
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
    """
    Form to edit the job basic information (name, description). It also returns forms to be rendered in other tabs
    (models).

    :param request: current request (post or get)
    :param id: job id
    :return: content to be rendered
    """
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
    """
    Form to edit the data model information. It also returns forms to be rendered in other tabs
    (models).

    :param request: current request (post or get)
    :param id: job id
    :return: content to be rendered
    """
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
    """
    Form to edit the dataset information. It also returns forms to be rendered in other tabs
    (models).

    :param request: current request (post or get)
    :param id: job id
    :return: content to be rendered
    """

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
    """
    Form to edit the dataset information. It returns an ajax response.

    :param request: current request (post)
    :param id: job id
    :return: ajax response
    """

    job = Job.objects.get(id=id)

    filetype = request.POST['filetype']

    try:
        dataset = DataSet.objects.get(job_id=id)
        if 'datafile1' in request.FILES:
            dataset.datafile1 = request.FILES['datafile1']
        if 'errorfile1' in request.FILES:
            dataset.errorfile1 = request.FILES['errorfile1']
        if 'maskfile1' in request.FILES:
            dataset.maskfile1 = request.FILES['maskfile1']
        if 'datafile2' in request.FILES:
            dataset.datafile2 = request.FILES['datafile2']
        if 'errorfile2' in request.FILES:
            dataset.errorfile2 = request.FILES['errorfile2']
        if 'maskfile2' in request.FILES:
            dataset.maskfile2 = request.FILES['maskfile2']
    except:
        dataset = DataSet()
        dataset.job = job
        if 'datafile1' in request.FILES:
            dataset.datafile1 = request.FILES['datafile1']
        if 'errorfile1' in request.FILES:
            dataset.errorfile1 = request.FILES['errorfile1']
        if 'maskfile1' in request.FILES:
            dataset.maskfile1 = request.FILES['maskfile1']
        if 'datafile2' in request.FILES:
            dataset.datafile2 = request.FILES['datafile2']
        if 'errorfile2' in request.FILES:
            dataset.errorfile2 = request.FILES['errorfile2']
        if 'maskfile2' in request.FILES:
            dataset.maskfile2 = request.FILES['maskfile2']

    try:
        data_file = dataset.save()
        if filetype == 'datafile1':
            data = {'is_valid': True, 'name': basename(dataset.datafile1.name)}
        if filetype == 'errorfile1':
            data = {'is_valid': True, 'name': basename(dataset.errorfile1.name)}
        if filetype == 'maskfile1':
            data = {'is_valid': True, 'name': basename(dataset.maskfile1.name)}
        if filetype == 'datafile2':
            data = {'is_valid': True, 'name': basename(dataset.datafile2.name)}
        if filetype == 'errorfile2':
            data = {'is_valid': True, 'name': basename(dataset.errorfile2.name)}
        if filetype == 'maskfile2':
            data = {'is_valid': True, 'name': basename(dataset.maskfile2.name)}
    except:
        data = {'is_valid': False}

    return JsonResponse(data)


@login_required
def edit_job_psf(request, id):
    """
    Form to edit the PSF information. It also returns forms to be rendered in other tabs
    (models).

    :param request: current request (post or get)
    :param id: job id
    :return: content to be rendered
    """

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
    """
    Form to edit the LSF information. It also returns forms to be rendered in other tabs
    (models).

    :param request: current request (post or get)
    :param id: job id
    :return: content to be rendered
    """

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
    """
    Form to edit the galaxy model information. It also returns forms to be rendered in other tabs
    (models).

    :param request: current request (post or get)
    :param id: job id
    :return: content to be rendered
    """

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
    """
    Form to edit the fitter information. It also returns forms to be rendered in other tabs
    (models).

    :param request: current request (post or get)
    :param id: job id
    :return: content to be rendered
    """

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
    """
    Form to edit the params information. It also returns forms to be rendered in other tabs
    (models).

    :param request: current request (post or get)
    :param id: job id
    :return: content to be rendered
    """

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
    """
    Form to launch a job (changes the job status to submitted)
    It also returns forms to be rendered in other tabs (models).

    :param request: current request (post or get)
    :param id: job id
    :return: content to be rendered
    """

    active_tab = LAUNCH
    active_tab, forms, views = act_on_request_method_edit(request, active_tab, id)

    if active_tab != SUBMITTED:
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


"""

    JOB RESULTS

"""


@login_required
def download_asset(request, job_id, download, file_path):
    """
    Returns a file from the server for the specified job
    :param request: The django request object
    :param job_id: int: The job id
    :param download: int: Force download or not
    :param file_path: string: the path to the file to fetch
    :return: A HttpStreamingResponse object representing the file
    """
    # Get the job
    job = get_object_or_404(Job, id=job_id)

    # Check that this user has access to this job
    if job.user != request.user:
        # Nothing to see here
        raise Http404

    # Get the requested file from the server
    try:
        return job.fetch_remote_file(file_path, force_download=download == 1)
    except:
        raise Http404


# Should require that you have access to this job id too.
@login_required
def results(request, id):
    """
    Handles a result form
    :param request: current request (get)
    :param id: job id
    :return: returns views to render
    """

    # Get the job
    job = get_object_or_404(Job, id=id)

    # Check that this user has access to this job
    if job.user != request.user:
        # Nothing to see here
        raise Http404

    active_tab = LAUNCH
    # This could be cleaned to avoid getting forms and only gather the one view we need
    # (which also requires info from gmodel and fitter).
    active_tab, forms, views = act_on_request_method_edit(request, active_tab, id)

    # for drafts there are no clusters assigned, so job.custer is None for them
    is_online = job.cluster is not None and job.cluster.is_connected() is not None

    job = model_instance_to_iterable(Job.objects.get(id=id), model=START)

    if is_online and job.job_status == JobStatus.COMPLETED:
        # Check if any results exist for this job
        if not Result.objects.filter(job_id=id).exists():
            result_json = b''
            for part in job.fetch_remote_file('output/results.json').streaming_content:
                result_json += part

            result_json = json.loads(result_json)

            save_job_results(job.id, result_json)

            # Get the list of images generated
            result = job.fetch_remote_file_list(path="/", recursive=True)
            # Waste the message id
            result.pop_uint()
            # Iterate over each file
            num_entries = result.pop_uint()
            files = []
            for _ in range(num_entries):
                files.append(result.pop_string())
                # Waste the is_file bool
                result.pop_bool()
                # Waste the file size
                result.pop_ulong()

            # Get all image files
            images = [f for f in files if f.endswith('.png')]
            image_data = []
            for i in images:
                if 'velmap' in i: image_data.append({'filename': i, 'type': 'velmap'})
                if 'sigmap' in i: image_data.append({'filename': i, 'type': 'sigmap'})
                if 'flxmap' in i: image_data.append({'filename': i, 'type': 'flxmap'})
                if 'flxcube' in i: image_data.append({'filename': i, 'type': 'flxcube'})

            for i in image_data:
                save_job_image(job.id, int(i['filename'].split('_')[-2]), i['type'], i['filename'])

        job.result = model_instance_to_iterable(Result.objects.get(job_id=id), model=RESULT)

        job.result.modes = {}
        i = 0

        for mode in Mode.objects.filter(result__id=job.result.id):
            job.result.modes[i] = model_instance_to_iterable(mode, model=MODE)

            # Gather the parameters of this mode
            job.result.modes[i].params = {}
            j = 0
            for params in ModeParameter.objects.filter(mode__id=job.result.modes[i].id):
                job.result.modes[i].params[j] = model_instance_to_iterable(params, model=MODE_PARAMS)
                j += 1

            # Gather the image of this mode
            job.result.modes[i].mode_image = {}
            j = 0
            for mode_image in ModeImage.objects.filter(mode_id=job.result.modes[i].id):
                job.result.modes[i].mode_image[j] = model_instance_to_iterable(mode_image, model=RESULT_FILE)
                j += 1

            i += 1

    return render(
        request,
        "job/job_result.html",
        {
            'job_id': id,
            'job_view': job,
            'is_online': is_online,
            'result_filename': '/gbkfit_job_{}.tar.gz'.format(job.id),
            'params_view': views[TABS_INDEXES[PARAMS]],
        }
    )


@login_required
def job_overview(request, id):
    """
    Function to handle the overview view of a job
    :param request: current request (get)
    :param id: job id
    :return: renderable views
    """

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
    """
    Function to duplicate a job
    :param request: current request (post)
    :param id: id of the job to duplicate
    :return: redirects to the edit page of the newly duplicated job
    """

    job = Job.objects.get(id=id)
    # Check write permission
    if job.user_id == request.user.id:
        job.pk = None
        job.id = None
        # TODO: Need a mechanism to ensure name unique constraint.
        job.name = job.name + '_copy'
        job.submission_time = None
        job.job_status = JobStatus.DRAFT
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

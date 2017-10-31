from __future__ import unicode_literals

import json

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django import forms

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
    GalaxyModel, Fitter as Fitter_model, ParameterSet as Params
)

from gbkfit_web.views.job_info import model_instance_to_iterable



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

TABS_INDEXES = {START: 0,
                DMODEL: 1,
                DATASET: 2,
                PSF: 3,
                LSF: 4,
                GMODEL: 5,
                FITTER: 6,
                PARAMS: 7,
                LAUNCH: 8}

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
        dataset=dataset,
        psf=psf,
        lsf=lsf,
        gmodel=gmodel,
        fitter=fitter,
        params=params,
    )

    return json.dumps(task_json)

"""

    JOB CREATION/EDITING  SECTION

"""
def save_form(form, request, active_tab):
    if form.is_valid():
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

    # ACTIVE TAB
    if request.method == 'POST':
        if active_tab == START:
            instance = MODELS_EDIT[active_tab].objects.get(id=id)
            form = FORMS_EDIT[active_tab](request.POST,
                                          instance=instance,
                                          request=request,
                                          job_id=id)
        else:
            if active_tab == DATASET:
                if request.FILES['datafile1']:
                    form = FORMS_NEW[active_tab](request.POST, request.FILES, request=request, id=id)
                else:
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
                    form = FORMS_NEW[active_tab](request.POST, request=request, id=id)


        active_tab = save_form(form, request, active_tab)

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
        }
    )
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
        }
    )

@login_required
def launch(request, id):
    active_tab = LAUNCH
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
        }
    )
    # task_json = build_task_json(request)
    #
    # request.session['task'] = task_json
    #
    # return HttpResponse(task_json, content_type='application/json')
from __future__ import unicode_literals

# for testing only
from django.http import HttpResponse
import json

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django import forms
from django.views.generic.edit import FormView

from django.shortcuts import render
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


"""

    UTILITY SECTION

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
        DATASET,
        DMODEL,
        PSF,
        LSF,
        GMODEL,
        FITTER,
        PARAMS,
        LAUNCH]

TABS_INDEXES = {START: 0,
                DATASET: 1,
                DMODEL: 2,
                PSF: 3,
                LSF: 4,
                GMODEL: 5,
                FITTER: 6,
                PARAMS: 7,
                LAUNCH: 8}

FORMS_NEW = {START: JobInitialForm,
             DATASET: DataSetForm,
             DMODEL: DataModelForm,
             PSF: PSFForm,
             LSF: LSFForm,
             GMODEL: GalaxyModelForm,
             FITTER: FitterForm,
             PARAMS: ParamsForm}

FORMS_EDIT = {START: EditJobForm,
              DATASET: EditDataSetForm,
              DMODEL: EditDataModelForm,
              PSF: EditPSFForm,
              LSF: EditLSFForm,
              GMODEL: EditGalaxyModelForm,
              FITTER: EditFitterForm,
              PARAMS: EditParamsForm}

MODELS_EDIT = {START: Job,
              DATASET: DataSet,
              DMODEL: DataModel,
              PSF: PSF_model,
              LSF: LSF_model,
              GMODEL: GalaxyModel,
              FITTER: Fitter_model,
              PARAMS: Params}

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
    id = request.session['draft_job']['id']
    job = Job.objects.get(id=id)
    dataset = DataSet.objects.get(job_id=id)
    dmodel = DataModel.objects.get(job_id=id)
    psf = PSF_model.objects.get(job_id=id)
    lsf = LSF_model.objects.get(job_id=id)
    gmodel = GalaxyModel.objects.get(job_id=id)
    fitter = Fitter_model.objects.get(job_id=id)
    params = Params.objects.get(job_id=id)

    task_json = dict(
        job=job.as_json(),
        task=dict(
            mode='fit',
            datasets=dataset.as_array(),
            dmodel=dmodel.as_json(),
            psf=psf.as_json(),
            lsf=lsf.as_json(),
            gmodel=gmodel.as_json(),
            fitter=fitter.as_json(),
            params=params.as_array()
        )
    )

    return json.dumps(task_json)



"""

    JOB CREATION SECTION

"""

def act_on_request_method_create(request, active_tab):
    if request.method == 'POST':
        form = FORMS_NEW[active_tab](request.POST, request=request)
        if form.is_valid():
            form.save()
            active_tab = next_tab(active_tab)
    else:
        form = FORMS_NEW[active_tab](request=request)

    return form, active_tab

@login_required
def start(request):
    active_tab = START

    JobInitialForm.base_fields['job'] = set_job_menu(request)

    form, active_tab = act_on_request_method_create(request, active_tab)

    return render(
        request,
        "job/create.html",
        {
            'active_tab': active_tab,
            'start_form': form,
            'dataset_form': FORMS_NEW[DATASET](),
            'data_model_form': FORMS_NEW[DMODEL](),
            'psf_form': FORMS_NEW[PSF](),
            'lsf_form': FORMS_NEW[LSF](),
            'galaxy_model_form': FORMS_NEW[GMODEL](),
            'fitter_form': FORMS_NEW[FITTER](),
            'params_form': FORMS_NEW[PARAMS](),
        }
    )

@login_required
def dataset(request):
    active_tab = DATASET

    JobInitialForm.base_fields['job'] = set_job_menu(request)

    if request.method == 'POST' and request.FILES['datafile1']:
        form = FORMS_NEW[active_tab](request.POST, request.FILES, request=request)

        if form.is_valid():
            form.save()
            active_tab = next_tab(active_tab)
    else:
        form = FORMS_NEW[active_tab]()

    return render(
        request,
        "job/create.html",
        {
            'active_tab': active_tab,
            'dataset_form': form,
            'start_form': FORMS_NEW[START](request=request),
            'data_model_form': FORMS_NEW[DMODEL](),
            'psf_form': FORMS_NEW[PSF](),
            'lsf_form': FORMS_NEW[LSF](),
            'galaxy_model_form': FORMS_NEW[GMODEL](),
            'fitter_form': FORMS_NEW[FITTER](),
            'params_form': FORMS_NEW[PARAMS](),
        }
    )

@login_required
def data_model(request):
    active_tab = DMODEL

    JobInitialForm.base_fields['job'] = set_job_menu(request)

    form, active_tab = act_on_request_method_create(request, active_tab)

    return render(
        request,
        "job/create.html",
        {
            'active_tab': active_tab,
            'start_form': FORMS_NEW[START](request=request),
            'dataset_form': FORMS_NEW[DATASET](),
            'data_model_form': form,
            'psf_form': FORMS_NEW[PSF](),
            'lsf_form': FORMS_NEW[LSF](),
            'galaxy_model_form': FORMS_NEW[GMODEL](),
            'fitter_form': FORMS_NEW[FITTER](),
            'params_form': FORMS_NEW[PARAMS](),
        }
    )

@login_required
def psf(request):
    active_tab = PSF

    JobInitialForm.base_fields['job'] = set_job_menu(request)

    form, active_tab = act_on_request_method_create(request, active_tab)

    return render(
        request,
        "job/create.html",
        {
            'active_tab': active_tab,
            'start_form': FORMS_NEW[START](request=request),
            'dataset_form': FORMS_NEW[DATASET](),
            'data_model_form': FORMS_NEW[DMODEL](),
            'psf_form': form,
            'lsf_form': FORMS_NEW[LSF](),
            'galaxy_model_form': FORMS_NEW[GMODEL](),
            'fitter_form': FORMS_NEW[FITTER](),
            'params_form': FORMS_NEW[PARAMS](),
        }
    )

@login_required
def lsf(request):
    active_tab = LSF

    JobInitialForm.base_fields['job'] = set_job_menu(request)

    form, active_tab = act_on_request_method_create(request, active_tab)

    return render(
        request,
        "job/create.html",
        {
            'active_tab': active_tab,
            'start_form': FORMS_NEW[START](request=request),
            'dataset_form': FORMS_NEW[DATASET](),
            'data_model_form': FORMS_NEW[DMODEL](),
            'psf_form': FORMS_NEW[PSF](),
            'lsf_form': form,
            'galaxy_model_form': FORMS_NEW[GMODEL](),
            'fitter_form': FORMS_NEW[FITTER](),
            'params_form': FORMS_NEW[PARAMS](),
        }
    )

@login_required
def galaxy_model(request):
    active_tab = GMODEL

    JobInitialForm.base_fields['job'] = set_job_menu(request)

    form, active_tab = act_on_request_method_create(request, active_tab)

    return render(
        request,
        "job/create.html",
        {
            'active_tab': active_tab,
            'start_form': FORMS_NEW[START](request=request),
            'dataset_form': FORMS_NEW[DATASET](),
            'data_model_form': FORMS_NEW[DMODEL](),
            'psf_form': FORMS_NEW[PSF](),
            'lsf_form': FORMS_NEW[LSF](),
            'galaxy_model_form': form,
            'fitter_form': FORMS_NEW[FITTER](),
            'params_form': FORMS_NEW[PARAMS](),
        }
    )

@login_required
def fitter(request):
    active_tab = FITTER

    JobInitialForm.base_fields['job'] = set_job_menu(request)

    form, active_tab = act_on_request_method_create(request, active_tab)

    return render(
        request,
        "job/create.html",
        {
            'active_tab': active_tab,
            'start_form': FORMS_NEW[START](request=request),
            'dataset_form': FORMS_NEW[DATASET](),
            'data_model_form': FORMS_NEW[DMODEL](),
            'psf_form': FORMS_NEW[PSF](),
            'lsf_form': FORMS_NEW[LSF](),
            'galaxy_model_form': FORMS_NEW[GMODEL](),
            'fitter_form': form,
            'params_form': FORMS_NEW[PARAMS](),
        }
    )

@login_required
def params(request):
    active_tab = PARAMS

    JobInitialForm.base_fields['job'] = set_job_menu(request)

    form, active_tab = act_on_request_method_create(request, active_tab)

    return render(
        request,
        "job/create.html",
        {
            'active_tab': active_tab,
            'start_form': FORMS_NEW[START](request=request),
            'dataset_form': FORMS_NEW[DATASET](),
            'data_model_form': FORMS_NEW[DMODEL](),
            'psf_form': FORMS_NEW[PSF](),
            'lsf_form': FORMS_NEW[LSF](),
            'galaxy_model_form': FORMS_NEW[GMODEL](),
            'fitter_form': FORMS_NEW[FITTER](),
            'params_form': form,
        }
    )

@login_required
def launch(request):
    task_json = build_task_json(request)

    request.session['task'] = task_json

    return HttpResponse(task_json, content_type='application/json')






"""

    JOB EDITING SECTION

"""

def act_on_request_method_edit(request, active_tab, id):
    if request.method == 'POST':
        if active_tab == START:
            form = FORMS_EDIT[active_tab](request.POST, instance=MODELS_EDIT[active_tab].objects.get(id=id))
        else:
            form = FORMS_EDIT[active_tab](request.POST, instance=MODELS_EDIT[active_tab].objects.get(job_id=id))

        if form.is_valid():
            form.save()
            active_tab = next_tab(active_tab)
    else:
        if active_tab == START:
            form = FORMS_EDIT[active_tab](instance=MODELS_EDIT[active_tab].objects.get(id=id))
        else:
            form = FORMS_EDIT[active_tab](instance=MODELS_EDIT[active_tab].objects.get(job_id=id))

    return form, active_tab

@login_required
def edit_job_name(request, id):
    active_tab = START
    JobInitialForm.base_fields['job'] = set_job_menu(request, id)

    form, active_tab = act_on_request_method_edit(request, active_tab, id)

    return render(
        request,
        "job/edit.html",
        {
            'job_id': id,
            'active_tab': active_tab,
            'start_form': form,
            'dataset_form': FORMS_EDIT[DATASET](instance=DataSet.objects.get(job_id=id)),
            'data_model_form': FORMS_EDIT[DMODEL](instance=DataModel.objects.get(job_id=id)),
            'psf_form': FORMS_EDIT[PSF](instance=PSF_model.objects.get(job_id=id)),
            'lsf_form': FORMS_EDIT[LSF](instance=LSF_model.objects.get(job_id=id)),
            'galaxy_model_form': FORMS_EDIT[GMODEL](instance=GalaxyModel.objects.get(job_id=id)),
            'fitter_form': FORMS_EDIT[FITTER](instance=Fitter_model.objects.get(job_id=id)),
            'params_form': FORMS_EDIT[PARAMS](instance=Params.objects.get(job_id=id)),
        }
    )

@login_required
def edit_job_dataset(request, id):
    active_tab = DATASET
    JobInitialForm.base_fields['job'] = set_job_menu(request, id)

    form, active_tab = act_on_request_method_edit(request, active_tab, id)

    return render(
        request,
        "job/edit.html",
        {
            'job_id': id,
            'active_tab': active_tab,
            'start_form': FORMS_EDIT[START](instance=Job.objects.get(id=id)),
            'dataset_form': form,
            'data_model_form': FORMS_EDIT[DMODEL](instance=DataModel.objects.get(job_id=id)),
            'psf_form': FORMS_EDIT[PSF](instance=PSF_model.objects.get(job_id=id)),
            'lsf_form': FORMS_EDIT[LSF](instance=LSF_model.objects.get(job_id=id)),
            'galaxy_model_form': FORMS_EDIT[GMODEL](instance=GalaxyModel.objects.get(job_id=id)),
            'fitter_form': FORMS_EDIT[FITTER](instance=Fitter_model.objects.get(job_id=id)),
            'params_form': FORMS_EDIT[PARAMS](instance=Params.objects.get(job_id=id)),
        }
    )

@login_required
def edit_job_data_model(request, id):
    active_tab = DMODEL
    JobInitialForm.base_fields['job'] = set_job_menu(request, id)

    form, active_tab = act_on_request_method_edit(request, active_tab, id)

    return render(
        request,
        "job/edit.html",
        {
            'job_id': id,
            'active_tab': active_tab,
            'start_form': FORMS_EDIT[START](instance=Job.objects.get(id=id)),
            'dataset_form': FORMS_EDIT[DATASET](instance=DataSet.objects.get(job_id=id)),
            'data_model_form': form,
            'psf_form': FORMS_EDIT[PSF](instance=PSF_model.objects.get(job_id=id)),
            'lsf_form': FORMS_EDIT[LSF](instance=LSF_model.objects.get(job_id=id)),
            'galaxy_model_form': FORMS_EDIT[GMODEL](instance=GalaxyModel.objects.get(job_id=id)),
            'fitter_form': FORMS_EDIT[FITTER](instance=Fitter_model.objects.get(job_id=id)),
            'params_form': FORMS_EDIT[PARAMS](instance=Params.objects.get(job_id=id)),
        }
    )

@login_required
def edit_job_psf(request, id):
    active_tab = PSF
    JobInitialForm.base_fields['job'] = set_job_menu(request, id)

    form, active_tab = act_on_request_method_edit(request, active_tab, id)

    return render(
        request,
        "job/edit.html",
        {
            'job_id': id,
            'active_tab': active_tab,
            'start_form': FORMS_EDIT[START](instance=Job.objects.get(id=id)),
            'dataset_form': FORMS_EDIT[DATASET](instance=DataSet.objects.get(job_id=id)),
            'data_model_form': FORMS_EDIT[DMODEL](instance=DataModel.objects.get(job_id=id)),
            'psf_form': form,
            'lsf_form': FORMS_EDIT[LSF](instance=LSF_model.objects.get(job_id=id)),
            'galaxy_model_form': FORMS_EDIT[GMODEL](instance=GalaxyModel.objects.get(job_id=id)),
            'fitter_form': FORMS_EDIT[FITTER](instance=Fitter_model.objects.get(job_id=id)),
            'params_form': FORMS_EDIT[PARAMS](instance=Params.objects.get(job_id=id)),
        }
    )

@login_required
def edit_job_lsf(request, id):
    active_tab = LSF
    JobInitialForm.base_fields['job'] = set_job_menu(request, id)

    form, active_tab = act_on_request_method_edit(request, active_tab, id)

    return render(
        request,
        "job/edit.html",
        {
            'job_id': id,
            'active_tab': active_tab,
            'start_form': FORMS_EDIT[START](instance=Job.objects.get(id=id)),
            'dataset_form': FORMS_EDIT[DATASET](instance=DataSet.objects.get(job_id=id)),
            'data_model_form': FORMS_EDIT[DMODEL](instance=DataModel.objects.get(job_id=id)),
            'psf_form': FORMS_EDIT[PSF](instance=PSF_model.objects.get(job_id=id)),
            'lsf_form': form,
            'galaxy_model_form': FORMS_EDIT[GMODEL](instance=GalaxyModel.objects.get(job_id=id)),
            'fitter_form': FORMS_EDIT[FITTER](instance=Fitter_model.objects.get(job_id=id)),
            'params_form': FORMS_EDIT[PARAMS](instance=Params.objects.get(job_id=id)),
        }
    )

@login_required
def edit_job_galaxy_model(request, id):
    active_tab = GMODEL
    JobInitialForm.base_fields['job'] = set_job_menu(request, id)

    form, active_tab = act_on_request_method_edit(request, active_tab, id)

    return render(
        request,
        "job/edit.html",
        {
            'job_id': id,
            'active_tab': active_tab,
            'start_form': FORMS_EDIT[START](instance=Job.objects.get(id=id)),
            'dataset_form': FORMS_EDIT[DATASET](instance=DataSet.objects.get(job_id=id)),
            'data_model_form': FORMS_EDIT[DMODEL](instance=DataModel.objects.get(job_id=id)),
            'psf_form': FORMS_EDIT[PSF](instance=PSF_model.objects.get(job_id=id)),
            'lsf_form': FORMS_EDIT[LSF](instance=LSF_model.objects.get(job_id=id)),
            'galaxy_model_form': form,
            'fitter_form': FORMS_EDIT[FITTER](instance=Fitter_model.objects.get(job_id=id)),
            'params_form': FORMS_EDIT[PARAMS](instance=Params.objects.get(job_id=id)),
        }
    )

@login_required
def edit_job_fitter(request, id):
    active_tab = FITTER
    JobInitialForm.base_fields['job'] = set_job_menu(request, id)

    form, active_tab = act_on_request_method_edit(request, active_tab, id)

    return render(
        request,
        "job/edit.html",
        {
            'job_id': id,
            'active_tab': active_tab,
            'start_form': FORMS_EDIT[START](instance=Job.objects.get(id=id)),
            'dataset_form': FORMS_EDIT[DATASET](instance=DataSet.objects.get(job_id=id)),
            'data_model_form': FORMS_EDIT[DMODEL](instance=DataModel.objects.get(job_id=id)),
            'psf_form': FORMS_EDIT[PSF](instance=PSF_model.objects.get(job_id=id)),
            'lsf_form': FORMS_EDIT[LSF](instance=LSF_model.objects.get(job_id=id)),
            'galaxy_model_form': FORMS_EDIT[GMODEL](instance=GalaxyModel.objects.get(job_id=id)),
            'fitter_form': form,
            'params_form': FORMS_EDIT[PARAMS](instance=Params.objects.get(job_id=id)),
        }
    )

@login_required
def edit_job_params(request, id):
    active_tab = PARAMS
    JobInitialForm.base_fields['job'] = set_job_menu(request, id)

    form, active_tab = act_on_request_method_edit(request, active_tab, id)

    return render(
        request,
        "job/edit.html",
        {
            'job_id': id,
            'active_tab': active_tab,
            'start_form': FORMS_EDIT[START](instance=Job.objects.get(id=id)),
            'dataset_form': FORMS_EDIT[DATASET](instance=DataSet.objects.get(job_id=id)),
            'data_model_form': FORMS_EDIT[DMODEL](instance=DataModel.objects.get(job_id=id)),
            'psf_form': FORMS_EDIT[PSF](instance=PSF_model.objects.get(job_id=id)),
            'lsf_form': FORMS_EDIT[LSF](instance=LSF_model.objects.get(job_id=id)),
            'galaxy_model_form': FORMS_EDIT[GMODEL](instance=GalaxyModel.objects.get(job_id=id)),
            'fitter_form': FORMS_EDIT[FITTER](instance=Fitter_model.objects.get(job_id=id)),
            'params_form': form,
        }
    )
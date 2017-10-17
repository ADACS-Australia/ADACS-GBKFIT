from __future__ import unicode_literals

# for testing only
from django.http import HttpResponse
import json

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django import forms
from django.shortcuts import render
from gbkfit_web.forms.job.dataset import DataSetForm
from gbkfit_web.forms.job.job_initial import JobInitialForm
from gbkfit_web.forms.job.data_model import DataModelForm
from gbkfit_web.forms.job.psf import PSFForm
from gbkfit_web.forms.job.lsf import LSFForm
from gbkfit_web.forms.job.galaxy_model import GalaxyModelForm
from gbkfit_web.forms.job.fitter import FitterForm
from gbkfit_web.forms.job.params import ParamsForm
from gbkfit_web.models import (
    Job, DataSet, DataModel, PSF as PSF_model, LSF as LSF_model, GalaxyModel, Fitter as Fitter_model
)

START = 'start'
DATASET = 'data-set'
DMODEL = 'data-model'
PSF = 'psf'
LSF = 'lsf'
GMODEL = 'galaxy-model'
FITTER = 'fitter'
PARAMS = 'params'
LAUNCH = 'launch'

TABS = [START, DATASET, DMODEL, PSF, LSF, GMODEL, FITTER, LAUNCH]
TABS_INDEXES = {START: 0,
                DATASET: 1,
                DMODEL: 2,
                PSF: 3,
                LSF: 4,
                GMODEL: 5,
                FITTER: 6,
                PARAMS: 7,
                LAUNCH: 8}
FORMS = {START: JobInitialForm,
         DATASET: DataSetForm,
         DMODEL: DataModelForm,
         PSF: PSFForm,
         LSF: LSFForm,
         GMODEL: GalaxyModelForm,
         FITTER: FitterForm,
         PARAMS: ParamsForm
}

def next_tab(active_tab):
    return TABS[TABS_INDEXES[active_tab] + 1]

def set_job_menu(request):
    return forms.ModelChoiceField(
        label=_('Select Job'),
        queryset=Job.objects.filter(user=request.user, status=Job.DRAFT),
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
        )
    )

    return json.dumps(task_json)

@login_required
def start(request):
    active_tab = START

    JobInitialForm.base_fields['job'] = set_job_menu(request)

    if request.method == 'POST':
        form = FORMS[START](request.POST, request=request)
        if form.is_valid():
            new_job = form.save()
            active_tab = next_tab(active_tab)
    else:
        form = FORMS[START](request=request)

    return render(
        request,
        "job/create.html",
        {
            'active_tab': active_tab,
            'start_form': form,
            'dataset_form': FORMS[DATASET](),
            'data_model_form': FORMS[DMODEL](),
            'psf_form': FORMS[PSF](),
            'lsf_form': FORMS[LSF](),
            'galaxy_model_form': FORMS[GMODEL](),
            'fitter_form': FORMS[FITTER](),
            'params_form': FORMS[PARAMS](),
        }
    )

@login_required
def dataset(request):
    active_tab = DATASET

    JobInitialForm.base_fields['job'] = set_job_menu(request)

    if request.method == 'POST' and request.FILES['datafile1']:
        form = FORMS[DATASET](request.POST, request.FILES, request=request)

        if form.is_valid():
            form.save()
            active_tab = next_tab(active_tab)
    else:
        form = FORMS[DATASET]()

    return render(
        request,
        "job/create.html",
        {
            'active_tab': active_tab,
            'dataset_form': form,
            'start_form': FORMS[START](request=request),
            'data_model_form': FORMS[DMODEL](),
            'psf_form': FORMS[PSF](),
            'lsf_form': FORMS[LSF](),
            'galaxy_model_form': FORMS[GMODEL](),
            'fitter_form': FORMS[FITTER](),
            'params_form': FORMS[PARAMS](),
        }
    )

@login_required
def data_model(request):
    active_tab = DMODEL

    JobInitialForm.base_fields['job'] = set_job_menu(request)

    if request.method == 'POST':
        form = FORMS[DMODEL](request.POST, request=request)

        if form.is_valid():
            form.save()
            active_tab = next_tab(active_tab)
    else:
        form = FORMS[DMODEL]()

    return render(
        request,
        "job/create.html",
        {
            'active_tab': active_tab,
            'start_form': FORMS[START](request=request),
            'dataset_form': FORMS[DATASET](),
            'data_model_form': form,
            'psf_form': FORMS[PSF](),
            'lsf_form': FORMS[LSF](),
            'galaxy_model_form': FORMS[GMODEL](),
            'fitter_form': FORMS[FITTER](),
            'params_form': FORMS[PARAMS](),
        }
    )

@login_required
def psf(request):
    active_tab = PSF

    JobInitialForm.base_fields['job'] = set_job_menu(request)

    if request.method == 'POST':
        form = FORMS[PSF](request.POST, request=request)

        if form.is_valid():
            form.save()
            active_tab = next_tab(active_tab)
    else:
        form = FORMS[PSF]()

    return render(
        request,
        "job/create.html",
        {
            'active_tab': active_tab,
            'start_form': FORMS[START](request=request),
            'dataset_form': FORMS[DATASET](),
            'data_model_form': FORMS[DMODEL](),
            'psf_form': form,
            'lsf_form': FORMS[LSF](),
            'galaxy_model_form': FORMS[GMODEL](),
            'fitter_form': FORMS[FITTER](),
            'params_form': FORMS[PARAMS](),
        }
    )

@login_required
def lsf(request):
    active_tab = LSF

    JobInitialForm.base_fields['job'] = set_job_menu(request)

    if request.method == 'POST':
        form = FORMS[LSF](request.POST, request=request)

        if form.is_valid():
            form.save()
            active_tab = next_tab(active_tab)
    else:
        form = FORMS[LSF]()

    return render(
        request,
        "job/create.html",
        {
            'active_tab': active_tab,
            'start_form': FORMS[START](request=request),
            'dataset_form': FORMS[DATASET](),
            'data_model_form': FORMS[DMODEL](),
            'psf_form': FORMS[PSF](),
            'lsf_form': form,
            'galaxy_model_form': FORMS[GMODEL](),
            'fitter_form': FORMS[FITTER](),
            'params_form': FORMS[PARAMS](),
        }
    )

@login_required
def galaxy_model(request):
    active_tab = GMODEL

    JobInitialForm.base_fields['job'] = set_job_menu(request)

    if request.method == 'POST':
        form = FORMS[GMODEL](request.POST, request=request)

        if form.is_valid():
            form.save()
            active_tab = next_tab(active_tab)
    else:
        form = FORMS[GMODEL]()

    return render(
        request,
        "job/create.html",
        {
            'active_tab': active_tab,
            'start_form': FORMS[START](request=request),
            'dataset_form': FORMS[DATASET](),
            'data_model_form': FORMS[DMODEL](),
            'psf_form': FORMS[PSF](),
            'lsf_form': FORMS[LSF](),
            'galaxy_model_form': form,
            'fitter_form': FORMS[FITTER](),
            'params_form': FORMS[PARAMS](),
        }
    )

@login_required
def fitter(request):
    active_tab = FITTER

    JobInitialForm.base_fields['job'] = set_job_menu(request)

    if request.method == 'POST':
        form = FORMS[FITTER](request.POST, request=request)

        if form.is_valid():
            form.save()
            active_tab = next_tab(active_tab)
    else:
        form = FORMS[FITTER]()

    return render(
        request,
        "job/create.html",
        {
            'active_tab': active_tab,
            'start_form': FORMS[START](request=request),
            'dataset_form': FORMS[DATASET](),
            'data_model_form': FORMS[DMODEL](),
            'psf_form': FORMS[PSF](),
            'lsf_form': FORMS[LSF](),
            'galaxy_model_form': FORMS[GMODEL](),
            'fitter_form': form,
            'params_form': FORMS[PARAMS](),
        }
    )

@login_required
def params(request):
    active_tab = PARAMS

    JobInitialForm.base_fields['job'] = set_job_menu(request)

    if request.method == 'POST':
        form = FORMS[PARAMS](request.POST, request=request)

        if form.is_valid():
            form.save()
            active_tab = next_tab(active_tab)
    else:
        form = FORMS[PARAMS]()

    return render(
        request,
        "job/create.html",
        {
            'active_tab': active_tab,
            'start_form': FORMS[START](request=request),
            'dataset_form': FORMS[DATASET](),
            'data_model_form': FORMS[DMODEL](),
            'psf_form': FORMS[PSF](),
            'lsf_form': FORMS[LSF](),
            'galaxy_model_form': FORMS[GMODEL](),
            'fitter_form': FORMS[FITTER](),
            'params_form': form,
        }
    )

@login_required
def launch(request):
    task_json = build_task_json(request)

    request.session['task'] = task_json

    return HttpResponse(task_json, content_type='application/json')


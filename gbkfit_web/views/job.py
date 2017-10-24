from __future__ import unicode_literals

# for testing only
from django.http import HttpResponse
import json

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django import forms
from django.views.generic.edit import FormView

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
    try:
        id = request.session['draft_job']['id']
    except:
        id = request.user.id

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
    tab_checker = active_tab
    disable_other_tabs = True

    if active_tab != DATASET:
        if request.method == 'POST':
            form = FORMS_NEW[active_tab](request.POST, request=request)
            active_tab = save_form(form, request, active_tab)
            disable_other_tabs = False
        else:
            form = FORMS_NEW[active_tab](request=request)
            if active_tab != START:
                disable_other_tabs = False

    else:
        disable_other_tabs = False

        if request.method == 'POST' and request.FILES['datafile1']:
            form = FORMS_NEW[active_tab](request.POST, request.FILES, request=request)
            active_tab = save_form(form, request, active_tab)
        else:
            form = FORMS_NEW[active_tab]()

            # OTHER TABS
    if tab_checker != START:
        start_form = FORMS_NEW[START](request=request)
    else:
        start_form = form

    if tab_checker != DATASET:
        dataset_form = FORMS_NEW[DATASET]()
    else:
        dataset_form = form

    if tab_checker != DMODEL:
        data_model_form = FORMS_NEW[DMODEL]()
    else:
        data_model_form = form

    if tab_checker != PSF:
        psf_form = FORMS_NEW[PSF]()
    else:
        psf_form = form

    if tab_checker != LSF:
        lsf_form = FORMS_NEW[LSF]()
    else:
        lsf_form = form

    if tab_checker != GMODEL:
        galaxy_model_form = FORMS_NEW[GMODEL]()
    else:
        galaxy_model_form = form

    if tab_checker != FITTER:
        fitter_form = FORMS_NEW[FITTER]()
    else:
        fitter_form = form

    if tab_checker != PARAMS:
        params_form = FORMS_NEW[PARAMS]()
    else:
        params_form = form

    return active_tab, [start_form, dataset_form, data_model_form, psf_form,
                        lsf_form, galaxy_model_form, fitter_form, params_form], disable_other_tabs

def save_form(form, request, active_tab):
    if form.is_valid():
        form.save()
        if 'next' in request.POST:
            active_tab = next_tab(active_tab)
        if 'previous' in request.POST:
            active_tab = previous_tab(active_tab)
    return active_tab

@login_required
def start(request):
    active_tab = START
    active_tab, forms, disable_other_tabs = act_on_request_method_create(request, active_tab)

<<<<<<< HEAD
    print (disable_other_tabs)

=======
>>>>>>> c3a1b366564e4e11be69dea794948eef4e644e93
    if active_tab == START:
        return render(
            request,
            "job/create.html",
            {
                'active_tab': active_tab,
                'disable_other_tabs': disable_other_tabs,
                'start_form': forms[TABS_INDEXES[START]],
                'dataset_form': forms[TABS_INDEXES[DATASET]],
                'data_model_form': forms[TABS_INDEXES[DMODEL]],
                'psf_form': forms[TABS_INDEXES[PSF]],
                'lsf_form': forms[TABS_INDEXES[LSF]],
                'galaxy_model_form': forms[TABS_INDEXES[GMODEL]],
                'fitter_form': forms[TABS_INDEXES[FITTER]],
                'params_form': forms[TABS_INDEXES[PARAMS]],
            }
        )
    else:
        return redirect('job_dataset_edit', id=request.session['draft_job']['id'])

@login_required
def dataset(request):
    active_tab = DATASET
    active_tab, forms, disable_other_tabs = act_on_request_method_create(request, active_tab)

    return render(
        request,
        "job/create.html",
        {
            'active_tab': active_tab,
            'disable_other_tabs': disable_other_tabs,
            'start_form': forms[TABS_INDEXES[START]],
            'dataset_form': forms[TABS_INDEXES[DATASET]],
            'data_model_form': forms[TABS_INDEXES[DMODEL]],
            'psf_form': forms[TABS_INDEXES[PSF]],
            'lsf_form': forms[TABS_INDEXES[LSF]],
            'galaxy_model_form': forms[TABS_INDEXES[GMODEL]],
            'fitter_form': forms[TABS_INDEXES[FITTER]],
            'params_form': forms[TABS_INDEXES[PARAMS]],
        }
    )

@login_required
def data_model(request):
    active_tab = DMODEL
    active_tab, forms, disable_other_tabs = act_on_request_method_create(request, active_tab)

    return render(
        request,
        "job/create.html",
        {
            'active_tab': active_tab,
            'disable_other_tabs': disable_other_tabs,
            'start_form': forms[TABS_INDEXES[START]],
            'dataset_form': forms[TABS_INDEXES[DATASET]],
            'data_model_form': forms[TABS_INDEXES[DMODEL]],
            'psf_form': forms[TABS_INDEXES[PSF]],
            'lsf_form': forms[TABS_INDEXES[LSF]],
            'galaxy_model_form': forms[TABS_INDEXES[GMODEL]],
            'fitter_form': forms[TABS_INDEXES[FITTER]],
            'params_form': forms[TABS_INDEXES[PARAMS]],
        }
    )

@login_required
def psf(request):
    active_tab = PSF
    active_tab, forms, disable_other_tabs = act_on_request_method_create(request, active_tab)

    return render(
        request,
        "job/create.html",
        {
            'active_tab': active_tab,
            'disable_other_tabs': disable_other_tabs,
            'start_form': forms[TABS_INDEXES[START]],
            'dataset_form': forms[TABS_INDEXES[DATASET]],
            'data_model_form': forms[TABS_INDEXES[DMODEL]],
            'psf_form': forms[TABS_INDEXES[PSF]],
            'lsf_form': forms[TABS_INDEXES[LSF]],
            'galaxy_model_form': forms[TABS_INDEXES[GMODEL]],
            'fitter_form': forms[TABS_INDEXES[FITTER]],
            'params_form': forms[TABS_INDEXES[PARAMS]],
        }
    )

@login_required
def lsf(request):
    active_tab = LSF
    active_tab, forms, disable_other_tabs = act_on_request_method_create(request, active_tab)

    return render(
        request,
        "job/create.html",
        {
            'active_tab': active_tab,
            'disable_other_tabs': disable_other_tabs,
            'start_form': forms[TABS_INDEXES[START]],
            'dataset_form': forms[TABS_INDEXES[DATASET]],
            'data_model_form': forms[TABS_INDEXES[DMODEL]],
            'psf_form': forms[TABS_INDEXES[PSF]],
            'lsf_form': forms[TABS_INDEXES[LSF]],
            'galaxy_model_form': forms[TABS_INDEXES[GMODEL]],
            'fitter_form': forms[TABS_INDEXES[FITTER]],
            'params_form': forms[TABS_INDEXES[PARAMS]],
        }
    )

@login_required
def galaxy_model(request):
    active_tab = GMODEL
    active_tab, forms, disable_other_tabs = act_on_request_method_create(request, active_tab)

    return render(
        request,
        "job/create.html",
        {
            'active_tab': active_tab,
            'disable_other_tabs': disable_other_tabs,
            'start_form': forms[TABS_INDEXES[START]],
            'dataset_form': forms[TABS_INDEXES[DATASET]],
            'data_model_form': forms[TABS_INDEXES[DMODEL]],
            'psf_form': forms[TABS_INDEXES[PSF]],
            'lsf_form': forms[TABS_INDEXES[LSF]],
            'galaxy_model_form': forms[TABS_INDEXES[GMODEL]],
            'fitter_form': forms[TABS_INDEXES[FITTER]],
            'params_form': forms[TABS_INDEXES[PARAMS]],
        }
    )

@login_required
def fitter(request):
    active_tab = FITTER
    active_tab, forms, disable_other_tabs = act_on_request_method_create(request, active_tab)

    return render(
        request,
        "job/create.html",
        {
            'active_tab': active_tab,
            'disable_other_tabs': disable_other_tabs,
            'start_form': forms[TABS_INDEXES[START]],
            'dataset_form': forms[TABS_INDEXES[DATASET]],
            'data_model_form': forms[TABS_INDEXES[DMODEL]],
            'psf_form': forms[TABS_INDEXES[PSF]],
            'lsf_form': forms[TABS_INDEXES[LSF]],
            'galaxy_model_form': forms[TABS_INDEXES[GMODEL]],
            'fitter_form': forms[TABS_INDEXES[FITTER]],
            'params_form': forms[TABS_INDEXES[PARAMS]],
        }
    )

@login_required
def params(request):
    active_tab = PARAMS
    active_tab, forms, disable_other_tabs = act_on_request_method_create(request, active_tab)

    return render(
        request,
        "job/create.html",
        {
            'active_tab': active_tab,
            'disable_other_tabs': disable_other_tabs,
            'start_form': forms[TABS_INDEXES[START]],
            'dataset_form': forms[TABS_INDEXES[DATASET]],
            'data_model_form': forms[TABS_INDEXES[DMODEL]],
            'psf_form': forms[TABS_INDEXES[PSF]],
            'lsf_form': forms[TABS_INDEXES[LSF]],
            'galaxy_model_form': forms[TABS_INDEXES[GMODEL]],
            'fitter_form': forms[TABS_INDEXES[FITTER]],
            'params_form': forms[TABS_INDEXES[PARAMS]],
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
    # JobInitialForm.base_fields['job'] = set_job_menu(request, id)

    tab_checker = active_tab

    # ACTIVE TAB
    if request.method == 'POST':
        if active_tab == START:
            form = FORMS_EDIT[active_tab](request.POST, instance=MODELS_EDIT[active_tab].objects.get(id=id))
        else:
            try:
                # Update
                form = FORMS_EDIT[active_tab](request.POST, instance=MODELS_EDIT[active_tab].objects.get(job_id=id))
            except:
                if active_tab != DATASET:
                    form = FORMS_NEW[active_tab](request.POST, request=request)
                else:
                    if request.FILES['datafile1']:
                        form = FORMS_NEW[active_tab](request.POST, request.FILES, request=request)
                    else:
                        form = FORMS_NEW[active_tab]()

        active_tab = save_form(form, request, active_tab)

    else:
        if active_tab == START:
            form = FORMS_EDIT[active_tab](instance=MODELS_EDIT[active_tab].objects.get(id=id))
        else:
            try:
                form = FORMS_EDIT[active_tab](instance=MODELS_EDIT[active_tab].objects.get(job_id=id))
            except:
                if active_tab != DATASET:
                    form = FORMS_NEW[active_tab](request=request)
                else:
                    form = FORMS_NEW[active_tab]()

    # OTHER TABS
    if tab_checker != START:
        try:
            start_form = FORMS_EDIT[START](instance=Job.objects.get(id=id))
        except:
            # If the job is not found, let's go where we can create one!
            return redirect('job_start')
    else:
        start_form = form

    if tab_checker != DATASET:
        try:
            dataset_form = FORMS_EDIT[DATASET](instance=DataSet.objects.get(job_id=id))
        except:
            dataset_form = FORMS_EDIT[DATASET]()
    else:
        dataset_form = form

    if tab_checker != DMODEL:
        try:
            data_model_form = FORMS_EDIT[DMODEL](instance=DataModel.objects.get(job_id=id))
        except:
            data_model_form = FORMS_EDIT[DMODEL]()
    else:
        data_model_form = form

    if tab_checker != PSF:
        try:
            psf_form = FORMS_EDIT[PSF](instance=PSF_model.objects.get(job_id=id))
        except:
            psf_form = FORMS_EDIT[PSF]()
    else:
        psf_form = form

    if tab_checker != LSF:
        try:
            lsf_form = FORMS_EDIT[LSF](instance=LSF_model.objects.get(job_id=id))
        except:
            lsf_form = FORMS_EDIT[LSF]()
    else:
        lsf_form = form

    if tab_checker != GMODEL:
        try:
            galaxy_model_form = FORMS_EDIT[GMODEL](instance=GalaxyModel.objects.get(job_id=id))
        except:
            galaxy_model_form = FORMS_EDIT[GMODEL]()
    else:
        galaxy_model_form = form

    if tab_checker != FITTER:
        try:
            fitter_form = FORMS_EDIT[FITTER](instance=Fitter_model.objects.get(job_id=id))
        except:
            fitter_form = FORMS_EDIT[FITTER]()
    else:
        fitter_form = form

    if tab_checker != PARAMS:
        try:
            params_form = FORMS_EDIT[PARAMS](instance=Params.objects.get(job_id=id))
        except:
            params_form = FORMS_EDIT[PARAMS]()
    else:
        params_form = form

    return active_tab, [start_form, dataset_form, data_model_form, psf_form,
                        lsf_form, galaxy_model_form, fitter_form, params_form]

@login_required
def edit_job_name(request, id):
    active_tab = START
    active_tab, forms = act_on_request_method_edit(request, active_tab, id)

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
        }
    )

@login_required
def edit_job_dataset(request, id):
    active_tab = DATASET
    active_tab, forms = act_on_request_method_edit(request, active_tab, id)

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
        }
    )

@login_required
def edit_job_data_model(request, id):
    active_tab = DMODEL
    active_tab, forms = act_on_request_method_edit(request, active_tab, id)

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
        }
    )

@login_required
def edit_job_psf(request, id):
    active_tab = PSF
    active_tab, forms = act_on_request_method_edit(request, active_tab, id)

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
        }
    )

@login_required
def edit_job_lsf(request, id):
    active_tab = LSF
    active_tab, forms = act_on_request_method_edit(request, active_tab, id)

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
        }
    )

@login_required
def edit_job_galaxy_model(request, id):
    active_tab = GMODEL
    active_tab, forms = act_on_request_method_edit(request, active_tab, id)

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
        }
    )

@login_required
def edit_job_fitter(request, id):
    active_tab = FITTER
    active_tab, forms = act_on_request_method_edit(request, active_tab, id)

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
        }
    )

@login_required
def edit_job_params(request, id):
    active_tab = PARAMS
    active_tab, forms = act_on_request_method_edit(request, active_tab, id)

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
        }
    )

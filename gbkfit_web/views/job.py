from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.decorators import login_required
from django import forms
from django.shortcuts import render
from gbkfit_web.forms.job.dataset import DataSetForm
from gbkfit_web.forms.job.job_initial import JobInitialForm
from gbkfit_web.models import Job


@login_required
def start(request):
    data_set_form = DataSetForm()

    active_tab = 'start'

    JobInitialForm.base_fields['job'] = forms.ModelChoiceField(
        label=_('Select Job'),
        queryset=Job.objects.filter(user=request.user, status=Job.DRAFT),
        empty_label=_('New'),
        widget=forms.Select(
            attrs={'class': 'form-control'},
        ),
        required=False,
    )

    if request.method == 'POST':
        form = JobInitialForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            active_tab = 'data-set'
    else:
        form = JobInitialForm(request=request)

    return render(
        request,
        "job/create.html",
        {
            'active_tab': active_tab,
            'start_form': form,
            'dataset_form': data_set_form,
        }
    )

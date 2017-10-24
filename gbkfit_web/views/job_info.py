from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
import json
from gbkfit_web.models import Job
from django.utils import timezone

class JobDetailView(DetailView):
    model = Job

    def get_context_data(self, **kwargs):
        context = super(JobDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class JobListView(ListView):

    model = Job

    def get_context_data(self, **kwargs):
        context = super(JobListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

def delete_job(request, id):
    Job.objects.get(pk=id).delete()
    # return response(request)

    if request.method == 'POST' and request.is_ajax():
        return HttpResponse(json.dumps({'message': 'Job {} deleted'.format(id)}), content_type="application/json")


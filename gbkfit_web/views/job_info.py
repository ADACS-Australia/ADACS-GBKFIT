from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
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
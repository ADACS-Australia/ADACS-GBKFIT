from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from gbkfit_web.views import account, index, job, verify, job_info
from rest_framework import routers, serializers, viewsets


urlpatterns = [
    url(r'^$', index.index, name='index'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^jobs/(?P<pk>\d+)/$', login_required(job_info.JobDetailView.as_view(template_name='job/job_detail.html')), name='job_detail'),
    url(r'^jobs/$', login_required(job_info.JobListView.as_view(template_name='job/job_list.html')), name='job_list'),
    url(r'^jobs/(?P<id>\d+)/delete', login_required(job_info.delete_job), name='job_delete'),

    url(r'^new_job/$', job.start, name='job_start'),
    url(r'^new_job/(?P<id>\d+)/$', job.edit_job_name, name='job_name_edit'),
    url(r'^new_job/(?P<id>\d+)/dataset$', job.edit_job_dataset, name='job_dataset_edit'),
    url(r'^new_job/(?P<id>\d+)/data_model$', job.edit_job_data_model, name='job_data_model_edit'),
    url(r'^new_job/(?P<id>\d+)/psf$', job.edit_job_psf, name='job_psf_edit'),
    url(r'^new_job/(?P<id>\d+)/lsf$', job.edit_job_lsf, name='job_lsf_edit'),
    url(r'^new_job/(?P<id>\d+)/galaxy_model$', job.edit_job_galaxy_model, name='job_galaxy_model_edit'),
    url(r'^new_job/(?P<id>\d+)/fitter$', job.edit_job_fitter, name='job_fitter_edit'),
    url(r'^new_job/(?P<id>\d+)/params$', job.edit_job_params, name='job_params_edit'),
    url(r'^new_job/(?P<id>\d+)/launch$', job.launch, name='job_launch'),

    url(r'^job/(?P<id>\d+)/results', job.results, name='job_results'),
    url('^job/(?P<id>\d+)/ajax/download_results', job.download_results_tar, name='download_results'),
    url(r'^new_job/(?P<id>\d+)/ajax_dataset$', job.ajax_edit_job_dataset, name='basic_upload'),

    url(r'^job/(?P<id>\d+)/overview', job.job_overview, name='job_overview'),
    url(r'^job/(?P<id>\d+)/duplicate', job.job_duplicate, name='job_duplicate'),

    url(r'^register/$', account.registration, name='register'),
    url(r'^verify/$', verify.verify, name='verify'),

    url(r'^accounts/login/$',
            auth_views.LoginView.as_view(redirect_authenticated_user=True,
                                         template_name='accounts/login.html'), name='login'),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^accounts/profile/$', account.profile, name='profile'),
    url(r'^accounts/password/$', account.change_password, name='change_password'),

    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        account.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
]

###############
# REST API
###############

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
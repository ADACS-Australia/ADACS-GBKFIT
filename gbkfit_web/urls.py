from django.conf.urls import url
from django.contrib.auth import views as auth_views

from gbkfit_web.views import account, index, job, verify

urlpatterns = [
    url(r'^register/$', account.registration, name='register'),
    url(r'^new_job/$', job.start, name='job_start'),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^accounts/profile/$', account.profile, name='profile'),
    url(r'^verify/$', verify.verify, name='verify'),
    url(r'^$', index.index, name='index'),
]

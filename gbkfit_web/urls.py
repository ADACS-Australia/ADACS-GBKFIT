from django.conf.urls import url
from django.contrib.auth import views as auth_views

from gbkfit_web.views import account, index, job, verify

urlpatterns = [
    url(r'^$', index.index, name='index'),

    url(r'^register/$', account.registration, name='register'),

    url(r'^accounts/login/$',
        auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='accounts/login.html'),
        name='login'),

    url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),

    url(r'^accounts/profile/$', account.profile, name='profile'),

    url(r'^verify/$', verify.verify, name='verify'),

    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),

    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),

    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

    url(r'^new_job/$', job.start, name='job_start'),

]

from django.conf.urls import url

from gbkfit_web.workflow.views import WorkFlowView

urlpatterns = [
    url(r'^workflow/', WorkFlowView.as_view(), name='workflow'),
]

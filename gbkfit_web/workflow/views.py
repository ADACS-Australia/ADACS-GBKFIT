import json
from _sha512 import sha512
from hmac import compare_digest

from django.conf import settings
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.generics import GenericAPIView

from gbkfit_web.models import Job


class WorkflowTokenPermission(permissions.BasePermission):
    """
    SHA512 Hashes the workflow key and checks that the token key header of the request matches the key in settings
    """

    def has_permission(self, request, view):
        # Check that the request has a token header
        if 'HTTP_TOKEN' not in request.META:
            return False

        # Calculate the local hash
        hash = sha512(settings.WORKFLOW_SECRET.encode("utf-8")).hexdigest()

        # Compare the digests
        return compare_digest(request.META['HTTP_TOKEN'], hash)


class WorkFlowView(GenericAPIView):
    permission_classes = (WorkflowTokenPermission,)

    def get(self, request):
        print(request.GET)
        # Get all jobs with the requested status
        jobs = Job.objects.filter(status=request.GET['status'])
        print(jobs)

        # Now serialize the jobs

        data = {
            'good': 'one'
        }

        return HttpResponse(json.dumps(data))

    def post(self, request):
        print("Workflow Get")
        data = {
            'good': 'one'
        }

        return HttpResponse(json.dumps(data))

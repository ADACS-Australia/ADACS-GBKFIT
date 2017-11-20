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
        _hash = sha512(settings.WORKFLOW_SECRET.encode("utf-8")).hexdigest()

        # Compare the digests
        return compare_digest(request.META['HTTP_TOKEN'], _hash)


class WorkFlowView(GenericAPIView):
    permission_classes = (WorkflowTokenPermission,)

    def get(self, request):
        # Get all jobs with the requested status
        jobs = Job.objects.filter(status=request.GET['status'])

        # Now serialize the jobs
        data = [
            {
                'userid': job.user.id,
                'jobid': job.id,
            }
            for job in jobs
        ]

        return HttpResponse(json.dumps(data), content_type='application/json')

    def post(self, request):
        data = json.loads(request.data)
        print(data)
        data = {
            'good': 'one'
        }

        return HttpResponse(json.dumps(data))

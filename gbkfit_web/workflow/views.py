import glob
import json
from _sha512 import sha512
from hmac import compare_digest

import os
from django.conf import settings
from django.conf.global_settings import MEDIA_ROOT
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.generics import GenericAPIView

from gbkfit_web.models import Job, user_job_results_file_directory_path_not_field
from gbkfit_web.serializers import save_job_results, save_job_tar, save_job_image


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


def job_completed(job):
    """
    Called when a job is completed to handle creating the results instances in the database
    :param job: The job instance being marked completed
    :return:
    """

    # Save the job results
    save_job_results(job.id, os.path.join(user_job_results_file_directory_path_not_field(job), 'results.json'))

    # Next save the job tar file
    save_job_tar(job.id, os.path.join(user_job_results_file_directory_path_not_field(job), 'results.tar.gz')[len(MEDIA_ROOT):])

    # Next get all mode image files from the results directory
    for file in glob.glob(os.path.join(user_job_results_file_directory_path_not_field(job), 'mode_*.png')):
        save_job_image(job.id, int(file.split('_')[-1].split('.')[0]), file[len(MEDIA_ROOT):])


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
        # Create a status map to map workflow status to UI status
        status_map = {
            "QUEUED": Job.QUEUED,
            "IN_PROGRESS": Job.IN_PROGRESS,
            "COMPLETED": Job.COMPLETED,
            "ERROR": Job.ERROR
        }

        # Get the job with the requested id
        job = Job.objects.get(id=request.data['jobid'])

        # Set the job status
        job.status = status_map[request.data['status']]

        # Save the job
        job.save()

        # Check if the job is being marked complete
        if request.data['status'] == "COMPLETED":
            # Process the completed job and add the results to the database
            job_completed(job)

        # Create a response
        data = {
            'detail': 'Job {} updated to status {} successfully...'.format(job.id, job.status)
        }

        return HttpResponse(json.dumps(data), content_type='application/json')

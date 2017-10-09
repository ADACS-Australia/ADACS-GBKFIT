# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

import django.contrib.auth.models as auth_models

from django.db import models
from django_countries.fields import CountryField


class User(auth_models.AbstractUser):
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    NOT_DISCLAUSED = ''
    MR = 'Mr'
    MS = 'Ms'
    # MISS = 'Miss'
    MRS = 'Mrs'
    DR = 'Dr'
    PROF = 'Prof'
    A_PROF = 'A/Prof'

    TITLE_CHOICES = [
        (NOT_DISCLAUSED, NOT_DISCLAUSED),
        (MR, MR),
        (MS, MS),
        # (MISS, MS),
        (MRS, MRS),
        (DR, DR),
        (PROF, PROF),
        (A_PROF, A_PROF),
    ]

    MALE = 'Male'
    FEMALE = 'Female'
    PREFER_NOT_TO_SAY = 'Prefer not to say'
    GENDER_CHOICES = [
        (NOT_DISCLAUSED, NOT_DISCLAUSED),
        (FEMALE, FEMALE),
        (MALE, MALE),
    ]

    title = models.CharField(max_length=10, choices=TITLE_CHOICES, default=NOT_DISCLAUSED, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default=NOT_DISCLAUSED, blank=True)
    is_student = models.BooleanField(default=False)
    institution = models.CharField(max_length=100)
    country = CountryField(blank_label='Select Country', null=False, blank=False)
    scientific_interests = models.TextField(verbose_name='Scientific Interests', blank=True, null=True)

    UNVERIFIED = 'Unverified'
    VERIFIED = 'Verified'
    CONFIRMED = 'Confirmed'
    DELETED = 'Deleted'
    STATUS_CHOICES = [
        (UNVERIFIED, 'Unverified'),
        (VERIFIED, 'Verified'),
        (CONFIRMED, 'Confirmed'),
        (DELETED, 'Deleted'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=False, default=UNVERIFIED)

    def __unicode__(self):
        return u'%s %s %s (%s)' % (self.title, self.first_name, self.last_name, self.username)

    def as_json(self):
        return dict(
            id=self.id,
            value=dict(
                username=self.username,
                title=self.title,
                first_name=self.first_name,
                last_name=self.last_name,
            ),
        )


class Job(models.Model):
    user = models.ForeignKey(User, related_name='user_job')
    name = models.CharField(max_length=255, blank=False, null=False)

    DRAFT = 'Draft'
    SUBMITTED = 'Submitted'
    QUEUED = 'Queued'
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'
    ERROR = 'Error'
    SAVED = 'Saved'
    WALL_TIME_EXCEEDED = 'Wall Time Exceeded'
    DELETED = 'Deleted'
    STATUS_CHOICES = [
        (DRAFT, DRAFT),
        (SUBMITTED, SUBMITTED),
        (QUEUED, QUEUED),
        (IN_PROGRESS, IN_PROGRESS),
        (COMPLETED, COMPLETED),
        (ERROR, ERROR),
        (SAVED, SAVED),
        (WALL_TIME_EXCEEDED, WALL_TIME_EXCEEDED),
        (DELETED, DELETED),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=False, default=DRAFT)
    creation_time = models.DateTimeField(auto_now_add=True)
    submission_time = models.DateTimeField(null=True)

    class Meta:
        unique_together = (
            ('user', 'name'),
        )

    def __unicode__(self):
        return '{}'.format(self.name)

    def as_json(self):
        return dict(
            id=self.id,
            value=dict(
                name=self.name,
                # user=self.user,
                status=self.status,
                creation_time=self.creation_time.strftime('%d %b %Y %I:%m %p'),
            ),
        )


class DataSet(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_data_set')
    CUBE = 'Cube'
    IMAGE = 'Image'
    TYPE_CHOICES = [
        (CUBE, 'Cube'),
        (IMAGE, 'Image'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, blank=False, default=CUBE)
    data = models.FileField()
    error = models.FileField()
    mask = models.FileField()
    creation_time = models.DateTimeField(auto_now_add=True)

class DataModel(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_data_model')
    name = models.CharField(max_length=255, blank=False, null=False)

    SCUBE_OMP = 'scube_omp'
    SCUBE_CUDA = 'scube_cuda'
    MMNT_OMP = 'mmnt_omp'
    MMNT_CUDA = 'mmnt_cuda'

    TYPE_CHOICES = [
        (SCUBE_OMP, SCUBE_OMP),
        (SCUBE_CUDA, SCUBE_CUDA),
        (MMNT_OMP, MMNT_OMP),
        (MMNT_CUDA, MMNT_CUDA)
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, blank=False, default=SCUBE_OMP)

    #size (if cube: 3dims, if mmnt: 2dims?)
    size_x = models.PositiveIntegerField(blank=False, default=1)
    size_y = models.PositiveIntegerField(blank=False, default=1)
    # Need to figure out how to require the z field when required.
    size_z = models.PositiveIntegerField(blank=True)

    step_x = models.PositiveIntegerField(blank=False, default=1)
    step_y = models.PositiveIntegerField(blank=False, default=1)
    # Need to figure out how to require the z field when required.
    step_z = models.PositiveIntegerField(blank=True)

    creation_time = models.DateTimeField(auto_now_add=True)

class PSF(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_psf')
    name = models.CharField(max_length=255, blank=False, null=False)

    GAUSS = 'gauss'
    MOFFAT = 'moffat'
    LORENTZ = 'lorentz'

    TYPE_CHOICES = [
        (GAUSS, GAUSS),
        (MOFFAT, MOFFAT),
        (LORENTZ, LORENTZ),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, blank=False, default=GAUSS)

    fwhm_x = models.FloatField(blank=False, default=1.)
    fwhm_y = models.FloatField(blank=False, default=1.)
    pa = models.IntegerField(blank=False, default=1)
    # If Moffat, need to figure out how to require the following field.
    beta = models.FloatField(blank=False, default=1.)

    creation_time = models.DateTimeField(auto_now_add=True)

class LSF(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_lsf')
    name = models.CharField(max_length=255, blank=False, null=False)

    GAUSS = 'gauss'
    MOFFAT = 'moffat'
    LORENTZ = 'lorentz'

    TYPE_CHOICES = [
        (GAUSS, GAUSS),
        (MOFFAT, MOFFAT),
        (LORENTZ, LORENTZ),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, blank=False, default=GAUSS)

    fwhm = models.FloatField(blank=False, default=1.)
    # If Moffat, need to figure out how to require the following field.
    beta = models.FloatField(blank=False, default=1.)

    creation_time = models.DateTimeField(auto_now_add=True)

class GalaxyModel(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_gmodel')
    name = models.CharField(max_length=255, blank=False, null=False)

    THINDISK_OMP = 'thindisk_omp'
    THINDISK_CUDA = 'thindisk_cuda'

    TYPE_CHOICES = [
        (THINDISK_OMP, THINDISK_OMP),
        (THINDISK_CUDA, THINDISK_CUDA),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, blank=False, default=THINDISK_OMP)

    EXPONENTIAL = 'exponential'
    FLAT= 'flat'
    BOISSIER = 'boissier',
    ARCTAN = 'arctan'
    EPINAT = 'epinat'
    RINGS = 'rings'

    FPROFILE_TYPE_CHOICES = [
        (EXPONENTIAL, EXPONENTIAL),
        (FLAT, FLAT),
        (BOISSIER, BOISSIER),
        (ARCTAN, ARCTAN),
        (EPINAT, EPINAT),
        (RINGS, RINGS),
    ]
    fprofile_type = models.CharField(max_length=10, choices=FPROFILE_TYPE_CHOICES, blank=False, default=EXPONENTIAL)

    VPROFILE_TYPE_CHOICES = [
        (EXPONENTIAL, EXPONENTIAL),
        (FLAT, FLAT),
        (BOISSIER, BOISSIER),
        (ARCTAN, ARCTAN),
        (EPINAT, EPINAT),
        (RINGS, RINGS),
    ]
    vprofile_type = models.CharField(max_length=10, choices=VPROFILE_TYPE_CHOICES, blank=False, default=EXPONENTIAL)

    # Need to figure out how to require these fields when required.
    nrings = models.PositiveIntegerField(blank=True, default=1)
    rsize = models.PositiveIntegerField(blank=True, default=1)

    creation_time = models.DateTimeField(auto_now_add=True)

# class ParameterSet(models.Model):
#     job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_parameter_set')
#     pass

class Fitter(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_fitter')
    name = models.CharField(max_length=255, blank=False, null=False)

    MPFIT = 'mpfit'
    MULTINEST = 'multinest'

    TYPE_CHOICES = [
        (MPFIT, MPFIT),
        (MULTINEST, MULTINEST),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, blank=False, default=MPFIT)

    # MPFIT properties
    ftol = models.PositiveIntegerField(blank=True, default=1)
    xtol = models.PositiveIntegerField(blank=True, default=1)
    gtol = models.PositiveIntegerField(blank=True, default=1)
    epsfcn = models.PositiveIntegerField(blank=True, default=1)
    stepfactor = models.PositiveIntegerField(blank=True, default=1)
    covtol = models.PositiveIntegerField(blank=True, default=1)
    maxiter = models.PositiveIntegerField(blank=True, default=1)
    maxfev = models.PositiveIntegerField(blank=True, default=1)
    nprint = models.PositiveIntegerField(blank=True, default=1)
    douserscale = models.PositiveIntegerField(blank=True, default=1)
    nofinitecheck = models.PositiveIntegerField(blank=True, default=1)

    # Multinest properties
    efr = models.PositiveIntegerField(blank=True, default=1)
    tol = models.PositiveIntegerField(blank=True, default=1)
    ztol = models.PositiveIntegerField(blank=True, default=1)
    logzero = models.PositiveIntegerField(blank=True, default=1)
    _is = models.PositiveIntegerField(blank=True, default=1)
    mmodal = models.PositiveIntegerField(blank=True, default=1)
    ceff = models.PositiveIntegerField(blank=True, default=1)
    nlive = models.PositiveIntegerField(blank=True, default=1)
    maxiter = models.PositiveIntegerField(blank=True, default=1)
    seed = models.PositiveIntegerField(blank=True, default=1)
    outfile = models.CharField(max_length=255, blank=False, null=False)

    creation_time = models.DateTimeField(auto_now_add=True)

class Verification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    information = models.CharField(max_length=1024)
    expiry = models.DateTimeField(null=True)
    verified = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.information

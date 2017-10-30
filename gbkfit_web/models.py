# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
import django.contrib.auth.models as auth_models
from django.db import models
from django_countries.fields import CountryField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

MINIMUM_POSITIVE_NON_ZERO_FLOAT = 0.000001 

class User(auth_models.AbstractUser):
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    NOT_DISCLOSED = ''
    MR = 'Mr'
    MS = 'Ms'
    MRS = 'Mrs'
    DR = 'Dr'
    PROF = 'Prof'
    A_PROF = 'A/Prof'

    TITLE_CHOICES = [
        (NOT_DISCLOSED, NOT_DISCLOSED),
        (MR, MR),
        (MS, MS),
        (MRS, MRS),
        (DR, DR),
        (PROF, PROF),
        (A_PROF, A_PROF),
    ]

    MALE = 'Male'
    FEMALE = 'Female'
    GENDER_CHOICES = [
        (NOT_DISCLOSED, NOT_DISCLOSED),
        (FEMALE, FEMALE),
        (MALE, MALE),
    ]

    title = models.CharField(max_length=10, choices=TITLE_CHOICES, default=NOT_DISCLOSED, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default=NOT_DISCLOSED, blank=True)
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

    def __str__(self):
        return u'%s %s %s (%s)' % (self.title, self.first_name, self.last_name, self.username)

    def as_json(self):
        return dict(
            user = self,
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
            ('user', 'id'),
        )

    def __unicode__(self):
        return '{}'.format(self.name)

    def __str__(self):
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

"""
    The following functions create the path to save files 
    in link to the user_id, job_id, and file category (data, error, mask)
    
    e.g. 
    ../media/user_<user_id>/job_<job_id>/<category>_file/filename.extension
    
"""
def user_job_datafile_directory_path(instance, filename):
    return '../media/user_{0}/job_{1}/data_files/{2}'.format(instance.job.user_id, instance.job.id, filename)
def user_job_errorfile_directory_path(instance, filename):
    return '../media/user_{0}/job_{1}/error_files/{2}'.format(instance.job.user_id, instance.job.id, filename)
def user_job_maskfile_directory_path(instance, filename):
    return '../media/user_{0}/job_{1}/mask_files/{2}'.format(instance.job.user_id, instance.job.id, filename)

class DataSet(models.Model):
    """
        DataSet class

        DESCRIPTION:
        A dataset (in current stage of development) can consist of two type of files:
            * 3D - Spectral cube
            * 2D - Velocity map / Velocity Special Map

    """
    job = models.OneToOneField(Job, related_name='job_data_set')
    # CUBE = 'Cube'
    # IMAGE = 'Image'

    FLXMAP = 'flxmap'
    VELMAP = 'velmap'
    SIGMAP = 'sigmap'
    FLXCUBE = 'flxcube'

    TYPE_CHOICES = [
        (FLXMAP, 'Flux map'),
        (VELMAP, 'Velocity map'),
        (SIGMAP, 'Velocity dispersion map'),
        (FLXCUBE, 'Spectral cubes'),
    ]

    dataset1_type = models.CharField(max_length=10, choices=TYPE_CHOICES, blank=False, default=VELMAP)
    datafile1 = models.FileField(upload_to=user_job_datafile_directory_path)
    errorfile1 = models.FileField(upload_to=user_job_errorfile_directory_path, blank=True, null=True)
    maskfile1 = models.FileField(upload_to=user_job_maskfile_directory_path, blank=True, null=True)

    dataset2_type = models.CharField(max_length=10, choices=TYPE_CHOICES, blank=False, default=SIGMAP)
    datafile2 = models.FileField(upload_to=user_job_datafile_directory_path, blank=True, null=True)
    errorfile2 = models.FileField(upload_to=user_job_errorfile_directory_path, blank=True, null=True)
    maskfile2 = models.FileField(upload_to=user_job_maskfile_directory_path, blank=True, null=True)

    creation_time = models.DateTimeField(auto_now_add=True)

    # TODO: This will need a bit of work to enable any number of files...
    def as_array(self):
        # 1st batch of files
        file1_dict = {}
        file1_dict['type'] = self.dataset1_type
        file1_dict['data'] = self.datafile1.url
        try:
            file1_dict['error'] = self.errorfile1.url
        except:
            pass
        try:
            file1_dict['mask'] = self.maskfile1.url
        except:
            pass

        # 2nd batch of files
        file2_dict = {}
        try:
            file2_dict['data'] = self.datafile2.url
            file2_dict['type'] = self.dataset1_type
        except:
            pass
        try:
            file2_dict['error'] = self.errorfile2.url
        except:
            pass
        try:
            file2_dict['mask'] = self.maskfile2.url
        except:
            pass

        # Create the array
        result = [file1_dict]

        if bool(file2_dict):
            result.append(file2_dict)

        return result

class DataModel(models.Model):
    """
        DataModel class

        DESCRIPTION:
        There are four different types of dmodels (data models):
            * scube_omp
            * scube_cuda
            * mmaps_omp
            * mmaps_cuda

    """

    # job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_data_model')
    job = models.OneToOneField(Job, related_name='job_data_model')
    # name = models.CharField(max_length=255, blank=False, null=False)

    SCUBE_OMP = 'scube_omp'
    SCUBE_CUDA = 'scube_cuda'
    # MMNT_OMP = 'mmnt_omp'
    # MMNT_CUDA = 'mmnt_cuda'
    MMAPS_OMP = 'mmaps_omp'
    MMAPS_CUDA = 'mmaps_cuda'

    TYPE_CHOICES = [
        (SCUBE_OMP, SCUBE_OMP),
        (SCUBE_CUDA, SCUBE_CUDA),
        (MMAPS_OMP, MMAPS_OMP),
        (MMAPS_CUDA, MMAPS_CUDA)
    ]
    dmodel_type = models.CharField(max_length=10, choices=TYPE_CHOICES, blank=False, default=SCUBE_OMP)

    MOMENTS = 'moments'
    GAUSS = 'gauss'
    METHOD_TYPE_CHOICES = [
        (MOMENTS, MOMENTS),
        (GAUSS, GAUSS)
    ]
    method = models.CharField(max_length=10, choices=METHOD_TYPE_CHOICES, blank=False, default=MOMENTS)

    # size  --- Ignore this for now says George ---
    # ------------------------------------------------------------
    # (if cube: 3dims, if mmnt: 2dims?)
    #
    # size_x = models.PositiveIntegerField(blank=False, default=1)
    # size_y = models.PositiveIntegerField(blank=False, default=1)
    # # Need to figure out how to require the z field when required.
    # size_z = models.PositiveIntegerField(blank=True)

    scale_x = models.PositiveIntegerField(blank=False, default=1, validators=[MinValueValidator(1)])
    scale_y = models.PositiveIntegerField(blank=False, default=1, validators=[MinValueValidator(1)])
    scale_z = models.PositiveIntegerField(blank=True, default=1, validators=[MinValueValidator(1)])

    step_x = models.FloatField(blank=False, default=1., validators=[MinValueValidator(1.)])
    step_y = models.FloatField(blank=False, default=1., validators=[MinValueValidator(1.)])
    step_z = models.FloatField(blank=True, default=1., validators=[MinValueValidator(1.)])

    creation_time = models.DateTimeField(auto_now_add=True)

    def clean(self):
        errors = []

        if self.scale_x <= 0:
            errors.append(ValidationError({'scale_x':
                                               ['Scale X: Accepted values: unsigned non-zero integer value.']}))

        if self.scale_y <= 0:
            errors.append(ValidationError({'scale_y':
                                               ['Scale Y: Accepted values: unsigned non-zero integer value.']}))

        if self.scale_z <= 0:
            errors.append(ValidationError({'scale_z':
                                               ['Scale Z: Accepted values: unsigned non-zero integer value.']}))

        if self.step_x <= 0:
            errors.append(ValidationError({'step_x':
                                               ['Step X: Accepted values: unsigned non-zero value.']}))

        if self.step_y <= 0:
            errors.append(ValidationError({'step_y':
                                               ['Step Y: Accepted values: unsigned non-zero value.']}))

        if self.step_z <= 0:
            errors.append(ValidationError({'step_z':
                                               ['Step: Accepted values: unsigned non-zero value.']}))

        if len(errors) > 0: # Check if dict is empty. If not, raise error.
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        DataModel.full_clean(self)
        super(DataModel, self).save(*args, **kwargs)

    def as_json(self):
        if self.dmodel_type in [self.SCUBE_OMP, self.SCUBE_CUDA]:
            return dict(
                type="gbkfit.dmodel." + self.dmodel_type,
                step=[self.step_x, self.step_y, self.step_z],
                scale=[self.scale_x, self.scale_y, self.scale_z]
            )
        else:
            return dict(
                type="gbkfit.dmodel." + self.dmodel_type,
                method=self.method,
                step=[self.step_x, self.step_y],
                scale=[self.scale_x, self.scale_y],
            )

class PSF(models.Model):
    """
        PSF class

        DESCRIPTION:
        There are three different types of PSFs (Point Spread Functions):
            * gauss
            * moffat
            * lorentz

        There is also the option not to use an LSF at all. In this case there will be no JSON for the LSF.
    """
    # job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_psf')
    job = models.OneToOneField(Job, related_name='job_psf')
    # name = models.CharField(max_length=255, blank=False, null=False)

    GAUSS = 'gaussian'
    MOFFAT = 'moffat'
    LORENTZ = 'lorentzian'

    TYPE_CHOICES = [
        (GAUSS, GAUSS),
        (MOFFAT, MOFFAT),
        (LORENTZ, LORENTZ),
    ]
    psf_type = models.CharField(max_length=10, choices=TYPE_CHOICES, blank=False, default=GAUSS)

    fwhm_x = models.FloatField(blank=False, default=1., validators=[MinValueValidator(MINIMUM_POSITIVE_NON_ZERO_FLOAT)])
    fwhm_y = models.FloatField(blank=False, default=1., validators=[MinValueValidator(MINIMUM_POSITIVE_NON_ZERO_FLOAT)])
    pa = models.IntegerField(blank=False, default=1)
    # If Moffat, need to figure out how to require the following field.
    beta = models.FloatField(blank=False, default=1., validators=[MinValueValidator(MINIMUM_POSITIVE_NON_ZERO_FLOAT)])

    creation_time = models.DateTimeField(auto_now_add=True)

    def clean(self):
        errors = []

        if self.fwhm_x <= 0.:
            errors.append(ValidationError({'fwhm_x':
                                               ['FWHM X: Accepted values: positive non-zero value.']}))

        if self.fwhm_y <= 0.:
            errors.append(ValidationError({'fwhm_y':
                                               ['FWHM Y: Accepted values: positive non-zero value.']}))

        if self.beta <= 0.:
            errors.append(ValidationError({'fwhm':
                                               ['FWHM: Accepted values: positive non-zero value.']}))

        if len(errors) > 0: # Check if dict is empty. If not, raise error.
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        PSF.full_clean(self)
        super(PSF, self).save(*args, **kwargs)

    def as_json(self):
        if self.psf_type in [self.MOFFAT]:
            return dict(
                type=self.psf_type,
                fwhm_x=self.fwhm_x,
                fwhm_y=self.fwhm_y,
                pa=self.pa,
                beta=self.beta
            )
        else:
            return dict(
                type=self.psf_type,
                fwhm_x=self.fwhm_x,
                fwhm_y=self.fwhm_y,
                pa=self.pa
            )

class LSF(models.Model):
    """
    LSF class

    DESCRIPTION:
    There are three different types of LSFs (Line Spread Functions):
        * gauss
        * moffat
        * lorentz

    There is also the option not to use an LSF at all. In this case there will be no JSON for the LSF.
    """
    # job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_lsf')
    job = models.OneToOneField(Job, related_name='job_lsf')
    # name = models.CharField(max_length=255, blank=False, null=False)

    GAUSS = 'gaussian'
    MOFFAT = 'moffat'
    LORENTZ = 'lorentzian'

    TYPE_CHOICES = [
        (GAUSS, GAUSS),
        (MOFFAT, MOFFAT),
        (LORENTZ, LORENTZ),
    ]
    lsf_type = models.CharField(max_length=10, choices=TYPE_CHOICES, blank=False, default=GAUSS)

    fwhm = models.FloatField(blank=False, default=1., validators=[MinValueValidator(MINIMUM_POSITIVE_NON_ZERO_FLOAT)])
    # If Moffat, need to figure out how to require the following field.
    beta = models.FloatField(blank=False, default=1., validators=[MinValueValidator(MINIMUM_POSITIVE_NON_ZERO_FLOAT)])

    creation_time = models.DateTimeField(auto_now_add=True)

    def clean(self):
        errors = []

        if self.fwhm <= 0.:
            errors.append(ValidationError({'fwhm':
                                               ['FWHM: Accepted values: positive non-zero value.']}))

        if self.beta <= 0.:
            errors.append(ValidationError({'fwhm':
                                               ['FWHM: Accepted values: positive non-zero value.']}))

        if len(errors) > 0: # Check if dict is empty. If not, raise error.
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        LSF.full_clean(self)
        super(LSF, self).save(*args, **kwargs)

    def as_json(self):
        if self.lsf_type in [self.MOFFAT]:
            return dict(
                type=self.lsf_type,
                fwhm=self.fwhm,
                beta=self.beta
            )
        else:
            return dict(
                type=self.lsf_type,
                fwhm=self.fwhm
            )

class GalaxyModel(models.Model):
    """
        GalaxyModel (GModel) class.

        DESCRIPTION:
        A gmodel (galaxy model) includes a set of model prameters. Depending on how the gmodel is configured
        (the configuration is described in this document), a different set of model parameters are recognized.
        When building a gmodel JSON string you do not need to include anything about these model parameters.
        However, the names of these parameters are required when building the Paramset resource.

        There are two different types of gmodels (galaxy models):
            * thindisk_omp
            * thindisk_cuda

        All gmodels recognize the following model parameters:
            * xo
            * yo
            * pa
            * incl
            * vsys
            * vsig

        When the exponential flx_profile is used, the gmodel will also recognize the parameters i0 and r0.

        When the flat vel_profile is used, the gmodel will also recognize the parameters rt, vt.
        When the boissier vel_profile is used, the gmodel will also recognize the parameters rt, vt.
        When the arctan vel_profile is used, the gmodel will also recognize the parameters rt, vt.
        When the epinat vel_profile is used, the gmodel will also recognize the parameters rt, vt, a, b.
        (rings will come later).
    """
    # job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_gmodel')
    job = models.OneToOneField(Job, related_name='job_gmodel')
    # name = models.CharField(max_length=255, blank=False, null=False)

    THINDISK_OMP = 'thindisk_omp'
    THINDISK_CUDA = 'thindisk_cuda'

    TYPE_CHOICES = [
        (THINDISK_OMP, THINDISK_OMP),
        (THINDISK_CUDA, THINDISK_CUDA),
    ]
    gmodel_type = models.CharField(max_length=13, choices=TYPE_CHOICES, blank=False, default=THINDISK_OMP)

    EXPONENTIAL = 'exponential'
    FLAT= 'flat'
    BOISSIER = 'boissier'
    ARCTAN = 'arctan'
    EPINAT = 'epinat'
    # RINGS = 'rings'

    flx_profile_TYPE_CHOICES = [
        (EXPONENTIAL, EXPONENTIAL),
        # (RINGS, RINGS),
    ]
    flx_profile = models.CharField(max_length=11, choices=flx_profile_TYPE_CHOICES, blank=False, default=EXPONENTIAL)

    vel_profile_TYPE_CHOICES = [
        (EXPONENTIAL, EXPONENTIAL),
        (FLAT, FLAT),
        (BOISSIER, BOISSIER),
        (ARCTAN, ARCTAN),
        (EPINAT, EPINAT),
        # (RINGS, RINGS),
    ]
    vel_profile = models.CharField(max_length=11, choices=vel_profile_TYPE_CHOICES, blank=False, default=EXPONENTIAL)

    creation_time = models.DateTimeField(auto_now_add=True)

    def as_json(self):
        return dict(
            type=self.gmodel_type,
            flx_profile=self.flx_profile,
            vel_profile=self.vel_profile,
        )

class Fitter(models.Model):
    """
    Fitter class.

    DESCRIPTION:
    There are two different types of fitters (or optimisers):
        * mpfit
        * multinest

    Each type has a specific set of attributes.
    """
    job = models.OneToOneField(Job, related_name='job_fitter')

    MPFIT = 'mpfit'
    MULTINEST = 'multinest'

    TYPE_CHOICES = [
        (MPFIT, MPFIT),
        (MULTINEST, MULTINEST),
    ]
    fitter_type = models.CharField(max_length=10, choices=TYPE_CHOICES, blank=False, default=MPFIT)

    ZERO_ONE_CHOICES = [
        (0, 0),
        (1, 1),
    ]

    # MPFIT properties
    ftol = models.FloatField(blank=True, default=1, validators=[MinValueValidator(0. )])
    xtol = models.FloatField(blank=True, default=1, validators=[MinValueValidator(0. )])
    gtol = models.FloatField(blank=True, default=1, validators=[MinValueValidator(0. )])
    epsfcn = models.FloatField(blank=True, default=1, validators=[MinValueValidator(0. )])
    stepfactor = models.FloatField(blank=True, default=1, validators=[MinValueValidator(0. )])
    covtol = models.FloatField(blank=True, default=1, validators=[MinValueValidator(0. )])
    mpfit_maxiter = models.PositiveIntegerField(blank=True, default=1)
    maxfev = models.PositiveIntegerField(blank=True, default=1)
    nprint = models.BooleanField(blank=True, default=1)
    douserscale = models.BooleanField(blank=True, default=1)
    nofinitecheck = models.BooleanField(blank=True, default=1)

    # Multinest properties
    multinest_is = models.BooleanField(blank=True, default=True)
    mmodal = models.BooleanField(blank=True, default=0)
    nlive = models.PositiveIntegerField(blank=True, default=1, validators=[MinValueValidator(1)])
    tol = models.FloatField(blank=True, default=1., validators=[MinValueValidator(MINIMUM_POSITIVE_NON_ZERO_FLOAT)])
    efr = models.FloatField(blank=True, default=1., validators=[MinValueValidator(MINIMUM_POSITIVE_NON_ZERO_FLOAT)])
    ceff = models.BooleanField(blank=True, default=0)
    ztol = models.FloatField(blank=True, null=True, validators=[MinValueValidator(MINIMUM_POSITIVE_NON_ZERO_FLOAT)])
    logzero = models.FloatField(blank=True, null=True, validators=[MinValueValidator(MINIMUM_POSITIVE_NON_ZERO_FLOAT)])
    multinest_maxiter = models.IntegerField(blank=True, null=True, default=-1)
    seed = models.IntegerField(blank=True, null=True, )
    outfile = models.BooleanField(blank=True, default=1)

    creation_time = models.DateTimeField(auto_now_add=True)

    def clean(self):
        errors = []

        if self.fitter_type == self.MPFIT:
            if self.ftol < 0:
                errors.append(ValidationError({'ftol':
                                                   ['mpfit, ftol: Accepted values: any positive value.']}))

            if self.xtol < 0:
                errors.append(ValidationError({'xtol':
                                                   ['mpfit, xtol: Accepted values: any positive value.']}))

            if self.gtol < 0:
                errors.append(ValidationError({'gtol':
                                                   ['mpfit, gtol: Accepted values: any positive value.']}))

            if self.epsfcn < 0:
                errors.append(ValidationError({'epsfcn':
                                                   ['mpfit, epsfcn: Accepted values: any positive value.']}))

            if self.stepfactor < 0:
                errors.append(ValidationError({'stepfactor':
                                                   ['mpfit, stepfactor: Accepted values: any positive value.']}))

            if self.covtol < 0:
                errors.append(ValidationError({'covtol':
                                                   ['mpfit, covtol: Accepted values: any positive value.']}))

            if self.mpfit_maxiter < 0:
                errors.append(ValidationError({'maxiter':
                                                   ['mpfit, maxiter: Accepted values: any positive value.']}))

            if self.maxfev < 0:
                errors.append(ValidationError({'maxfev':
                                                   ['mpfit, maxfev: Accepted values: any positive value.']}))

        if self.fitter_type == self.MULTINEST:
            if self.nlive < 0:
                errors.append(ValidationError({'nlive':
                                                   ['Multinest, nlive: Accepted values: any positive non-zero integer value.']}))

            if self.tol < 0:
                errors.append(ValidationError({'tol':
                                                   ['Multinest, tol: Accepted values: any positive non-zero value.']}))

            if self.efr < 0:
                errors.append(ValidationError({'efr':
                                                   ['Multinest, efr: Accepted values: any positive non-zero value.']}))

            if self.ztol != None:
                if self.ztol < 0:
                    errors.append(ValidationError({'ztol':
                                                       ['Multinest, ztol: Accepted values: any positive non-zero value.']}))

            if self.logzero != None:
                if self.logzero < 0:
                    errors.append(ValidationError({'logzero':
                                                       ['Multinest, logzero: Accepted values: any positive non-zero value.']}))

            if self.outfile < 0:
                errors.append(ValidationError({'logzero':
                                                   ['Multinest, logzero: Accepted values: any positive non-zero value.']}))

        if len(errors) > 0: # Check if dict is empty. If not, raise error.
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        Fitter.full_clean(self)
        super(Fitter, self).save(*args, **kwargs)

    def as_json(self):
        """
        Return 'fitter' parameters into a json string (dictionary)

        :return: json dict
        """

        nprint = 1 if self.nprint else 0
        douserscale = 1 if self.douserscale else 0
        nofinitecheck = 1 if self.nofinitecheck else 0
        multinest_is = 1 if self.multinest_is else 0
        mmodal = 1 if self.mmodal else 0
        efr = 1 if self.efr else 0
        outfile = 1 if self.outfile else 0

        if self.fitter_type == self.MPFIT:
            return dict(
                    type="gbkfit.fitter." + self.fitter_type,
                    ftol = self.ftol,
                    xtol = self.xtol,
                    gtol = self.gtol,
                    epsfcn = self.epsfcn,
                    stepfactor = self.stepfactor,
                    covtol = self.covtol,
                    maxiter = self.mpfit_maxiter,
                    maxfev = self.maxfev,
                    nprint = nprint,
                    douserscale = douserscale,
                    nofinitecheck = nofinitecheck
                )
        else:
            return dict(
                    type="gbkfit.fitter." + self.fitter_type,
                    _is = multinest_is,
                    mmodal = mmodal,
                    nlive = self.nlive,
                    tol = self.tol,
                    efr = efr,
                    ceff = self.ceff,
                    ztol = self.ztol,
                    logzero = self.logzero,
                    maxiter = self.multinest_maxiter,
                    seed = self.seed,
                    outfile = outfile
                )

class ParameterSet(models.Model):
    """
        ParameterSet class

        DESCRIPTION:
        The paramset (parameter set) is a list of key-value pairs (dictionary).

        The keys of the dictionary are the model parameter names of the selected gmodel configuration.

        Different gmodel configurations may result in different parameter names.
        The values of the parameter dictionary are other dictionaries. Each with a series of parameter properties.
        """
    # job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_parameter_set')
    job = models.OneToOneField(Job, related_name='job_parameter_set')

    # COMMON TO ALL

    # xo
    xo_fixed = models.NullBooleanField(blank=True, default=0)
    xo_value = models.FloatField(blank=True, null=True, default=1)
    xo_min = models.FloatField(blank=True, null=True, default=1)
    xo_max = models.FloatField(blank=True, null=True, default=1)
    xo_wrap = models.PositiveIntegerField(blank=True, null=True, default=0, validators=[MaxValueValidator(1)])
    xo_step = models.FloatField(blank=True, null=True, default=0.)
    xo_relstep = models.FloatField(blank=True, null=True, default=0.)
    xo_side = models.PositiveIntegerField(blank=True, null=True, default=0, validators=[MaxValueValidator(3)])

    # yo
    yo_fixed = models.NullBooleanField(blank=True, default=0)
    yo_value = models.FloatField(blank=True, null=True, default=1)
    yo_min = models.FloatField(blank=True, null=True, default=1)
    yo_max = models.FloatField(blank=True, null=True, default=1)
    yo_wrap = models.PositiveIntegerField(blank=True, null=True, default=0, validators=[MaxValueValidator(1)])
    yo_step = models.FloatField(blank=True, null=True, default=0.)
    yo_relstep = models.FloatField(blank=True, null=True, default=0.)
    yo_side = models.PositiveIntegerField(blank=True, null=True, default=0, validators=[MaxValueValidator(3)])

    # pa
    pa_fixed = models.NullBooleanField(blank=True, default=0)
    pa_value = models.FloatField(blank=True, null=True, default=1)
    pa_min = models.FloatField(blank=True, null=True, default=1)
    pa_max = models.FloatField(blank=True, null=True, default=1)
    pa_wrap = models.PositiveIntegerField(blank=True, null=True, default=0, validators=[MaxValueValidator(1)])
    pa_step = models.FloatField(blank=True, null=True, default=0.)
    pa_relstep = models.FloatField(blank=True, null=True, default=0.)
    pa_side = models.PositiveIntegerField(blank=True, null=True, default=0, validators=[MaxValueValidator(3)])

    # incl
    incl_fixed = models.NullBooleanField(blank=True, default=0)
    incl_value = models.FloatField(blank=True, null=True, default=1)
    incl_min = models.FloatField(blank=True, null=True, default=1)
    incl_max = models.FloatField(blank=True, null=True, default=1)
    incl_wrap = models.PositiveIntegerField(blank=True, null=True, default=0, validators=[MaxValueValidator(1)])
    incl_step = models.FloatField(blank=True, null=True, default=0.)
    incl_relstep = models.FloatField(blank=True, null=True, default=0.)
    incl_side = models.PositiveIntegerField(blank=True, null=True, default=0, validators=[MaxValueValidator(3)])

    # vsys
    vsys_fixed = models.NullBooleanField(blank=True, default=0)
    vsys_value = models.FloatField(blank=True, null=True, default=1)
    vsys_min = models.FloatField(blank=True, null=True, default=1)
    vsys_max = models.FloatField(blank=True, null=True, default=1)
    vsys_wrap = models.PositiveIntegerField(blank=True, null=True, default=0, validators=[MaxValueValidator(1)])
    vsys_step = models.FloatField(blank=True, null=True, default=0.)
    vsys_relstep = models.FloatField(blank=True, null=True, default=0.)
    vsys_side = models.PositiveIntegerField(blank=True, null=True, default=0, validators=[MaxValueValidator(3)])

    # vsig
    vsig_fixed = models.NullBooleanField(blank=True, default=0)
    vsig_value = models.FloatField(blank=True, null=True, default=1)
    vsig_min = models.FloatField(blank=True, null=True, default=1)
    vsig_max = models.FloatField(blank=True, null=True, default=1)
    vsig_wrap = models.PositiveIntegerField(blank=True, null=True, default=0, validators=[MaxValueValidator(1)])
    vsig_step = models.FloatField(blank=True, null=True, default=0.)
    vsig_relstep = models.FloatField(blank=True, null=True, default=0.)
    vsig_side = models.PositiveIntegerField(blank=True, null=True, default=0, validators=[MaxValueValidator(3)])

    # i0
    i0_fixed = models.NullBooleanField(blank=True, default=0)
    i0_value = models.FloatField(blank=True, null=True, default=1)
    i0_min = models.FloatField(blank=True, null=True, default=1)
    i0_max = models.FloatField(blank=True, null=True, default=1)
    i0_wrap = models.PositiveIntegerField(blank=True, null=True, default=0, validators=[MaxValueValidator(1)])
    i0_step = models.FloatField(blank=True, null=True, default=0.)
    i0_relstep = models.FloatField(blank=True, null=True, default=0.)
    i0_side = models.PositiveIntegerField(blank=True, null=True, default=0, validators=[MaxValueValidator(3)])

    # r0
    r0_fixed = models.NullBooleanField(blank=True, default=0)
    r0_value = models.FloatField(blank=True, null=True, default=1)
    r0_min = models.FloatField(blank=True, null=True, default=1)
    r0_max = models.FloatField(blank=True, null=True, default=1)
    r0_wrap = models.PositiveIntegerField(blank=True, null=True, default=0, validators=[MaxValueValidator(1)])
    r0_step = models.FloatField(blank=True, null=True, default=0.)
    r0_relstep = models.FloatField(blank=True, null=True, default=0.)
    r0_side = models.PositiveIntegerField(blank=True, null=True, default=0, validators=[MaxValueValidator(3)])

    # CASE-BASED

    # rt
    rt_fixed = models.NullBooleanField(blank=True, default=0)
    rt_value = models.FloatField(blank=True, null=True, default=1)
    rt_min = models.FloatField(blank=True, null=True, default=1)
    rt_max = models.FloatField(blank=True, null=True, default=1)
    rt_wrap = models.PositiveIntegerField(blank=True, null=True, default=0, validators=[MaxValueValidator(1)])
    rt_step = models.FloatField(blank=True, null=True, default=0.)
    rt_relstep = models.FloatField(blank=True, null=True, default=0.)
    rt_side = models.PositiveIntegerField(blank=True, null=True, default=0, validators=[MaxValueValidator(3)])

    # vt
    vt_fixed = models.NullBooleanField(blank=True, null=True, default=0)
    vt_value = models.FloatField(blank=True, null=True, default=1)
    vt_min = models.FloatField(blank=True, null=True, default=1)
    vt_max = models.FloatField(blank=True, null=True, default=1)
    vt_wrap = models.PositiveIntegerField(blank=True, null=True, default=0, validators=[MaxValueValidator(1)])
    vt_step = models.FloatField(blank=True, null=True, default=0.)
    vt_relstep = models.FloatField(blank=True, null=True, default=0.)
    vt_side = models.PositiveIntegerField(blank=True, null=True, default=0, validators=[MaxValueValidator(3)])

    # a
    a_fixed = models.NullBooleanField(blank=True, default=0)
    a_value = models.FloatField(blank=True, null=True, default=1)
    a_min = models.FloatField(blank=True, null=True, default=1)
    a_max = models.FloatField(blank=True, null=True, default=1)
    a_wrap = models.PositiveIntegerField(blank=True, null=True, default=0, validators=[MaxValueValidator(1)])
    a_step = models.FloatField(blank=True, null=True, default=0.)
    a_relstep = models.FloatField(blank=True, null=True, default=0.)
    a_side = models.PositiveIntegerField(blank=True, null=True, default=0, validators=[MaxValueValidator(3)])

    # b
    b_fixed = models.NullBooleanField(blank=True, default=0)
    b_value = models.FloatField(blank=True, null=True, default=1)
    b_min = models.FloatField(blank=True, null=True, default=1)
    b_max = models.FloatField(blank=True, null=True, default=1)
    b_wrap = models.PositiveIntegerField(blank=True, null=True, default=0, validators=[MaxValueValidator(1)])
    b_step = models.FloatField(blank=True, null=True, default=0.)
    b_relstep = models.FloatField(blank=True, null=True, default=0.)
    b_side = models.PositiveIntegerField(blank=True, null=True, default=0, validators=[MaxValueValidator(3)])

    creation_time = models.DateTimeField(auto_now_add=True)

    def clean(self):
        errors = []
        # xo
        if self.xo_fixed == 1:
            if self.xo_min > self.xo_max:
                errors.append(ValidationError({'xo_min': ['xo: Minimum must be smaller than or equal to the maximum.']}))

            elif self.xo_value < self.xo_min or self.xo_value > self.xo_max:
                errors.append(ValidationError({'xo_value': ['xo: Value must be within range set by minimum and maximum.']}))

        # yo
        if self.yo_fixed == 1:
            if self.yo_min > self.yo_max:
                errors.append(ValidationError({'yo_min': ['yo: Minimum must be smaller than or equal to the maximum.']}))

            elif self.yo_value < self.yo_min or self.yo_value > self.yo_max:
                errors.append(ValidationError({'yo_value': ['yo: Value must be within range set by minimum and maximum.']}))

        # pa
        if self.pa_fixed == 1:
            if self.pa_min > self.pa_max:
                errors.append(ValidationError({'pa_min': ['pa: Minimum must be smaller than or equal to the maximum.']}))

            elif self.pa_value < self.pa_min or self.pa_value > self.pa_max:
                errors.append(ValidationError({'pa_value': ['pa: Value must be within range set by minimum and maximum.']}))

        # incl
        if self.incl_fixed == 1:
            if self.incl_min > self.incl_max:
                errors.append(ValidationError({'incl_min': ['incl: Minimum must be smaller than or equal to the maximum.']}))

            elif self.incl_value < self.incl_min or self.incl_value > self.incl_max:
                errors.append(ValidationError({'incl_value': ['incl: Value must be within range set by minimum and maximum.']}))

        # vsys
        if self.vsys_fixed == 1:
            if self.vsys_min > self.vsys_max:
                errors.append(ValidationError(
                    {'vsys_min': ['vsys: Minimum must be smaller than or equal to the maximum.']}))

            elif self.vsys_value < self.vsys_min or self.vsys_value > self.vsys_max:
                errors.append(ValidationError(
                    {'vsys_value': ['vsys: Value must be within range set by minimum and maximum.']}))

        # vsig
        if self.vsig_fixed == 1:
            if self.vsig_min > self.vsig_max:
                errors.append(ValidationError(
                    {'vsig_min': ['vsig: Minimum must be smaller than or equal to the maximum.']}))

            elif self.vsig_value < self.vsig_min or self.vsig_value > self.vsig_max:
                errors.append(ValidationError(
                    {'vsig_value': ['vsig: Value must be within range set by minimum and maximum.']}))

        # i0
        if self.i0_fixed == 1:
            if self.i0_min > self.i0_max:
                errors.append(
                    ValidationError({'i0_min': ['i0: Minimum must be smaller than or equal to the maximum.']}))
            elif self.i0_value < self.i0_min or self.i0_value > self.i0_max:
                errors.append(ValidationError(
                    {'i0_value': ['i0: Value must be within range set by minimum and maximum.']}))

        # r0
        if self.r0_fixed == 1:
            if self.r0_min > self.r0_max:
                errors.append(
                    ValidationError({'r0_min': ['r0: Minimum must be smaller than or equal to the maximum.']}))

            elif self.r0_value < self.r0_min or self.r0_value > self.r0_max:
                errors.append(ValidationError(
                    {'r0_value': ['r0: Value must be within range set by minimum and maximum.']}))

        # rt
        if self.rt_fixed == 1:
            if self.rt_min > self.rt_max:
                errors.append(ValidationError({'rt_min': ['rt: Minimum must be smaller than or equal to the maximum.']}))

            elif self.rt_value < self.rt_min or self.rt_value > self.rt_max:
                errors.append(ValidationError({'rt_value': ['rt: Value must be within range set by minimum and maximum.']}))

        # vt
        if self.vt_fixed == 1:
            if self.vt_min > self.vt_max:
                errors.append(ValidationError({'vt_min': ['vt: Minimum must be smaller than or equal to the maximum.']}))

            elif self.vt_value < self.vt_min or self.vt_value > self.vt_max:
                errors.append(ValidationError({'vt_value': ['vt: Value must be within range set by minimum and maximum.']}))

        # a
        if self.a_fixed == 1:
            if self.a_min > self.a_max:
                errors.append(
                    ValidationError({'a_min': ['a: Minimum must be smaller than or equal to the maximum.']}))

            elif self.a_value < self.a_min or self.a_value > self.a_max:
                errors.append(
                    ValidationError({'a_value': ['a: Value must be within range set by minimum and maximum.']}))

        # b
        if self.b_fixed == 1:
            if self.b_min > self.b_max:
                errors.append(
                    ValidationError({'b_min': ['b: Minimum must be smaller than or equal to the maximum.']}))

            elif self.b_value < self.b_min or self.b_value > self.b_max:
                errors.append(
                    ValidationError({'b_value': ['b: Value must be within range set by minimum and maximum.']}))

        if len(errors) > 0: # Check if dict is empty. If not, raise error.
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        ParameterSet.full_clean(self)
        super(ParameterSet, self).save(*args, **kwargs)

    def as_array(self):
        return [ self.xo_dict(),
                 self.yo_dict(),
                 self.pa_dict(),
                 self.incl_dict(),
                 self.vsys_dict(),
                 self.vsig_dict(),
                 self.i0_dict(),
                 self.r0_dict(),
                 self.rt_dict(),
                 self.vt_dict(),
                 self.a_dict(),
                 self.b_dict()
                 ]

    def xo_dict(self):
        # xo
        xo_dict = {
            'name': 'xo'
        }
        try:
            xo_fixed = 1 if self.xo_fixed else 0
            xo_dict['fixed'] = xo_fixed
        except:
            pass

        try:
            xo_dict['value'] = self.xo_value
        except:
            pass

        try:
            xo_dict['min'] = self.xo_min
        except:
            pass

        try:
            xo_dict['max'] = self.xo_max
        except:
            pass
        try:
            xo_dict['wrap'] = self.xo_wrap
        except:
            pass

        try:
            xo_dict['step'] = self.xo_step
        except:
            pass

        try:
            xo_dict['relstep'] = self.xo_relstep
        except:
            pass

        try:
            xo_dict['side'] = self.xo_side
        except:
            pass

        try:
            xo_dict['error'] = self.errorfile1.path
        except:
            pass
        try:
            xo_dict['mask'] = self.maskfile1.path
        except:
            pass

        return xo_dict

    def yo_dict(self):
        # yo
        yo_dict = {
            'name': 'yo'
        }
        try:
            yo_fixed = 1 if self.yo_fixed else 0
            yo_dict['fixed'] = yo_fixed
        except:
            pass

        try:
            yo_dict['value'] = self.yo_value
        except:
            pass

        try:
            yo_dict['min'] = self.yo_min
        except:
            pass

        try:
            yo_dict['max'] = self.yo_max
        except:
            pass
        try:
            yo_dict['wrap'] = self.yo_wrap
        except:
            pass

        try:
            yo_dict['step'] = self.yo_step
        except:
            pass

        try:
            yo_dict['relstep'] = self.yo_relstep
        except:
            pass

        try:
            yo_dict['side'] = self.yo_side
        except:
            pass

        try:
            yo_dict['error'] = self.errorfile1.path
        except:
            pass
        try:
            yo_dict['mask'] = self.maskfile1.path
        except:
            pass

        return yo_dict

    def pa_dict(self):
        # pa
        pa_dict = {
            'name': 'pa'
        }
        try:
            pa_fixed = 1 if self.pa_fixed else 0
            pa_dict['fixed'] = pa_fixed
        except:
            pass

        try:
            pa_dict['value'] = self.pa_value
        except:
            pass

        try:
            pa_dict['min'] = self.pa_min
        except:
            pass

        try:
            pa_dict['max'] = self.pa_max
        except:
            pass
        try:
            pa_dict['wrap'] = self.pa_wrap
        except:
            pass

        try:
            pa_dict['step'] = self.pa_step
        except:
            pass

        try:
            pa_dict['relstep'] = self.pa_relstep
        except:
            pass

        try:
            pa_dict['side'] = self.pa_side
        except:
            pass

        try:
            pa_dict['error'] = self.errorfile1.path
        except:
            pass
        try:
            pa_dict['mask'] = self.maskfile1.path
        except:
            pass

        return pa_dict

    def incl_dict(self):
        # incl
        incl_dict = {
            'name': 'incl'
        }
        try:
            incl_fixed = 1 if self.incl_fixed else 0
            incl_dict['fixed'] = incl_fixed
        except:
            pass

        try:
            incl_dict['value'] = self.incl_value
        except:
            pass

        try:
            incl_dict['min'] = self.incl_min
        except:
            pass

        try:
            incl_dict['max'] = self.incl_max
        except:
            pass
        try:
            incl_dict['wrap'] = self.incl_wrap
        except:
            pass

        try:
            incl_dict['step'] = self.incl_step
        except:
            pass

        try:
            incl_dict['relstep'] = self.incl_relstep
        except:
            pass

        try:
            incl_dict['side'] = self.incl_side
        except:
            pass

        try:
            incl_dict['error'] = self.errorfile1.path
        except:
            pass
        try:
            incl_dict['mask'] = self.maskfile1.path
        except:
            pass

        return incl_dict

    def vsys_dict(self):
        # vsys
        vsys_dict = {
            'name': 'vsys'
        }
        try:
            vsys_fixed = 1 if self.vsys_fixed else 0
            vsys_dict['fixed'] = vsys_fixed
        except:
            pass

        try:
            vsys_dict['value'] = self.vsys_value
        except:
            pass

        try:
            vsys_dict['min'] = self.vsys_min
        except:
            pass

        try:
            vsys_dict['max'] = self.vsys_max
        except:
            pass
        try:
            vsys_dict['wrap'] = self.vsys_wrap
        except:
            pass

        try:
            vsys_dict['step'] = self.vsys_step
        except:
            pass

        try:
            vsys_dict['relstep'] = self.vsys_relstep
        except:
            pass

        try:
            vsys_dict['side'] = self.vsys_side
        except:
            pass

        try:
            vsys_dict['error'] = self.errorfile1.path
        except:
            pass
        try:
            vsys_dict['mask'] = self.maskfile1.path
        except:
            pass

        return vsys_dict

    def vsig_dict(self):
        # vsig
        vsig_dict = {
            'name': 'vsig'
        }
        try:
            vsig_fixed = 1 if self.vsig_fixed else 0
            vsig_dict['fixed'] = vsig_fixed
        except:
            pass

        try:
            vsig_dict['value'] = self.vsig_value
        except:
            pass

        try:
            vsig_dict['min'] = self.vsig_min
        except:
            pass

        try:
            vsig_dict['max'] = self.vsig_max
        except:
            pass
        try:
            vsig_dict['wrap'] = self.vsig_wrap
        except:
            pass

        try:
            vsig_dict['step'] = self.vsig_step
        except:
            pass

        try:
            vsig_dict['relstep'] = self.vsig_relstep
        except:
            pass

        try:
            vsig_dict['side'] = self.vsig_side
        except:
            pass

        try:
            vsig_dict['error'] = self.errorfile1.path
        except:
            pass
        try:
            vsig_dict['mask'] = self.maskfile1.path
        except:
            pass

        return vsig_dict

    def i0_dict(self):
        # i0
        i0_dict = {
            'name': 'i0'
        }
        try:
            i0_fixed = 1 if self.i0_fixed else 0
            i0_dict['fixed'] = i0_fixed
        except:
            pass

        try:
            i0_dict['value'] = self.i0_value
        except:
            pass

        try:
            i0_dict['min'] = self.i0_min
        except:
            pass

        try:
            i0_dict['max'] = self.i0_max
        except:
            pass
        try:
            i0_dict['wrap'] = self.i0_wrap
        except:
            pass

        try:
            i0_dict['step'] = self.i0_step
        except:
            pass

        try:
            i0_dict['relstep'] = self.i0_relstep
        except:
            pass

        try:
            i0_dict['side'] = self.i0_side
        except:
            pass

        try:
            i0_dict['error'] = self.errorfile1.path
        except:
            pass
        try:
            i0_dict['mask'] = self.maskfile1.path
        except:
            pass

        return i0_dict

    def r0_dict(self):
        # r0
        r0_dict = {
            'name': 'r0'
        }
        try:
            r0_fixed = 1 if self.r0_fixed else 0
            r0_dict['fixed'] = r0_fixed
        except:
            pass

        try:
            r0_dict['value'] = self.r0_value
        except:
            pass

        try:
            r0_dict['min'] = self.r0_min
        except:
            pass

        try:
            r0_dict['max'] = self.r0_max
        except:
            pass
        try:
            r0_dict['wrap'] = self.r0_wrap
        except:
            pass

        try:
            r0_dict['step'] = self.r0_step
        except:
            pass

        try:
            r0_dict['relstep'] = self.r0_relstep
        except:
            pass

        try:
            r0_dict['side'] = self.r0_side
        except:
            pass

        try:
            r0_dict['error'] = self.errorfile1.path
        except:
            pass
        try:
            r0_dict['mask'] = self.maskfile1.path
        except:
            pass

        return r0_dict

    def rt_dict(self):
        # rt
        rt_dict = {
            'name': 'rt'
        }
        try:
            rt_fixed = 1 if self.rt_fixed else 0
            rt_dict['fixed'] = rt_fixed
        except:
            pass

        try:
            rt_dict['value'] = self.rt_value
        except:
            pass

        try:
            rt_dict['min'] = self.rt_min
        except:
            pass

        try:
            rt_dict['max'] = self.rt_max
        except:
            pass
        try:
            rt_dict['wrap'] = self.rt_wrap
        except:
            pass

        try:
            rt_dict['step'] = self.rt_step
        except:
            pass

        try:
            rt_dict['relstep'] = self.rt_relstep
        except:
            pass

        try:
            rt_dict['side'] = self.rt_side
        except:
            pass

        try:
            rt_dict['error'] = self.errorfile1.path
        except:
            pass
        try:
            rt_dict['mask'] = self.maskfile1.path
        except:
            pass

        return rt_dict

    def vt_dict(self):
        # vt
        vt_dict = {
            'name': 'vt'
        }
        try:
            vt_fixed = 1 if self.vt_fixed else 0
            vt_dict['fixed'] = vt_fixed
        except:
            pass

        try:
            vt_dict['value'] = self.vt_value
        except:
            pass

        try:
            vt_dict['min'] = self.vt_min
        except:
            pass

        try:
            vt_dict['max'] = self.vt_max
        except:
            pass
        try:
            vt_dict['wrap'] = self.vt_wrap
        except:
            pass

        try:
            vt_dict['step'] = self.vt_step
        except:
            pass

        try:
            vt_dict['relstep'] = self.vt_relstep
        except:
            pass

        try:
            vt_dict['side'] = self.vt_side
        except:
            pass

        try:
            vt_dict['error'] = self.errorfile1.path
        except:
            pass
        try:
            vt_dict['mask'] = self.maskfile1.path
        except:
            pass

        return vt_dict

    def a_dict(self):
        # a
        a_dict = {
            'name': 'a'
        }
        try:
            a_fixed = 1 if self.a_fixed else 0
            a_dict['fixed'] = a_fixed
        except:
            pass

        try:
            a_dict['value'] = self.a_value
        except:
            pass

        try:
            a_dict['min'] = self.a_min
        except:
            pass

        try:
            a_dict['max'] = self.a_max
        except:
            pass
        try:
            a_dict['wrap'] = self.a_wrap
        except:
            pass

        try:
            a_dict['step'] = self.a_step
        except:
            pass

        try:
            a_dict['relstep'] = self.a_relstep
        except:
            pass

        try:
            a_dict['side'] = self.a_side
        except:
            pass

        try:
            a_dict['error'] = self.errorfile1.path
        except:
            pass
        try:
            a_dict['mask'] = self.maskfile1.path
        except:
            pass

        return a_dict

    def b_dict(self):
        # b
        b_dict = {
            'name': 'b'
        }
        try:
            b_fixed = 1 if self.b_fixed else 0
            b_dict['fixed'] = b_fixed
        except:
            pass

        try:
            b_dict['value'] = self.b_value
        except:
            pass

        try:
            b_dict['min'] = self.b_min
        except:
            pass

        try:
            b_dict['max'] = self.b_max
        except:
            pass
        try:
            b_dict['wrap'] = self.b_wrap
        except:
            pass

        try:
            b_dict['step'] = self.b_step
        except:
            pass

        try:
            b_dict['relstep'] = self.b_relstep
        except:
            pass

        try:
            b_dict['side'] = self.b_side
        except:
            pass

        try:
            b_dict['error'] = self.errorfile1.path
        except:
            pass
        try:
            b_dict['mask'] = self.maskfile1.path
        except:
            pass

        return b_dict

class Verification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    information = models.CharField(max_length=1024)
    expiry = models.DateTimeField(null=True)
    verified = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.information

    def __str__(self):
        return u'%s' % self.information


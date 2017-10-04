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
        (DRAFT, 'Draft'),
        (SUBMITTED, 'Submitted'),
        (QUEUED, 'Queued'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
        (ERROR, 'Error'),
        (SAVED, 'Saved'),
        (WALL_TIME_EXCEEDED, 'Wall Time Exceeded'),
        (DELETED, 'Deleted'),
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


class Verification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    information = models.CharField(max_length=1024)
    expiry = models.DateTimeField(null=True)
    verified = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.information

"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profile_picture = models.CharField(max_length=30, blank=True)
    

    def __unicode__(self):
        return self.user

class Course(models.Model):
    course_name = models.CharField(max_length=30)
    course_code = models.CharField(max_length=8)
    course_description = models.TextField()

class Lecture(models.Model):
    Lecture_name = models.CharField(max_length=30)
    Lecture_week = models.IntegerField()
    # add a file field or some sort later
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

class Class(models.Model):
    class_name = models.CharField(max_length=30)
    class_description = models.TextField()
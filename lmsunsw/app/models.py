"""
Definition of models.
"""

from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
import re

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profile_picture = models.CharField(max_length=30, blank=True)
    
    # like a toString
    def __unicode__(self):
        return unicode(self.user)



class Course(models.Model):
    course_name = models.CharField(max_length=30)
    course_code = models.CharField(max_length=8, unique=True, validators=[RegexValidator(regex=r'^[A-Z]{4}[0-9]{4}$', message="Course Code is invalid", code='invalid_course_code')])
    course_description = models.TextField()
    course_head_lecturer = models.ForeignKey(User)

    # like a toString
    def __unicode__(self):
        return unicode(self.course_code)

    def get_absolute_url(self):
        return "/course/" + self.course_code

class Lecture(models.Model):
    lecture_name = models.CharField(max_length=30)
    lecture_number = models.IntegerField()
    course = models.ForeignKey(Course)
    # add a file field or some sort later

    class Meta:
        unique_together = ('course','lecture_number')

    def __unicode__(self):
        return unicode(self.course.course_code + "/" + str(self.lecture_number))

    def get_absolute_url(self):
        return "/course/" + self.course.course_code + "/" + str(self.lecture_number)

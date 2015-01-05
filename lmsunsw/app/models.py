"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profile_picture = models.CharField(max_length=30, blank=True)
    
    # like a toString
    def __unicode__(self):
        return unicode(self.user)



class Course(models.Model):
    course_name = models.CharField(max_length=30)
    course_code = models.CharField(max_length=8)
    course_description = models.TextField()
    course_head_lecturer = models.ForeignKey(User)

    # like a toString
    def __unicode__(self):
        return unicode(self.course_code)

    def get_absolute_url(self):
        return "/course/"+self.course_code

class Lecture(models.Model):
    lecture_name = models.CharField(max_length=30)
    lecture_week = models.IntegerField()
    course_lecture = models.ForeignKey(Course)
    # add a file field or some sort later

    def __unicode__(self):
        return unicode(self.course_lecture + "/" + self.lecture_week)

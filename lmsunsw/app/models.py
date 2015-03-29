"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User
from fluent_contents.models import PlaceholderField
import string

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profile_picture = PlaceholderField("profile_picture")
    
    # like a toString
    def __unicode__(self):
        return unicode(self.user)

class Lecture(models.Model):
    lecture_name = models.CharField(max_length=30, unique=True)
    collab_doc = PlaceholderField("collab_doc")

    @property
    def get_slug_field(self):
        return self.lecture_name.replace(' ','_')

    @property
    def get_absolute_url(self):
        return self.id + "/" + get_slug_field()

    def __unicode__(self):
        return unicode(self.lecture_name)

class Quiz(models.Model):
    question = models.TextField()
    visible = models.BooleanField(default=False)
    Lecture = models.ForeignKey(Lecture)

    def __unicode__(self):
        return unicode(self.Lecture.lecture_name + " " + self.question)


class QuizChoice(models.Model):
    choice = models.TextField()
    Quiz = models.ForeignKey(Quiz)
    correct = models.BooleanField(default=False)
    #times_chosen = models.PositiveSmallIntegerField()
    

class QuizChoiceSelected(models.Model):
    user = models.ForeignKey(User)
    quiz_choice = models.ForeignKey(QuizChoice)

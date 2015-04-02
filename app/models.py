"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User
import string

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile')
    # like a toString
    def __unicode__(self):
        return unicode(self.user)

class Lecture(models.Model):
    lecture_name = models.CharField(max_length=30, unique=True)
    lecture_slide = models.URLField(blank=True, null=True, help_text="Optional, Provide a URL link to the lecture slides to be displayed")
    collab_doc = models.URLField(blank=True, null=True, help_text="Optional, Provide a URL Link to a specific google docs, a blank default will be used if empty")

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
    @property
    def times_chosen(self):
        return len(QuizChoiceSelected.objects.filter(quiz_choice=self.id))

class QuizChoiceSelected(models.Model):
    user = models.ForeignKey(User)
    quiz_choice = models.ForeignKey(QuizChoice)

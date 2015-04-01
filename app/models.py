"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User
from fluent_contents.models import PlaceholderField
from fluent_contents.models import Placeholder
import string

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile')
    profile_picture = PlaceholderField("profile_picture")
    # like a toString
    def __unicode__(self):
        return unicode(self.user)

class Lecture(models.Model):
    lecture_name = models.CharField(max_length=30, unique=True)
    collab_doc = PlaceholderField("lecture_docs")

    @property
    def lecture_docs_used(self):
        #returns whether the PlaceholderField is being used or not
        return bool(len(Placeholder.objects.filter(slot='lecture_docs', parent_id=self.id)))

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

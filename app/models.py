"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User
import string
from app.docsURL import glist
from autoslug import AutoSlugField

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile')
    # like a toString
    def __unicode__(self):
        return unicode(self.user)

class Lecture(models.Model):
    lecture_name = models.CharField(max_length=30, unique=True)
    lecture_slide = models.URLField(blank=True, null=True, help_text="Optional, Provide a URL link to the lecture slides to be displayed")
    collab_doc = models.URLField(blank=True, null=True, help_text="Optional, Provide a URL Link to a specific google docs, a blank default will be used if empty")
    slug = AutoSlugField(populate_from='lecture_name')

    @property
    def get_slug_field(self):
        return self.lecture_name.replace(' ','_')

    @property
    def get_absolute_url(self):
        return self.id + "/" + self.slug

    def __unicode__(self):
        return unicode(self.lecture_name)

    @staticmethod
    def gdoc_used(gdoc):
        for lecture in Lecture.objects.all():
            if lecture.collab_doc == gdoc:
                return True
        return False

    @staticmethod
    def get_unused_gdoc():
        for gdoc in glist:
            used = False
            for lecture in Lecture.objects.all():
                if lecture.collab_doc == gdoc:
                    used = True
            if used == False:
                # no lectures are using this gdoc
                return gdoc
        # no unused gdocs
        return ""

    def save(self, *args, **kwargs):
        if self.collab_doc == None:
            # no collab docs has been specified, need to link it with an ununsed gdoc
            self.collab_doc = Lecture.get_unused_gdoc()
        return super(Lecture, self).save(*args, **kwargs)

class QuizType():
    # represents an enum
    # one right answer
    SINGLEMCQ = 1
    # multiple right answers
    MULTIMCQ = 2
    # zero right answers
    ZEROMCQ = 3

class Quiz(models.Model):
    question = models.TextField()
    visible = models.BooleanField(default=False)
    Lecture = models.ForeignKey(Lecture)

    def __unicode__(self):
        return unicode(self.Lecture.lecture_name + " " + self.question)

    @property
    def quiz_type(self):
    # must return an enum of QuizType
        quiz_choice_list = QuizChoice.objects.filter(Quiz=self.id)
        # acan ssume that for each quiz, there must always be at least 2 choice associated
        num_correct = len(QuizChoice.objects.filter(Quiz=self.id, correct=True))
        if num_correct == 0:
            return QuizType.ZEROMCQ
        elif num_correct == 1:
            return QuizType.SINGLEMCQ
        else:
            # for all else it is multimcq
            return QuizType.MULTIMCQ

class QuizChoice(models.Model):
    choice = models.TextField()
    Quiz = models.ForeignKey(Quiz)
    correct = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.choice)


    @property
    def times_chosen(self):
        return len(QuizChoiceSelected.objects.filter(QuizChoice=self.id))

class QuizChoiceSelected(models.Model):
    User = models.ForeignKey(User)
    QuizChoice = models.ForeignKey(QuizChoice)

    class Meta:
        unique_together = ('User', 'QuizChoice') 

class ConfidenceMeter(models.Model):
    User = models.OneToOneField(User)
    confidence = models.SmallIntegerField(default=0) # value of 0 means neutral

class Thread(models.Model):
    # to be thread head for posts to attach onto
    title = models.TextField()
    content = models.TextField()
    Creator = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    views = models.SmallIntegerField(default=0)
    slug = AutoSlugField(populate_from='title')
    last_post = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.title)

    @property
    def replies(self):
        replies = len(Post.objects.filter(Thread=self.id))
        return replies

    def inc_views(self):
        self.views = self.views + 1
        self.save()

class Post(models.Model):
    Thread = models.ForeignKey(Thread)
    content = models.TextField()
    Creator = models.ForeignKey(User)
    last_touch = models.DateTimeField(auto_now=True)
    rank = models.SmallIntegerField() # for ordering of posts
    anonymous = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.content)

    @property
    def Creator_name(self):
        return "anonymous" if self.anonymous else self.Creator

class Wordcloud(models.Model):
    title = models.CharField(max_length=30, unique=True)
    words = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='wordcloud')

    def __unicode__(self):
        return unicode(self.title)



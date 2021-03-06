"""
Definition of models.
"""

import string

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission

from autoslug import AutoSlugField


from pygments import highlight, styles
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_all_styles
from pygments.styles import STYLE_MAP

from app.docsURL import glist

class SeatLocation():
    # enum for seating categorisation
    # add to this class for more categories
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='UserProfile')
    personal_collab_doc = models.URLField(blank=True, null=True, help_text=_("Optional, Provide a URL Link to a specific google docs which will override the default public doc, you can share this with your friends to create small groups"))
    confidence_message = models.CharField(blank=True, null=True, max_length=50)
    seat_location = models.SmallIntegerField(default=SeatLocation.MIDDLE)
    # like a toString
    def __unicode__(self):
        return unicode(self.user)

    @receiver(post_save, sender=User)
    def addUserPermission(sender, **kwargs):
        from app.cache_helpers import get_user_permission, get_profile_permission
        if kwargs['created']:
            user = kwargs['instance']
            user.user_permissions.add(get_user_permission())
            user.user_permissions.add(get_profile_permission())
            user.is_staff = True
            user.save()
            try:
                UserProfile.objects.create(user=user, seat_location=user._seat_location)
            except AttributeError:
                # for programmatically creating users, default seat_location is middle, according to the model
                UserProfile.objects.create(user=user)


class Lecture(models.Model):
    title = models.CharField(max_length=30, unique=True)
    
    collab_doc = models.URLField(blank=True, null=True, help_text=_("Optional, Provide a URL Link to a specific google docs, a blank default will be used if empty"))
    slug = AutoSlugField(populate_from='title')

    @property
    def get_absolute_url(self):
        return _("%(id)s/%(slug)s") % {'id':self.id, 'slug':self.slug}

    def __unicode__(self):
        return unicode(self.title)

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
        return _("")

    def save(self, *args, **kwargs):
        if self.collab_doc == None:
            # no collab docs has been specified, need to link it with an ununsed gdoc
            self.collab_doc = Lecture.get_unused_gdoc()

        #check if this object is a new entry in db
        ret_val = super(Lecture, self).save(*args, **kwargs)
        cache.delete('lecture_list')
        return ret_val

    def delete(self, *args, **kwargs):
        cache.delete('lecture_list')
        return super(Lecture, self).delete(*args, **kwargs)


class LectureMaterial(models.Model):

    Lecture = models.ForeignKey(Lecture)
    local_lecture_material = models.FileField(upload_to="lecture", blank=True, null=True)
    online_lecture_material = models.URLField(blank=True, null=True)

    @property
    def serve_material(self):
        if self.online_lecture_material == u'':
            return self.local_lecture_material.url
        else:
            return self.online_lecture_material

class QuizType():
    # represents an enum
    # no right answers
    ZEROMCQ = 0
    # one right answer
    SINGLEMCQ = 1
    # multiple right answers
    MULTIMCQ = 2
    # freeform question
    FREEFORM = 3



class Quiz(models.Model):

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

    question = models.TextField()
    visible = models.BooleanField(default=False)
    Lecture = models.ForeignKey(Lecture)
    last_touch = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(populate_from='question')

    # code snippet fields, all are optional
    syntax = models.CharField(blank=True, null=True, max_length=30, choices=settings.LANGUAGE_CHOICES, default=settings.DEFAULT_LANGUAGE)
    code = models.TextField(blank=True, null=True, )

    # freeform answer, optional 
    answer = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return unicode(self.Lecture.title + " " + self.question)

    def save(self, *args, **kwargs):

        ret_val = super(Quiz, self).save(*args, **kwargs)
        cache.delete('current_quiz_list')
        return ret_val

    def delete(self, *args, **kwargs):

        # remove from cache before actual delete

        cache.delete('current_quiz_list')
        return super(Quiz, self).delete(*args, **kwargs)




    @property
    def render_code(self):
 
        if self.code != None and self.code != "":
            formatter = HtmlFormatter(style='default', nowrap=True, classprefix='code%s-' % self.pk)
            html = highlight(self.code, get_lexer_by_name(self.syntax), formatter)
            css = formatter.get_style_defs()
            # Included in a DIV, so the next item will be displayed below.
            return _('<div class="code"><style type="text/css">%(css)s</style>\n<pre>%(html)s</pre></div>\n') % {'css':css, 'html':html}

        return ""

    @property
    def quiz_type(self):
    # must return an enum of QuizType
        from app.cache_helpers import filter_quizchoice_list, filter_quizchoice_list_for_correct
        quiz_choice_list = filter_quizchoice_list(Quiz=self)

        if len(quiz_choice_list) == 0:
            return QuizType.FREEFORM

        num_correct = len(filter_quizchoice_list_for_correct(Quiz=self, correct=True))

        if num_correct == 1:
            return QuizType.SINGLEMCQ
        elif num_correct > 1:
            return QuizType.MULTIMCQ
        elif self.answer != u"" and self.answer != None:
            return QuizType.FREEFORM
        else:
            # must be ZEROMCQ
            return QuizType.ZEROMCQ


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
    QuizChoice = models.ForeignKey(QuizChoice, blank=True, null=True)
    # for when answer is for freeform quiz
    answer = models.TextField(blank=True, null=True)
    Quiz = models.ForeignKey(Quiz, blank=True, null=True)

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
    anonymous = models.BooleanField(default=True)
    replies = models.SmallIntegerField(default=0)

    def __unicode__(self):
        return unicode(self.title)

    def save(self, inc_view=None, *args, **kwargs):
         #check if this object is a new entry in db

        ret_val = super(Thread, self).save(*args, **kwargs)
        if inc_view != True:
            cache.delete('thread_list')
            
        return ret_val

    def delete(self, *args, **kwargs):

        # remove from caches before actual delete

        cache.delete('thread_list')
        return super(Thread, self).delete(*args, **kwargs)

    def inc_views(self):
        self.views = self.views + 1
        self.save(inc_view=True)

    def Creator_name(self):
        return _("anonymous") if self.anonymous else self.Creator.username

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
        return _("anonymous") if self.anonymous else self.Creator.username

    def save(self, *args, **kwargs):
        self.Thread.replies = self.Thread.replies + 1
        self.Thread.save()
        cache.delete('post_list')
        return super(Post, self).save(*args, **kwargs)


class CodeSnippet(models.Model):
    syntax = models.CharField(max_length=30, choices=settings.LANGUAGE_CHOICES, default=settings.DEFAULT_LANGUAGE)
    code = models.TextField()
    Lecture = models.ForeignKey(Lecture)

    class Meta:
        verbose_name = _('Code snippet')
        verbose_name_plural = _('Code snippets')

    def __str__(self):
        return Truncator(self.code).words(20)

    @property
    def render_code(self):
        formatter = HtmlFormatter(style='default', nowrap=True, classprefix='code%s-' % self.pk)
        html = highlight(self.code, get_lexer_by_name(self.syntax), formatter)
        css = formatter.get_style_defs()

        # Included in a DIV, so the next item will be displayed below.
        return _('<div class="code"><style type="text/css">%(css)s</style>\n<pre>%(html)s</pre></div>\n') % {'css':css, 'html':html}



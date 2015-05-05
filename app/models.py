"""
Definition of models.
"""

import string

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils.functional import cached_property
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

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='UserProfile')
    # like a toString
    def __unicode__(self):
        return unicode(self.user)

    @receiver(post_save, sender=User)
    def addUserPermission(sender, **kwargs):
        if kwargs['created']:
            user = kwargs['instance']
            user.user_permissions.add(get_permission())
            user.is_staff = True
            user.save()


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
        created = False
        if self.id == None:
            created = True
        ret_val = super(Lecture, self).save(*args, **kwargs)
            # update cache for lecture based entries
        if created == True:
            lecture_list = cache.get('lecture_list')
            try:
                lecture_list.append(self)
            except AttributeError:
                # first call, nothing in cache yet
                lecture_list = [self]
            cache.set('lecture_list', lecture_list)

        return ret_val

    def delete(self, *args, **kwargs):

        # remove from caches before actual delete

        lecture_list = cache.get('lecture_list')
        try:
            lecture_list.remove(self)
            cache.set('lecture_list', lecture_list)
        except ValueError:
            # not in list
            pass
        except AttributeError:
            # list is not a list, but None
            # and None does not have remove()
            pass    

        return super(Lecture, self).delete(*args, **kwargs)


class LectureMaterial(models.Model):

    Lecture = models.ForeignKey(Lecture)
    local_lecture_material = models.FileField(upload_to="lecture", blank=True, null=True)
    online_lecture_material = models.URLField(blank=True, null=True)

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

        if self.visible == True:
            # update current_quiz_list in cache
            current_quiz_list = cache.get('current_quiz_list')
            try:
                current_quiz_list.append(self)
            except AttributeError:
                # first call, nothing in cache yet
                current_quiz_list = [self]

            cache.set('current_quiz_list', current_quiz_list)
        elif self.visible == False:
            current_quiz_list = cache.get('current_quiz_list')
            try:
                current_quiz_list.remove(self)
                cache.set('current_quiz_list', current_quiz_list)
            except ValueError:
                # not in list
                pass
            except AttributeError:
                # list is not a list, but None
                # and None does not have remove()
                pass    
            
        return ret_val

    def delete(self, *args, **kwargs):

        # remove from caches before actual delete

        current_quiz_list = cache.get('current_quiz_list')
        try:
            current_quiz_list.remove(self)
            cache.set('current_quiz_list', current_quiz_list)
        except ValueError:
            # not in list
            pass
        except AttributeError:
            # list is not a list, but None
            # and None does not have remove()
            pass    

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

    @cached_property
    def quiz_type(self):
    # must return an enum of QuizType
        quiz_choice_list = QuizChoice.objects.filter(Quiz=self.id)
        # acan ssume that for each quiz, there must always be at least 2 choice associated
        num_correct = len(QuizChoice.objects.filter(Quiz=self.id, correct=True))
        
        
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

    def save(self, *args, **kwargs):
         #check if this object is a new entry in db
        created = False
        if self.id == None:
            created = True
        # save the object
        ret_val = super(Thread, self).save(*args, **kwargs)
            # update cache for lecture based entries
        if created == True:
            thread_list = cache.get('thread_list')
            try:
                thread_list.append(self)
            except AttributeError:
                # first call, nothing in cache yet
                thread_list = Thread.objects.all()
            cache.set('thread_list', thread_list, settings.THREAD_LIST_CACHE_INTERVAL)

        return ret_val

    def delete(self, *args, **kwargs):

        # remove from caches before actual delete

        thread_list = cache.get('thread_list')
        try:
            thread_list.remove(self)
            cache.set('thread_list', thread_list, settings.THREAD_LIST_CACHE_INTERVAL)
        except ValueError:
            # not in list
            pass
        except AttributeError:
            # list is not a list, but None
            # and None does not have remove()
            pass    

        return super(Thread, self).delete(*args, **kwargs)

    def inc_views(self):
        self.views = self.views + 1
        self.save()

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



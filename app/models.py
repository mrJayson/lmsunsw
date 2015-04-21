"""
Definition of models.
"""

import string

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from autoslug import AutoSlugField

from wordcloud import WordCloud


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

class Lecture(models.Model):
    lecture_name = models.CharField(max_length=30, unique=True)
    lecture_slide = models.URLField(blank=True, null=True, help_text=_("Optional, Provide a URL link to the lecture slides to be displayed"))
    collab_doc = models.URLField(blank=True, null=True, help_text=_("Optional, Provide a URL Link to a specific google docs, a blank default will be used if empty"))
    slug = AutoSlugField(populate_from='lecture_name')

    @property
    def get_absolute_url(self):
        return _("%(id)s/%(slug)s") % {'id':self.id, 'slug':self.slug}

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
        return _("")

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
    anonymous = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.title)

    @property
    def replies(self):
        replies = len(Post.objects.filter(Thread=self.id))
        return replies

    def inc_views(self):
        self.views = self.views + 1
        self.save()

    @property
    def Creator_name(self):
        return _("anonymous") if self.anonymous else self.Creator

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
        return _("anonymous") if self.anonymous else self.Creator

class Wordcloud(models.Model):
    title = models.CharField(max_length=30, unique=True)
    image = models.ImageField(upload_to="wordcloud", blank=True, null=True)
    Lecture = models.ForeignKey(Lecture)
    visible = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.title)

    @property
    def words(self):
        # joins all the words into one string with space as separator
        return " ".join([word.word for word in WordcloudSubmission.objects.filter(Wordcloud=self)])

    def generate_image(self):
        # returns whether or not it generated an image
        if self.words != '':
            wc = WordCloud(font_path="static/app/fonts/Microsoft Sans Serif.ttf", width=800, height=400).generate(self.words)
            filepath = "wordcloud/"+ self.title +".png"
            img = wc.to_image()
            img.save(settings.MEDIA_ROOT + "/" + filepath, 'PNG') # create the image file on filesystem
            self.image = filepath # add the image to the model
            self.save()
            return True
        return False

class WordcloudSubmission(models.Model):
    User = models.ForeignKey(User)
    Wordcloud = models.ForeignKey(Wordcloud)
    word = models.CharField(max_length=30)

    class Meta:
        unique_together = ('User', 'Wordcloud') 

class CodeSnippet(models.Model):
    syntax = models.CharField(max_length=30, choices=settings.LANGUAGE_CHOICES, default=settings.DEFAULT_LANGUAGE)
    code = models.TextField()
    linenumbers = models.BooleanField(default=settings.DEFAULT_LINE_NUMBERS)
    style = models.CharField(max_length=30, choices=tuple(STYLE_MAP.items()), default='default')

    class Meta:
        verbose_name = _('Code snippet')
        verbose_name_plural = _('Code snippets')

    def __str__(self):
        return Truncator(self.code).words(20)

    @property
    def render_code(self):
        style = styles.get_style_by_name(self.style)
        formatter = HtmlFormatter(linenos=self.linenumbers, style=style, nowrap=True, classprefix='code%s-' % self.pk)
        html = highlight(self.code, get_lexer_by_name(self.syntax), formatter)
        css = formatter.get_style_defs()

        # Included in a DIV, so the next item will be displayed below.
        return _('<div class="code"><style type="text/css">%(css)s</style>\n<pre>%(html)s</pre></div>\n') % {'css':css, 'html':html}



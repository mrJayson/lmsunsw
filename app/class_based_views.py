"""
Definition of class-based-views.
"""

from django.views.generic import TemplateView, View, CreateView, FormView, ListView
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from app.mixins import BaseSidebarContextMixin, SidebarContextMixin
from app.forms import QuizSelectionForm, CreateThreadForm, CreateUserForm, PostReplyForm, WordcloudSubmissionForm
from app.models import *

class IndexView(TemplateView, BaseSidebarContextMixin):
    template_name = _('app/index.html')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser and request.path == u'/':
            return redirect('admin:index')
        else:
            # student index is empty, redirect to latest lecture page 
            lecture = Lecture.objects.last()
            if lecture == None:
                # only display index page if in the event there are no lectures to display
                return super(IndexView, self).dispatch(request, *args, **kwargs)
            else:
                return redirect(reverse('lecture', kwargs={'lecture_id': lecture.id, 'url_slug': lecture.slug}))
        
    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        context['lecture_list'] = Lecture.objects.all()
        if context.has_key('session_key'):
            context['session_key'] = self.request.session.session_key
        return context


class CreateUser(CreateView):
    template_name = _('app/create_user.html')
    form_class = CreateUserForm

    def get_success_url(self):
        return reverse('alert', kwargs={'tag':'create_user_success'})


class LectureView(TemplateView, SidebarContextMixin):
    template_name = _('app/lecture.html')


class QuizView(FormView, SidebarContextMixin):
    template_name = _('app/quiz.html')
    #form_class = QuizSelectionForm
    #queryset = QuizChoice.objects.filter(Quiz = self.kwargs(quiz_id))

    def get_form(self, data=None, files=None, *args, **kwargs):
        user = self.request.user
        quiz = Quiz.objects.get(id=self.kwargs.get('quiz_id'))

        if self.request.method == "POST":
            form = QuizSelectionForm(user, quiz, data=self.request.POST)
        else: # mainly for GET requests
            form = QuizSelectionForm(user, quiz)

        return form

    def form_valid(self, form):
        if form.is_valid():
            form.save()
        return super(QuizView, self).form_valid(form)

    def get_success_url(self):
        lecture_id = self.kwargs.get('lecture_id')
        quiz_id = self.kwargs.get('quiz_id')
        lecture = Lecture.objects.get(id=self.kwargs.get('lecture_id'))
        quiz = Quiz.objects.get(id=self.kwargs.get('quiz_id'))

        
        return reverse('quiz', kwargs={'lecture_id':lecture.id, 'url_slug':lecture.slug, 'quiz_id':quiz.id, 'quiz_slug':quiz.question})

class LectureSlideView(TemplateView, SidebarContextMixin):
    template_name = _('app/lecture_slide.html')


class ThreadView(ListView, BaseSidebarContextMixin):
    # view for all threads in a lecture
    template_name = _('app/thread.html')
    model = Thread

    def get_context_data(self, *args, **kwargs):
        context = super(ThreadView, self).get_context_data(*args, **kwargs)
        context['lecture_list'] = Lecture.objects.all()
        return context

    def get_queryset(self, *args, **kwargs):
        return Thread.objects.all()

class CreateThreadView(CreateView, BaseSidebarContextMixin):
    template_name = _('app/create_thread.html')
    model = Thread

    def get_context_data(self, *args, **kwargs):
        context = super(CreateThreadView, self).get_context_data(*args, **kwargs)
        context['lecture_list'] = Lecture.objects.all()
        return context

    def get_form(self, data=None, files=None, *args, **kwargs):
        user = self.request.user
        if self.request.method == "POST":
            form = CreateThreadForm(user=user, data=self.request.POST)
        else: # mainly for GET requests
            form = CreateThreadForm(user=user)
        return form

    def get_success_url(self):
        return reverse('thread')

class PostView(CreateView, BaseSidebarContextMixin):
    # create view since priority is the posts reply form
    template_name = _('app/post.html')
    model = Post

    def dispatch(self, request, *args, **kwargs):
        thread = Thread.objects.get(id=kwargs.get('thread_id'))
        thread.inc_views()
        return super(PostView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(PostView, self).get_context_data(*args, **kwargs)
        context['lecture_list'] = Lecture.objects.all()
        context['thread'] = Thread.objects.get(id=self.kwargs.get('thread_id'))
        context['posts'] = Post.objects.filter(Thread = self.kwargs.get('thread_id'))
        return context

    def get_form(self, data=None, files=None, *args, **kwargs):
        user = self.request.user
        thread = Thread.objects.get(id=self.kwargs.get('thread_id'))
        if self.request.method == "POST":
            form = PostReplyForm(user=user, thread=thread, data=self.request.POST)
        else: # for GET requests
            form = PostReplyForm(user=user, thread=thread)
        return form

    def get_success_url(self):
        return reverse('post', kwargs={'thread_id':self.kwargs.get('thread_id'), 'thread_slug':self.kwargs.get('thread_slug')})

class WordcloudSubmissionView(CreateView, SidebarContextMixin):
    # view for students to submit word to wordcloud
    template_name = _('app/wordcloud_submission.html')
    model = WordcloudSubmission

    def get_context_data(self, *args, **kwargs):
        context = super(WordcloudSubmissionView, self).get_context_data(*args, **kwargs)
        context['lecture_list'] = Lecture.objects.all()
        context['wordcloud'] = Wordcloud.objects.get(id=self.kwargs.get('wordcloud_id'))
        return context

    def get_form(self, data=None, files=None, *args, **kwargs):
        user = self.request.user
        wordcloud = Wordcloud.objects.get(id=self.kwargs.get('wordcloud_id'))
        if self.request.method == "POST":
            form = WordcloudSubmissionForm(user=user, wordcloud=wordcloud, data=self.request.POST)
        else: # mainly for GET requests
            form = WordcloudSubmissionForm(user=user, wordcloud=wordcloud)
        return form

    def get_success_url(self):
        return reverse('wordcloud', kwargs={'lecture_id':self.kwargs.get('lecture_id'), 'url_slug':self.kwargs.get('url_slug'), 'wordcloud_id':self.kwargs.get('wordcloud_id'), 'wordcloud_slug':self.kwargs.get('wordcloud_slug')})

class CodeSnippetView(ListView, SidebarContextMixin):
    template_name = _('app/code_snippet.html')
    model = CodeSnippet

    #def get_queryset(self, *args, **kwargs):

















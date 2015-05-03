"""
Definition of class-based-views.
"""

from django.views.generic import TemplateView, View, CreateView, FormView, ListView
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from app.mixins import BaseSidebarContextMixin, SidebarContextMixin
from app.forms import QuizSelectionForm, CreateThreadForm, CreateUserForm, PostReplyForm
from app.models import *
from app.cache_helpers import *

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
                return redirect(reverse('lecture', kwargs={'lecture_id': lecture.id, 'lecture_slug': lecture.slug}))
        
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

    def get_context_data(self, *args, **kwargs):
        context = super(QuizView, self).get_context_data(*args, **kwargs)
        context['code_snippet'] = Quiz.objects.get(id=self.kwargs.get('quiz_id')).render_code
        return context

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

        
        return reverse('quiz', kwargs={'lecture_id':lecture.id, 'lecture_slug':lecture.slug, 'quiz_id':quiz.id, 'quiz_slug':quiz.question})

class LectureSlideView(TemplateView, SidebarContextMixin):
    template_name = _('app/lecture_slide.html')


class ThreadView(ListView, BaseSidebarContextMixin):
    # view for all threads in a lecture
    template_name = _('app/thread.html')
    model = Thread


    def get_queryset(self, *args, **kwargs):
        thread_list = get_thread_list()

        return thread_list

class CreateThreadView(CreateView, BaseSidebarContextMixin):
    template_name = _('app/create_thread.html')
    model = Thread

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

    @staticmethod
    def get_thread_from_id(id):
        thread_list = cache.get('thread_list')
        if thread_list == None:
            thread_list = Thread.objects.all()
            cache.set('thread_list', thread_list, settings.THREAD_LIST_CACHE_INTERVAL)

        thread = thread_list.get(id=id)
        return thread

    def dispatch(self, request, *args, **kwargs):

        PostView.get_thread_from_id(kwargs.get('thread_id')).inc_views()
        return super(PostView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(PostView, self).get_context_data(*args, **kwargs)

        thread = PostView.get_thread_from_id(self.kwargs.get('thread_id'))
        context['thread'] = thread

        context['posts'] = Post.objects.select_related().filter(Thread = thread)
        return context

    def get_form(self, data=None, files=None, *args, **kwargs):
        user = self.request.user
        thread = PostView.get_thread_from_id(self.kwargs.get('thread_id'))
        if self.request.method == "POST":
            form = PostReplyForm(user=user, thread=thread, data=self.request.POST)
        else: # for GET requests
            form = PostReplyForm(user=user, thread=thread)
        return form

    def get_success_url(self):
        return reverse('post', kwargs={'thread_id':self.kwargs.get('thread_id'), 'thread_slug':self.kwargs.get('thread_slug')})


class CodeSnippetView(ListView, SidebarContextMixin):
    template_name = _('app/code_snippet.html')
    model = CodeSnippet

    #def get_queryset(self, *args, **kwargs):

















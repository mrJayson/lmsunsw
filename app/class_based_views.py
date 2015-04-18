from django.views.generic import TemplateView, View, CreateView, FormView, ListView
from django.shortcuts import render, redirect
from django.template import RequestContext
from app.models import *
from django.contrib.auth.models import User
from app.forms import QuizSelectionForm, CreateThreadForm, CreateUserForm, PostReplyForm, WordcloudSubmissionForm
from django.core.urlresolvers import reverse
from app.mixins import BaseSidebarContextMixin, SidebarContextMixin

class IndexView(TemplateView, BaseSidebarContextMixin):
    template_name = 'app/index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser and request.path == u'/':
            print request.path
            return redirect('admin:index')
        else:
            return super(IndexView, self).dispatch(request, *args, **kwargs)

        
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['lecture_list'] = Lecture.objects.all()
        context['session_key'] = self.request.session.session_key
        return context


class LectureView(TemplateView, SidebarContextMixin):
    template_name = 'app/lecture.html'



class CreateUser(CreateView):
    template_name = 'app/create_user.html'
    form_class = CreateUserForm

    def get_success_url(self):
        return reverse('alert', kwargs={'tag':'create_user_success'})

class QuizView(FormView, SidebarContextMixin):
    template_name = 'app/quiz.html'
    #form_class = QuizSelectionForm
    #queryset = QuizChoice.objects.filter(Quiz = self.kwargs(quiz_id))

    def get_form(self, data=None, files=None, **kwargs):
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
        lect_id = self.kwargs.get('lect_id')
        quiz_id = self.kwargs.get('quiz_id')
        lecture = Lecture.objects.get(id=self.kwargs.get('lect_id'))
        quiz = Quiz.objects.get(id=self.kwargs.get('quiz_id'))

        
        return reverse('quiz', kwargs={'lect_id':lecture.id, 'url_slug':lecture.slug, 'quiz_id':quiz.id, 'quiz_slug':quiz.question})

class LectureSlideView(TemplateView, SidebarContextMixin):
    template_name = 'app/lecture_slide.html'


class ThreadView(ListView, BaseSidebarContextMixin):
    # view for all threads in a lecture
    template_name = 'app/thread.html'
    model = Thread

    def get_context_data(self, **kwargs):
        context = super(ThreadView, self).get_context_data(**kwargs)
        context['lecture_list'] = Lecture.objects.all()
        return context

    def get_queryset(self, *args, **kwargs):
        return Thread.objects.all()

class CreateThreadView(CreateView, BaseSidebarContextMixin):
    template_name = 'app/create_thread.html'
    model = Thread

    def get_context_data(self, **kwargs):
        context = super(CreateThreadView, self).get_context_data(**kwargs)
        context['lecture_list'] = Lecture.objects.all()
        return context

    def get_form(self, data=None, files=None, **kwargs):
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
    template_name = 'app/post.html'
    model = Post

    def dispatch(self, request, *args, **kwargs):
        thread = Thread.objects.get(id=kwargs.get('thread_id'))
        thread.inc_views()
        return super(PostView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        context['lecture_list'] = Lecture.objects.all()
        context['thread'] = Thread.objects.get(id=self.kwargs.get('thread_id'))
        context['posts'] = Post.objects.filter(Thread = self.kwargs.get('thread_id'))
        return context

    def get_form(self, data=None, files=None, **kwargs):
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
    template_name = 'app/wordcloud_submission.html'
    model = WordcloudSubmission

    def get_context_data(self, **kwargs):
        context = super(WordcloudSubmissionView, self).get_context_data(**kwargs)
        context['lecture_list'] = Lecture.objects.all()
        context['wordcloud'] = Wordcloud.objects.get(id=self.kwargs.get('wordcloud_id'))
        return context

    def get_form(self, data=None, files=None, **kwargs):
        user = self.request.user
        wordcloud = Wordcloud.objects.get(id=self.kwargs.get('wordcloud_id'))
        if self.request.method == "POST":
            print "POST"
            form = WordcloudSubmissionForm(user=user, wordcloud=wordcloud, data=self.request.POST)
        else: # mainly for GET requests
            form = WordcloudSubmissionForm(user=user, wordcloud=wordcloud)
        return form

    def get_success_url(self):
        return reverse('wordcloud', kwargs={'lect_id':self.kwargs.get('lect_id'), 'url_slug':self.kwargs.get('url_slug'), 'wordcloud_id':self.kwargs.get('wordcloud_id'), 'wordcloud_slug':self.kwargs.get('wordcloud_slug')})
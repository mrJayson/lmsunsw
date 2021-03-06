"""
Definition of class-based-views.
"""

from django.views.generic import TemplateView, View, CreateView, FormView, ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from app.mixins import BaseSidebarContextMixin, SidebarContextMixin
from app.forms import QuizSelectionForm, CreateThreadForm, CreateUserForm, PostReplyForm, ChangeCollabDocForm
from app.models import *
from app.cache_helpers import *

class IndexView(TemplateView):
    template_name = _('app/index.html')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser and request.path == u'/':
            return redirect('admin:index')
        else:
            # student index is empty, redirect to latest lecture page 
            lecture = get_last_lecture_object()
            if lecture == None:
                # only display index page if in the event there are no lectures to display
                return super(IndexView, self).dispatch(request, *args, **kwargs)
            else:
                return redirect(reverse('lecture', kwargs={'lecture_id': lecture.id, 'lecture_slug': lecture.slug}))
        
    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        context['lecture_list'] = get_lecture_list()
        if context.has_key('session_key'):
            context['session_key'] = self.request.session.session_key
        return context


class CreateUser(CreateView):
    template_name = _('app/create_user.html')
    form_class = CreateUserForm

    def get_success_url(self):
        return reverse('login_')


class LectureView(TemplateView, SidebarContextMixin):
    template_name = _('app/lecture.html')

    def get_context_data(self, *args, **kwargs):
        context = super(LectureView, self).get_context_data(*args, **kwargs)


        return context


class QuizView(FormView, SidebarContextMixin):
    template_name = _('app/quiz.html')

    def get_context_data(self, *args, **kwargs):
        context = super(QuizView, self).get_context_data(*args, **kwargs)
        quiz = get_quiz_object(id=self.kwargs.get('quiz_id'))
        context['code_snippet'] = quiz.render_code
        return context


    def get_form(self, data=None, files=None, *args, **kwargs):
        user = self.request.user
        quiz = get_quiz_object(id=self.kwargs.get('quiz_id'))

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
        lecture = get_lecture_object(id=self.kwargs['lecture_id'])
        quiz = get_quiz_object(id=self.kwargs.get('quiz_id'))

        
        return reverse('quiz', kwargs={'lecture_id':lecture.id, 'lecture_slug':lecture.slug, 'quiz_id':quiz.id, 'quiz_slug':quiz.question})

class LectureSlideView(TemplateView, SidebarContextMixin):
    template_name = _('app/lecture_slide.html')

    def get_context_data(self, *args, **kwargs):
        context = super(LectureSlideView, self).get_context_data(*args, **kwargs)
        Lecture = get_lecture_object(id=self.kwargs['lecture_id'])
        context['lecture_slide_list'] = filter_lecture_materials_list(Lecture=Lecture)
        return context


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

    def dispatch(self, request, *args, **kwargs):
        get_thread_object(id=kwargs.get('thread_id')).inc_views()
        return super(PostView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(PostView, self).get_context_data(*args, **kwargs)

        thread = get_thread_object(id=self.kwargs.get('thread_id'))
        context['thread'] = thread
        context['posts'] = filter_post_list(Thread = thread)
        return context

    def get_form(self, data=None, files=None, *args, **kwargs):
        user = self.request.user
        thread = get_thread_object(id=self.kwargs.get('thread_id'))
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

class AdminQuizResultsView(ListView):
    template_name = _('admin/quiz_results.html')
    model = Quiz

    def get_queryset(self, *args, **kwargs):
        return get_quiz_list()

class AdminQuizResultsDetailView(TemplateView):
    template_name = _('admin/quiz_results_detail.html')

    def get_context_data(self, *args, **kwargs):
        context = super(AdminQuizResultsDetailView, self).get_context_data(*args, **kwargs)
        quiz = get_quiz_object(id=kwargs.get('quiz_id'))
        context['quiz'] = quiz
        context['code_snippet'] = quiz.render_code
        quiz_type = quiz.quiz_type
        if quiz_type == QuizType.FREEFORM:
            answers = QuizChoiceSelected.objects.select_related().filter(Quiz=quiz)
            context['answers'] = answers
            context['submission_count'] = answers.count()
        else:
            quizchoices = filter_quizchoice_list(Quiz=quiz)
            context['quizchoices'] = quizchoices
            context['quiz_choices_summary'] = []
            context['quiz_choices_summary_max_value'] = 0
            for qc in quizchoices:
                context['quiz_choices_summary'].append({'choice':qc.choice, 'times_chosen':qc.times_chosen})
                context['quiz_choices_summary_max_value'] = max(context['quiz_choices_summary_max_value'], qc.times_chosen)
            for qc in context['quiz_choices_summary']:
                try:
                    qc['relative_percentage'] = (qc['times_chosen'] * 100/context['quiz_choices_summary_max_value'])
                except ZeroDivisionError:
                    # in the event that there are no submissions, exception will occur
                    qc['relative_percentage'] = 0
            quizchoiceselecteds = QuizChoiceSelected.objects.select_related().filter(QuizChoice__Quiz=quiz.id)
            context['quizchoiceselecteds'] = quizchoiceselecteds
            context['submission_count'] = len(quizchoiceselecteds)
        return context
















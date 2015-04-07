from django.views.generic import TemplateView, View, CreateView, FormView
from django.shortcuts import render
from django.template import RequestContext
from app.models import *
from app.forms import CreateUserForm
from django.contrib.auth.models import User
from app.forms import QuizSelectionForm
from django.core.urlresolvers import reverse


class IndexView(TemplateView):
    template_name = 'app/index.html'
        
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['lecture_list'] = Lecture.objects.all()
        context['session_key'] = self.request.session.session_key

        return context


class LectureView(TemplateView):
    template_name = 'app/lecture.html'

    def get_context_data(self, **kwargs):
        context = super(LectureView, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs['url_slug']

        #need to pass identity of current lecture into template
        context['current_lecture'] = Lecture.objects.get(id=self.kwargs['lect_id'])

        #used on the sidebar to display tabs

        context['lecture_list'] = Lecture.objects.all()
        context['quiz_list'] = Quiz.objects.filter(Lecture = self.kwargs['lect_id'], visible = True)
        
        return context

class CreateUser(CreateView):
    template_name = 'app/create_user.html'
    form_class = CreateUserForm

    def get_success_url(self):
        return reverse('alert', kwargs={'tag':'create_user_success'})

class QuizView(FormView):
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

    def get_context_data(self, **kwargs):
        context = super(QuizView, self).get_context_data(**kwargs)
        context['lecture_list'] = Lecture.objects.all()
        context['quiz_list'] = Quiz.objects.filter(Lecture = self.kwargs['lect_id'], visible = True)
        return context

    def form_valid(self, form):
        print "FORM_VALID"
        if form.is_valid():
            form.save()
        return super(QuizView, self).form_valid(form)

    def get_success_url(self):
        lect_id = self.kwargs.get('lect_id')
        quiz_id = self.kwargs.get('quiz_id')
        lecture = Lecture.objects.get(id=self.kwargs.get('lect_id'))
        quiz = Quiz.objects.get(id=self.kwargs.get('quiz_id'))

        
        return reverse('quiz', kwargs={'lect_id':lecture.id, 'url_slug':lecture.get_slug_field, 'quiz_id':quiz.id, 'quiz_slug':quiz.question})

class LectureSlideView(LectureView):
    template_name = 'app/lecture_slide.html'

    def get_context_data(self, **kwargs):
        context = super(LectureSlideView, self).get_context_data(**kwargs)
        # inherit all the same contexts used in LectureView

        return context

class ThreadView(LectureView):
    # view for all threads in a lecture
    template_name = 'app/thread.html'

    def get_context_data(self, **kwargs):
        context = super(ThreadView, self).get_context_data(**kwargs)
        # inherit all the same contexts used in LectureView

        return context

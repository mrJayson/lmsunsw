from django.views.generic import TemplateView, ListView, FormView, View
from django.shortcuts import render
from django.template import RequestContext
from app.models import *
from app.forms import QuizSelectionForm


class IndexView(TemplateView):
    template_name = 'app/index.html'
        
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['sidebar'] = Lecture.objects.all()

        return context

class LectureView(TemplateView):
    template_name = 'app/lecture.html'

    def get_context_data(self, **kwargs):
        context = super(LectureView, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs['url_slug']
        lecture_id = self.kwargs['lect_id']
        context['sidebar'] = Quiz.objects.filter(Lecture = lecture_id, visible = True)
        
        
        return context

class QuizView(FormView):
    template_name = 'app/quiz.html'
    #form_class = QuizSelectionForm
    #queryset = QuizChoice.objects.filter(Quiz = self.kwargs(quiz_id))

    def get_form(self, data=None, files=None, **kwargs):

        user = self.request.user
        quiz_id = self.kwargs.get('quiz_id')
        print user.first_name
        print quiz_id
        form = QuizSelectionForm(user, quiz_id)
        return form

    def get_context_data(self, **kwargs):
        context = super(QuizView, self).get_context_data(**kwargs)
        context['quizchoices'] = self.get_queryset()
        return context

    def get_queryset(self):
        quiz_id = self.kwargs.get('quiz_id')
        qs = QuizChoice.objects.filter(Quiz = quiz_id)
        return qs

    def form_valid(self, form):

        return super(QuizView, self).form_valid(form)
from django.views.generic import TemplateView, ListView, FormView, View
from django.shortcuts import render
from django.template import RequestContext
from app.models import *
from app.forms import QuizSelectionForm
from django.core.urlresolvers import reverse



class IndexView(TemplateView):
    template_name = 'app/index.html'
        
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['lecture_list'] = Lecture.objects.all()

        return context


class LectureView(TemplateView):
    template_name = 'app/lecture.html'

    def get_context_data(self, **kwargs):
        context = super(LectureView, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs['url_slug']
        #lecture_id = self.kwargs['lect_id']
        context['lecture_list'] = Lecture.objects.all()
        context['quiz_list'] = Quiz.objects.filter(Lecture = self.kwargs['lect_id'], visible = True)
        context['lect'] = Lecture.objects.get(id=self.kwargs['lect_id'])
        
        return context

class QuizView(FormView):
    template_name = 'app/quiz.html'
    #form_class = QuizSelectionForm
    #queryset = QuizChoice.objects.filter(Quiz = self.kwargs(quiz_id))

    def get_form(self, data=None, files=None, **kwargs):
        print "get_form"
        user = self.request.user
        quiz_id = self.kwargs.get('quiz_id')

        if self.request.method == "POST":
            form = QuizSelectionForm(user, quiz_id, data=self.request.POST)
        else: # mainly for GET requests
            form = QuizSelectionForm(user, quiz_id)

        return form

    def get_context_data(self, **kwargs):
        context = super(QuizView, self).get_context_data(**kwargs)
        context['lecture_list'] = Lecture.objects.all()
        context['quiz_list'] = Quiz.objects.filter(Lecture = self.kwargs['lect_id'], visible = True)
        return context

    '''def get_queryset(self):
        print "get_queryset"
        quiz_id = self.kwargs.get('quiz_id')
        qs = QuizChoice.objects.filter(Quiz = quiz_id)
        return qs'''

    def form_valid(self, form):
        print "form_valid"
        print form.data
        if form.is_valid():
            form.save()
        else:
            print "FAILED"
        return super(QuizView, self).form_valid(form)

    def get_success_url(self):
        print "get_success_url"
        lect_id = self.kwargs.get('lect_id')
        quiz_id = self.kwargs.get('quiz_id')
        lecture = Lecture.objects.get(id=self.kwargs.get('lect_id'))
        quiz = Quiz.objects.get(id=self.kwargs.get('quiz_id'))

        
        return reverse('quiz', kwargs={'lect_id':lecture.id, 'url_slug':lecture.get_slug_field, 'quiz_id':quiz.id, 'quiz_slug':quiz.question})
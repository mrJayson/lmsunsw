
from django.views.generic import View, CreateView, FormView
from app.forms import CreateUserForm
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.models import User
from app.forms import QuizSelectionForm
from django.core.urlresolvers import reverse
from app.models import Lecture, Quiz

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

    def form_valid(self, form):
        if form.is_valid():
            form.save()
        return super(QuizView, self).form_valid(form)

    def get_success_url(self):
        lect_id = self.kwargs.get('lect_id')
        quiz_id = self.kwargs.get('quiz_id')
        lecture = Lecture.objects.get(id=self.kwargs.get('lect_id'))
        quiz = Quiz.objects.get(id=self.kwargs.get('quiz_id'))

        
        return reverse('quiz', kwargs={'lect_id':lecture.id, 'url_slug':lecture.get_slug_field, 'quiz_id':quiz.id, 'quiz_slug':quiz.question})
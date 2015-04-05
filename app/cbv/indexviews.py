from django.views.generic import TemplateView, View
from django.shortcuts import render
from django.template import RequestContext
from app.models import *




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

class LectureSlideView(TemplateView):
    template_name = 'app/lecture_slide.html'

    def get_context_data(self, **kwargs):
        context = super(LectureSlideView, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs['url_slug']

        #need to pass identity of current lecture into template
        context['current_lecture'] = Lecture.objects.get(id=self.kwargs['lect_id'])

        #used on the sidebar to display tabs

        context['lecture_list'] = Lecture.objects.all()
        context['quiz_list'] = Quiz.objects.filter(Lecture = self.kwargs['lect_id'], visible = True)
        return context


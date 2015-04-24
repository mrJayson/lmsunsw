"""
Definition of custom mixins.
"""

from django.views.generic.base import ContextMixin
from django.contrib import admin

from app.models import Lecture, Quiz, QuizChoiceSelected, CodeSnippet, Wordcloud, WordcloudSubmission

class BaseSidebarContextMixin(ContextMixin):
	def get_context_data(self, *args, **kwargs):
		context = super(BaseSidebarContextMixin, self).get_context_data(*args, **kwargs)
		context['lecture_list'] = Lecture.objects.all()
		return context

class SidebarContextMixin(BaseSidebarContextMixin):

	def get_context_data(self, *args, **kwargs):
		context = super(SidebarContextMixin, self).get_context_data(*args, **kwargs)
		context['slug'] = self.kwargs['url_slug']

		#need to pass identity of current lecture into template
		context['current_lecture'] = Lecture.objects.get(id=self.kwargs['lect_id'])

		#used on the sidebar to display tabs

		context['quiz_list'] = Quiz.objects.filter(Lecture = self.kwargs['lect_id'], visible = False).filter(
			Lecture__in=list(set([k.Lecture for k in [j.Quiz for j in [i.QuizChoice for i in QuizChoiceSelected.objects.select_related().all()]]])))
		context['wordcloud_list'] = Wordcloud.objects.filter(Lecture=self.kwargs['lect_id'], visible=False).filter(
			id__in=list(set([i.Wordcloud.id for i in WordcloudSubmission.objects.all()])))
		context['codesnippet_list'] = CodeSnippet.objects.filter(Lecture=self.kwargs['lect_id'])
		return context


"""
Definition of custom mixins.
"""

from django.views.generic.base import ContextMixin
from django.contrib import admin
from django.core.cache import cache

from app.models import Lecture, Quiz, QuizChoiceSelected, CodeSnippet
from app.cache_helpers import *
from app.forms import ConfidenceMessageForm

class BaseSidebarContextMixin(ContextMixin):

	# basic sidebar contexts

	def get_context_data(self, *args, **kwargs):
		context = super(BaseSidebarContextMixin, self).get_context_data(*args, **kwargs)
		context['lecture_list'] = get_lecture_list()
		context['confidence_message_form'] = ConfidenceMessageForm(path=self.request.path,instance=self.request.user.UserProfile)
		return context

class SidebarContextMixin(BaseSidebarContextMixin):
	# provides context for the top nav bar
	# more specific sidebar contexts

	def get_context_data(self, *args, **kwargs):
		context = super(SidebarContextMixin, self).get_context_data(*args, **kwargs)
		context['slug'] = self.kwargs['lecture_slug']

		#need to pass identity of current lecture into template

		context['current_lecture'] = get_lecture_object(id=self.kwargs['lecture_id'])

		#used on the navbar to display tabs

		context['codesnippet_list'] = filter_codesnippet_list(Lecture=context['current_lecture'])
		context['lecture_slide_exists'] = filter_lecture_materials_list(Lecture=context['current_lecture']) != []
		return context
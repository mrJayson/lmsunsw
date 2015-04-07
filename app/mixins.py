
from django.views.generic.base import ContextMixin

from app.models import Lecture, Quiz

class SidebarContextMixin(ContextMixin):

	def get_context_data(self, **kwargs):
		context = super(SidebarContextMixin, self).get_context_data(**kwargs)
		context['slug'] = self.kwargs['url_slug']

		#need to pass identity of current lecture into template
		context['current_lecture'] = Lecture.objects.get(id=self.kwargs['lect_id'])

		#used on the sidebar to display tabs

		context['lecture_list'] = Lecture.objects.all()
		context['quiz_list'] = Quiz.objects.filter(Lecture = self.kwargs['lect_id'], visible = True)
		return context
from django.views.generic.base import ContextMixin
from django.contrib import admin

from app.models import Lecture, Quiz, QuizChoiceSelected

class SidebarContextMixin(ContextMixin):

	def get_context_data(self, **kwargs):
		context = super(SidebarContextMixin, self).get_context_data(**kwargs)
		context['slug'] = self.kwargs['url_slug']

		#need to pass identity of current lecture into template
		context['current_lecture'] = Lecture.objects.get(id=self.kwargs['lect_id'])

		#used on the sidebar to display tabs

		context['lecture_list'] = Lecture.objects.all()
		context['quiz_list'] = Quiz.objects.filter(Lecture = self.kwargs['lect_id'], visible = False).filter(
			Lecture__in=list(set([k.Lecture for k in [j.Quiz for j in [i.QuizChoice for i in QuizChoiceSelected.objects.select_related().all()]]])))
		return context

###################################################################################################

# Mixin for limited admin site

class LimitedModelAdminMixin(admin.ModelAdmin):

	def add_view(self, request, form_url='', extra_context=None):
		extra_context = extra_context or {}
		extra_context['lecture_list'] = Lecture.objects.all()
		return super(LimitedModelAdminMixin, self).add_view(request, form_url, extra_context)

	def change_view(self, request, object_id, form_url='', extra_context=None):
		extra_context = extra_context or {}
		extra_context['lecture_list'] = Lecture.objects.all()
		return super(LimitedModelAdminMixin, self).change_view(request, object_id, form_url, extra_context)

	def delete_view(self, request, object_id, extra_context=None):
		extra_context = extra_context or {}
		extra_context['lecture_list'] = Lecture.objects.all()
		return super(LimitedModelAdminMixin, self).delete_view(request, object_id, extra_context)

	def changelist_view(self, request, extra_context=None):
		extra_context = extra_context or {}
		extra_context['lecture_list'] = Lecture.objects.all()
		return super(LimitedModelAdminMixin, self).changelist_view(request=request, extra_context=extra_context)

###################################################################################################

# Mixin for default admin site

class ModelAdminMixin(admin.ModelAdmin):

	def add_view(self, request, form_url='', extra_context=None, admin_site=None):
		extra_context = extra_context or {}
		if admin_site:
		    extra_context['app_list'] = admin_site.app_list(request)
		return super(ModelAdminMixin, self).add_view(request, form_url, extra_context)

	def change_view(self, request, object_id, form_url='', extra_context=None, admin_site=None):
		extra_context = extra_context or {}
		if admin_site:
		    extra_context['app_list'] = admin_site.app_list(request)
		return super(ModelAdminMixin, self).change_view(request, object_id, form_url, extra_context)

	def delete_view(self, request, object_id, extra_context=None, admin_site=None):
		extra_context = extra_context or {}
		if admin_site:
		    extra_context['app_list'] = admin_site.app_list(request)
		return super(ModelAdminMixin, self).delete_view(request, object_id, extra_context)

	def changelist_view(self, request, extra_context=None, admin_site=None):
		extra_context = extra_context or {}
		if admin_site:
		    extra_context['app_list'] = admin_site.app_list(request)
		return super(ModelAdminMixin, self).changelist_view(request=request, extra_context=extra_context)
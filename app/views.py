"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.http import Http404  

from django.views.generic import TemplateView

'''generic view for displaying single messages to the user'''
class AlertView(TemplateView):
    template_name = "alert.html"

    def get_context_data(self, **kwargs):
        context = super(AlertView, self).get_context_data(**kwargs)
        tag = self.kwargs['tag']
        '''message to display is based on the url slug'''
        if tag == "create_user_success":
            context['msg'] = "Account successfully created!\nPlease log in now"
        else:
            raise Http404
        return context
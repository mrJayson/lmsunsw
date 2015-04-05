"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from datetime import datetime
from django.http import Http404  

from django.views.generic import TemplateView, View
import json
from app.models import ConfidenceMeter


'''generic view for displaying single messages to the user'''
class AlertView(TemplateView):
    template_name = "app/alert.html"

    def get_context_data(self, **kwargs):
        context = super(AlertView, self).get_context_data(**kwargs)
        tag = self.kwargs['tag']
        '''message to display is based on the url slug'''
        if tag == "create_user_success":
            context['msg'] = "Account successfully created!\nPlease log in now"
        else:
            raise Http404
        return context

def vote(request):
    # voting for the confusion meter
    if request.is_ajax():
        user = request.user
        vote = request.GET.get("vote")
        # update model
        confidence_object, created = ConfidenceMeter.objects.get_or_create(User=user)
        if vote == "up":
            confidence = True
        else:
            confidence = False
        ConfidenceMeter.confidence = confidence

        #once updated, return results back for html update
        results = {'confidence': confidence}
        confidence_object.save()
        return HttpResponse(json.dumps(results), content_type='application/json')

    else:
        #if not ajax request, render index page as they are not supposed to request via non ajax
        raise Http404
        pass
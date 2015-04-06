"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from datetime import datetime
from django.http import Http404 
from django.contrib.auth import views

from django.views.generic import TemplateView, View
import json
from app.models import ConfidenceMeter
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.sessions.models import Session



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

def logout(request, next_page=None,
           template_name='registration/logged_out.html',
           redirect_field_name=REDIRECT_FIELD_NAME,
           current_app=None, extra_context=None):
    #record user id before logout wipes it
    user_id = request.user.id
    # perform normal logout operation
    ret_val = views.logout(request, next_page, template_name, redirect_field_name, current_app, extra_context)
    #remove session entry from db to maintain correct number of session entries since django only clears the contents not the entry
    Session.objects.all().get(session_key=request.session.session_key).delete()
    for session in Session.objects.all():
        if session.get_decoded().get('_auth_user_id') == user_id:
            # sometimes there are multiple sessions for the same user, delete those sessions as well
            session.delete()
    return ret_val

def get_confidence_meter_values():
    # context processor for retreiving data for confidence meter
    print "context_processor"
    
    return ret_val

def vote(request):
    # voting for the confusion meter
    if request.is_ajax():
        user = request.user
        vote = request.GET.get("vote")
        # update model
        confidence_object, created = ConfidenceMeter.objects.get_or_create(User=user)
        if vote == u'1':
            confidence = 1
        elif vote == u'-1':
            confidence = -1
        else:
            #all else is neutral
            confidence = 0

        confidence_object.confidence = confidence

        confidence_object.save()

        print "context_processor"
        good = 0
        neutral = 0
        bad = 0
        for vote in ConfidenceMeter.objects.all():
            if vote.confidence == 1:
                good += 1
            elif vote.confidence == -1:
                bad += 1
            else:
                neutral += 1
        good = good * 100 / len(ConfidenceMeter.objects.all())
        neutral = neutral * 100 / len(ConfidenceMeter.objects.all())
        bad = bad * 100 / len(ConfidenceMeter.objects.all())

        ret_val = {'good': good, 'neutral': neutral, 'bad': bad}

        #once updated, return results back for html update
        results = ret_val
        
        return HttpResponse(json.dumps(results), content_type='application/json')

    else:
        #if not ajax request, render index page as they are not supposed to request via non ajax
        raise Http404
        pass
"""
Definition of views.
"""

from datetime import datetime
import json

from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.http import Http404 
from django.contrib.auth import views
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, View
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.sessions.models import Session
from django.core.cache import cache

from app.models import ConfidenceMeter, Quiz, Lecture

'''generic view for displaying single messages to the user'''
class AlertView(TemplateView):
    template_name = _("app/alert.html")

    def get_context_data(self, *args, **kwargs):
        context = super(AlertView, self).get_context_data(*args, **kwargs)
        tag = self.kwargs['tag']
        '''message to display is based on the url slug'''
        if tag == "create_user_success":
            context['msg'] = _("Account successfully created!\nPlease log in now")
        else:
            raise Http404
        return context

def logout(request, next_page=None,
           template_name=_('registration/logged_out.html'),
           redirect_field_name=REDIRECT_FIELD_NAME,
           current_app=None, extra_context=None):
    # get user id before logout wipes it
    user_id = request.user.id
    # perform normal logout operation
    ret_val = views.logout(request, next_page, template_name, redirect_field_name, current_app, extra_context)
    # remove session entry from db to maintain correct number of session entries since django only clears the contents not the entry
    Session.objects.all().get(session_key=request.session.session_key).delete()
    for session in Session.objects.all():
        if session.get_decoded().get('_auth_user_id') == user_id:
            # sometimes there are multiple sessions for the same user, delete those sessions as well
            session.delete()
    return ret_val


def long_poll(request):
    # gets all the polling data for all needs
    if request.is_ajax():
        user = request.user
        # need to import in here to prevent circular imports
        from app.context_processors import get_confidence_meter_values
        results = get_confidence_meter_values(request)
        return HttpResponse(json.dumps(results), content_type=_('application/json'))
    else:
        #if not ajax request, render index page as they are not supposed to request via non ajax
        raise Http404
        pass

def student_poll(request):
    if request.is_ajax():

        # need to import in here to prevent circular imports
        from app.context_processors import get_confidence_meter_values
        results = get_confidence_meter_values(request)
        # if there is a change in the quiz_list by checking length
        if int(request.GET.get("quiz_length")) != len(Quiz.objects.filter(visible = True)):
            difference = int(request.GET.get("quiz_length")) - len(Quiz.objects.filter(visible = True))
            results.update({'quiz_difference': difference})
        return HttpResponse(json.dumps(results), content_type=_('application/json'))
    else:
        #if not ajax request, render index page as they are not supposed to request via non ajax
        raise Http404
        pass

def vote(request):
    # voting for the confusion meter

    if request.is_ajax():
        user = request.user
        if request.GET.has_key("vote"):
            vote = request.GET.get("vote")
            # update model
            confidence_object, created = ConfidenceMeter.objects.get_or_create(User=user)
            # new vote 
            if vote == u'1':
                confidence = 1
                cache.incr("good_confidence_meter_data")
            elif vote == u'-1':
                confidence = -1
                cache.incr("bad_confidence_meter_data")
            else:
                #all else is neutral
                confidence = 0
                cache.incr("neutral_confidence_meter_data")

            if confidence_object.confidence == 1:
                cache.decr("good_confidence_meter_data")
            elif confidence_object.confidence == -1:
                cache.decr("bad_confidence_meter_data")
            else:
                cache.decr("neutral_confidence_meter_data")

            confidence_object.confidence = confidence
            confidence_object.save()
        
        # once updated, return results back for html update
        # need to import in here to prevent circular imports
        from app.context_processors import get_confidence_meter_values
        results = get_confidence_meter_values(request)
        return HttpResponse(json.dumps(results), content_type=_('application/json'))
    else:
        #if not ajax request, render 404 as they are not supposed to request via non ajax
        raise Http404
        pass

def quick_update(request):
    # for admin quick settings
    if request.is_ajax():
        user = request.user
        response = {}
        if request.POST.has_key('lecture'):
            # store current lecture in session
            request.session['quick_lecture'] = request.POST.get('lecture')
            lecture = Lecture.objects.get(id=request.POST.get('lecture'))
            response['return_type'] = 'lecture'
            response['return_value'] = request.POST.get('lecture')
            response['notice'] = "Updated Current Lecture to %(lecture)s" % {'lecture':lecture.title}
        if request.POST.has_key('quiz'):
            # mark selected quiz as not visible
            quiz = Quiz.objects.get(id=request.POST.get('quiz'))
            quiz.visible = False
            quiz.save()
            response['return_type'] = 'quiz'
            response['return_value'] = request.POST.get('quiz')
            response['notice'] = "Turned off Quiz %(quiz)s" % {'quiz':quiz.question}


        return HttpResponse(json.dumps(response), content_type=_('application/json'))
    else:
         #if not ajax request, render 404 as they are not supposed to request via non ajax
        raise Http404
        pass
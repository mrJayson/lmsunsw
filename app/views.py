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
from django.views.decorators.cache import cache_page

from app.models import ConfidenceMeter, Quiz, Wordcloud, Lecture

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


@cache_page(5)

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

def vote(request):
    # voting for the confusion meter

    if request.is_ajax():
        user = request.user
        if request.GET.has_key("vote"):
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
            response['notice'] = "Updated Current Lecture to %(lecture)s" % {'lecture':lecture.lecture_name}
        if request.POST.has_key('quiz'):
            # mark selected quiz as not visible
            quiz = Quiz.objects.get(id=request.POST.get('quiz'))
            quiz.visible = False
            quiz.save()
            response['return_type'] = 'quiz'
            response['return_value'] = request.POST.get('quiz')
            response['notice'] = "Turned off Quiz %(quiz)s" % {'quiz':quiz.question}
        if request.POST.has_key('wordcloud'):
            # mark selected wordcloud as not visible
            wordcloud = Wordcloud.objects.get(id=request.POST.get('wordcloud'))
            wordcloud.visible = False
            wordcloud.save()
            # can only reach this area by turning wordcloud's visible to not visible, therefore, always generate image
            created = wordcloud.generate_image()
            response['return_type'] = 'wordcloud'
            response['return_value'] = request.POST.get('wordcloud')
            response['notice'] = "Turned off Wordcloud %(wordcloud)s" % {'wordcloud':wordcloud.title}
            if created:
                response['notice'] += ", Generating an image from inputs"
            else:
                response['notice'] += ", No words were submitted, no image created"

        return HttpResponse(json.dumps(response), content_type=_('application/json'))
    else:
         #if not ajax request, render 404 as they are not supposed to request via non ajax
        raise Http404
        pass
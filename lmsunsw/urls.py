"""
Definition of urls for lmsunsw.
"""

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
from app.admin import user_admin_site


from datetime import datetime
from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout
from django.contrib.auth.forms import AuthenticationForm

from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import user_passes_test, login_required
# check for pages that require the user to not be logged in
login_forbidden =  user_passes_test(lambda u: u.is_anonymous(), '/', None)

from app.views import *
from app.cbv.indexviews import *
from app.cbv.createviews import *


urlpatterns = patterns('',
    # Examples:
    url(r'^$', login_required(IndexView.as_view()), name='index'),
    url(r'^createuser/$',login_forbidden(CreateUser.as_view()), name='createuser'),
    url(r'^alert/(?P<tag>.*)$', AlertView.as_view(), name='alert'),
    url(r'^course/(?P<lect_id>[0-9]+)/(?P<url_slug>[^/]+)$', login_required(LectureView.as_view()), name='lecture'),
    url(r'^course/(?P<lect_id>[0-9]+)/(?P<url_slug>[^/]+)/quiz/(?P<quiz_id>[0-9]+)/(?P<quiz_slug>[^/]+)$', login_required(QuizView.as_view()), name='quiz'),

    url(r'^login/?$', login_forbidden(login), 
        {'template_name':'login.html',
            #'redirect_field_name':'/',
            'authentication_form':AuthenticationForm,
            'extra_context':
                {'title':'LMSUNSW'}},
        name='login'),
    url(r'^logout$',
        'django.contrib.auth.views.logout',
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^settings/', include(user_admin_site.urls), name='settings'),
)
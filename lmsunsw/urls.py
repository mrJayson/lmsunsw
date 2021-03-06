"""
Definition of urls for lmsunsw.
"""

from datetime import datetime

from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import user_passes_test, login_required
# check for pages that require the user to not be logged in
login_forbidden =  user_passes_test(lambda u: u.is_anonymous(), '/', None)
login_superuser =  user_passes_test(lambda u: u.is_superuser, '/', None)

from app.views import *
from app.class_based_views import *
from app.forms import BootstrapAuthenticationForm
from app.admin import adminsite

urlpatterns = patterns('',
    # Examples:

    url(r'^vote/$', login_required(vote), name='vote'),
    url(r'^admin_poll/$', login_required(admin_poll), name='admin_poll'),
    url(r'^student_poll/$', login_required(student_poll), name='student_poll'),
    url(r'^quick_update/$', login_required(quick_update), name='quick_update'),
    url(r'^confidence_message/$', login_required(confidence_message), name='confidence_message'),

    url(r'^help/?$', help, name='help'),

    # index page
    url(r'^$', login_required(IndexView.as_view()), name='root'),
    url(r'^index/?$', login_required(IndexView.as_view()), name='index'),
    # user registration page
    url(r'^createuser/?$',login_forbidden(CreateUser.as_view()), name='createuser'),
    # generic alert message page
    url(r'^alert/(?P<tag>.*)$', AlertView.as_view(), name='alert'),
    # lecture index page
    url(r'^course/(?P<lecture_id>[0-9]+)/(?P<lecture_slug>[^/]+)/?$', login_required(LectureView.as_view()), name='lecture'),
    # quiz page
    url(r'^course/(?P<lecture_id>[0-9]+)/(?P<lecture_slug>[^/]+)/quiz/(?P<quiz_id>[0-9]+)/(?P<quiz_slug>[^/]+)/?$', login_required(QuizView.as_view()), name='quiz'),
    # lecture slide page
    url(r'^course/(?P<lecture_id>[0-9]+)/(?P<lecture_slug>[^/]+)/lecture_slide/?$', login_required(LectureSlideView.as_view()), name='lecture_slide'),
    # thread index page
    url(r'^course/threads/?$', login_required(ThreadView.as_view()), name='thread'),
    # thread create page
    url(r'^course/threads/new/?$', login_required(CreateThreadView.as_view()), name='create_thread'),
    # posts page
    url(r'^course/threads/(?P<thread_id>[0-9]+)/(?P<thread_slug>[^/]+)$', login_required(PostView.as_view()), name='post'),

    url(r'^course/(?P<lecture_id>[0-9]+)/(?P<lecture_slug>[^/]+)/code/?$', login_required(CodeSnippetView.as_view()), name='codesnippet'),

    url(r'^forgot_password/?$', ForgotPasswordView.as_view(), name='forgot_password'),
    # generic login page
    url(r'^login/?$', login_forbidden(login), 
        {'template_name':'app/login.html',
            #'redirect_field_name':'/',
            'authentication_form':BootstrapAuthenticationForm,
        },
        name='login'),
    url(r'^login_/?$', login_forbidden(login), 
        {'template_name':'app/login.html',
            #'redirect_field_name':'/',
            'authentication_form':BootstrapAuthenticationForm,
            'extra_context':{'created':True},
        },
        name='login_'),
    #generic logout page
    url(r'^logout$',
        logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(adminsite.urls)),
    url(r'^admin/quiz-results/?$', login_required(AdminQuizResultsView.as_view()), name='quiz_results'),
    url(r'^admin/quiz-results/(?P<quiz_id>.+)/?$', login_required(AdminQuizResultsDetailView.as_view()), name='quiz_results_detail'),
    url(r'^settings/', include(adminsite.urls)),
    url(r'^dump/(?P<dump>.*)$', login_superuser(dump), name='dump'),
    
    # Django server serves the media files, not an external service, do not think it is needed
    url(r'media/(?P<path>.*)$','django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT
        })

)


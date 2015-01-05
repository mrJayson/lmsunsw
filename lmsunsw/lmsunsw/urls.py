"""
Definition of urls for lmsunsw.
"""

from datetime import datetime
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.contrib.auth.forms import AuthenticationForm
from app.views import *

from django.contrib.auth.decorators import user_passes_test, login_required


# check for pages that require the user to not be logged in
login_forbidden =  user_passes_test(lambda u: u.is_anonymous(), '/', None)

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^register/?$', login_forbidden(register), name='register'),
    url(r'^logout/?$', logout, {'next_page':'/',}, name='logout'),
    url(r'^account/?$', login_required(account, None), name='account'),
    url(r'^course/?$', login_required(course_index), name='courseindex'),
    url(r'^course/(?P<course_code>[A-Z]{4}[0-9]{4})?/$', login_required(course_details), name='coursedetails'),
    url(r'^addcourse/?$', login_required(add_course), name='addcourse'),
    url(r'^course/(?P<course_code>[A-Z]{4}[0-9]{4})/addlecture/?$', login_required(add_lecture), name='addlecture'),
    url(r'^course/(?P<course_code>[A-Z]{4}[0-9]{4})/(?P<lecture_number>[0-9]+)/?$', login_required(lecture_details), name='lecturedetails'),

    url(r'^login/?$', login_forbidden(login), 
        {'template_name':'app/login.html',
            #'redirect_field_name':'/',
            'authentication_form':AuthenticationForm,
            'extra_context':
                {'browser_headline':'Log In'}},
        name='login'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # standard log in redirects to accounts/profile/
    url(r'^accounts/profile/?$', 'app.views.index', name='index'), 
)

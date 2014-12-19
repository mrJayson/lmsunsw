"""
Definition of urls for lmsunsw.
"""

from datetime import datetime
from django.conf.urls import patterns, url
from django.contrib.auth.views import login
from django.contrib.auth.forms import AuthenticationForm

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'app.views.index', name='index'),
    url(r'^register$', 'app.views.register', name='register'),
    #url(r'^login/$', 'app.views.login', name='login'),
    #url(r'^login/$', 'app.views.login', name='login'),
    url(r'^login$', 'django.contrib.auth.views.login', 
        {'template_name':'app/login.html',
            #'redirect_field_name':'/',
            'authentication_form':AuthenticationForm,
            'extra_context':
                {'browser_headline':'Log In'}},
        name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout', 
        {'next_page':'/',},
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

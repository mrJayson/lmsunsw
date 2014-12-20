"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from datetime import datetime
from app.models import *
from app.forms import *
from lmsunsw.settings import DEBUG
from django.contrib import auth

def index(request):
    print "INDEX VIEW"
    assert isinstance(request, HttpRequest)
    extra_content = {'browserheadline':'Index'}
    template = 'app/index.html'
    return render(request, template, context_instance = RequestContext(request, extra_content))

def register(request):
    print "REGISTER VIEW"
    assert isinstance(request, HttpRequest)
    template = 'app/register.html'
    form = RegisterUserForm()
    extra_content = {'browserheadline':'Register', 'form':form}

    # process form
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            template = 'app/registerconfirmation.html'
        else:
            # if error occurs, render the registration page again
            print form.errors
    
    return render(request, template, context_instance = RequestContext(request, extra_content))

def login(request):
    print "LOGIN VIEW"
    assert isinstance(request, HttpRequest)
    template = 'app/login.html'
    form = AuthenticationForm()
    extra_content = {'browserheadline':'Log in', 'form':form}

    if request.method == 'POST':
        form = AuthenticationForm(request.POST, data=request.POST)



    return render(request, template, context_instance = RequestContext(request, extra_content))
    
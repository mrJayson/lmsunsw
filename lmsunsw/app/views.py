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
from django.contrib.auth.decorators import login_required

def index(request):
    print "INDEX VIEW"
    extra_content = {'browserheadline':'Index'}
    template = 'app/index.html'
    if request.user.is_authenticated():
        if request.user.is_staff:
            template = 'app/staff.html'
            class_form = AddCourseForm(request.user)
            extra_content.update({'class_form':class_form})
            print extra_content

        elif not request.user.is_staff:
            template = 'app/student.html'

        elif request.user.is_superuser:
            template = 'app/superuser.html'

    return render(request, template, context_instance = RequestContext(request, extra_content))

def register(request):
    print "REGISTER VIEW"
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


def account(request):
    print "ACCOUNT VIEW"
    template = 'app/account.html'
    extra_context = {'browserheadline':'Account'}


    return render(request, template, context_instance = RequestContext(request, extra_context))

def course(request):
    print "course VIEW"
    template = 'app/course.html'
    extra_context = {'browserheadline':'Course'}
    # if request is a POST, then it is a course creation
    print "REQUEST>METHOD"
    print request.method
    if request.method == 'POST':
        form = AddCourseForm(request.POST)
        if form.is_valid():
            print "form is valid"
            form.save(commit=True)
            # after course is created, need to redirect to the corresponding course url
        else:
            print "form is not valid"
            print form.errors
    # else it is the standard course view
    else:
        class_form = AddCourseForm()
        extra_context.update({'class_form':class_form})

    return render(request, template, context_instance = RequestContext(request, extra_context))

def add_course(request):
    print "add_course VIEW"
    template = 'app/addcourse.html'
    add_course_form = AddCourseForm(request.user)
    extra_context = {'browserheadline':'Add Course','add_course_form':add_course_form}

    return render(request, template, context_instance = RequestContext(request, extra_context))

def add_lecture(request):
    print "add_lecture VIEW"
    template = 'app/lecture.html'
    add_lecture_form = AddLectureForm()
    extra_context = {'browserheadline':'Lecture','add_lecture_form':add_lecture_form}

    return render(request, template, context_instance = RequestContext(request, extra_context))
    
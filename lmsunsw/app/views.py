"""
Definition of views.
"""

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from datetime import datetime
from app.models import *
from app.forms import *
from lmsunsw.settings import DEBUG
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

def index(request):
    extra_content = {'browserheadline':'Index'}
    template = 'app/index.html'
    if request.user.is_authenticated():
        if request.user.is_staff:
            template = 'app/staff.html'

        elif not request.user.is_staff:
            template = 'app/student.html'

        elif request.user.is_superuser:
            template = 'app/superuser.html'

    return render(request, template, context_instance = RequestContext(request, extra_content))

def register(request):
    if request.method == 'POST':
        return register_POST(request)
    else:
        return register_GET(request)

def register_POST(request):
    template = 'app/register.html'
    extra_context = {'browserheadline':'Register'}
    register_user_form = RegisterUserForm(request.POST)
    extra_context.update({'register_user_form':register_user_form})
    if register_user_form.is_valid():
        register_user_form.save()
        # display confirmation page once successful
        template = 'app/registerconfirmation.html'
    else:
        # if error occurs, render the registration page again
        print register_user_form.errors

    return render(request, template, context_instance = RequestContext(request, extra_context))

def register_GET(request):
    template = 'app/register.html'
    extra_context = {'browserheadline':'Register'}
    register_user_form = RegisterUserForm()
    extra_context.update({'register_user_form':register_user_form})

    return render(request, template, context_instance = RequestContext(request, extra_context))


def account(request):
    template = 'app/account.html'
    extra_context = {'browserheadline':'Account'}

    return render(request, template, context_instance = RequestContext(request, extra_context))

def course_index(request):
    template = 'app/courseindex.html'
    extra_context = {'browserheadline':'Course'}
    user = request.user
    course_list = Course.objects.filter(course_head_lecturer=user.id)
    extra_context.update({'course_list':course_list})

    return render(request, template, context_instance = RequestContext(request, extra_context))

def course_details(request, course_code, *args, **kwargs):
    #also lecture index
    
    # first check if the course code in the url is valid
    try:
        course = Course.objects.get(course_code=course_code)
    except(ObjectDoesNotExist):
        return redirect('courseindex')

    template = 'app/coursedetails.html'
    extra_context = {'browserheadline':'Course Details'}
    extra_context.update({'course':course})
    lecture_list = Lecture.objects.filter(course=course.id)
    extra_context.update({'lecture_list':lecture_list})

    return render(request, template, context_instance = RequestContext(request, extra_context))

def add_course(request):
    if request.method == 'POST':
        return add_course_POST(request)
    else:
        return add_course_GET(request)

def add_course_POST(request):
    template = 'app/addcourse.html'
    extra_context = {'browserheadline':'Add Course'}
    add_course_form = AddCourseForm(request.user, request.POST)

    if add_course_form.is_valid():
    # fields filled out correctly
        instance = add_course_form.save()
        # after course is created, need to redirect to the corresponding course url
        #redirects according to the model instance using get_absolute_url()
        return redirect(instance)
    else:
    # forms is not filled out properly, redisplay page with existing details
        extra_context.update({'add_course_form':add_course_form})
        return render(request, template, context_instance = RequestContext(request, extra_context))

def add_course_GET(request):
    template = 'app/addcourse.html'
    extra_context = {'browserheadline':'Add Course'}
    add_course_form = AddCourseForm()
    extra_context.update({'add_course_form':add_course_form})
    return render(request, template, context_instance = RequestContext(request, extra_context))


def add_lecture(request, course_code, *args, **kwargs):
    # first check if the course code in the url is valid
    try:
        course = Course.objects.get(course_code=course_code)
    except(ObjectDoesNotExist):
        return redirect('courseindex')

    if request.method == 'POST':
        return add_lecture_POST(request, course)
    else:
        return add_lecture_GET(request, course)


def add_lecture_POST(request, course, *args, **kwargs):
    template = 'app/addlecture.html'
    extra_context = {'browserheadline':'Lecture'}

    add_lecture_form = AddLectureForm(course, request.POST)
    if add_lecture_form.is_valid():
    # fields filled out correctly
        instance = add_lecture_form.save()
        return redirect(instance)

    else:
    # forms is not filled out properly, redisplay page with existing details
        extra_context.update({'add_lecture_form':add_lecture_form})
        return render(request, template, context_instance = RequestContext(request, extra_context))

def add_lecture_GET(request, course, *args, **kwargs):
    template = 'app/addlecture.html'
    extra_context = {'browserheadline':'Lecture'}
    add_lecture_form = AddLectureForm()
    extra_context.update({'add_lecture_form':add_lecture_form})
    
    return render(request, template, context_instance = RequestContext(request, extra_context))

def lecture_details(request, course_code, lecture_number, *args, **kwargs):
    template = 'app/lecturedetails.html'
    extra_context = {'browserheadline':'Lecture'}

    return render(request, template, context_instance = RequestContext(request, extra_context))
    
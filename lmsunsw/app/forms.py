"""
Definition of forms.
"""

import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models import Max

from app.models import *



class RegisterUserForm(UserCreationForm):

    #email = forms.EmailField(required=True)
    #first_name = forms.CharField(max_length=30)
    #last_name = forms.CharField(max_length=30)

    class Meta:
        # Provide an assoication between the ModelForm and a model
        model = User
        fields = ("username", "password1", "password2", "first_name", "last_name", "email")

    def save(self, commit=True):
        new_user=User.objects.create_user(self.cleaned_data['username'].lower(), self.cleaned_data['email'], self.cleaned_data['password1'])
        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        #user = super(UserCreationForm, self).save(commit=False)
        #user.email = self.cleaned_data["email"]
        #user.first_name = self.cleaned_data["first_name"]
        #user.last_name = self.cleaned_data["last_name"]
        if commit:
            new_user.save()
        return new_user

class AddCourseForm(forms.ModelForm):
    course_name = forms.CharField(widget=forms.TextInput(), max_length=30)
    course_code = forms.RegexField(widget=forms.TextInput(), max_length=8, min_length=8, regex=r'^[A-Z]{4}[0-9]{4}$', error_message = ("Course Code is invalid"))
    course_description = forms.CharField(widget=forms.TextInput())

    #automatically gets called when validating
    def clean_course_code(self):
        data = self.cleaned_data['course_code']

        if not re.match(r'^[A-Z]{4}[0-9]{4}$',data, re.UNICODE):
            raise forms.ValidationError(u'Course Code is invalid')
        #self.cleaned_data['course_code'] = data.upper() # to satisfy the model validation
        #print self.cleaned_data['course_code']
        return data

    def save(self, commit=True):
        instance = super(AddCourseForm, self).save(commit=False) # call super's save function, which deals with other fields
        instance.course_head_lecturer = self.user
        if commit:
            instance.save()
        return instance

    def __init__(self, user=None, *args, **kwargs):
        super(AddCourseForm, self).__init__(*args, **kwargs)
        self.user = user

    class Meta:
        # Provide an assoication between the ModelForm and a model
        model = Course
        fields = ('course_name', 'course_code', 'course_description')

class AddLectureForm(forms.ModelForm):
    lecture_name = forms.CharField(max_length=30)
    #lecture_number = forms.IntegerField()

    def save(self, commit=True):
        instance = super(AddLectureForm, self).save(commit=False)   # call super's save function, which deals with other fields

        # internally inc the lecture number for each course since (lecture_number,course) is unique
        lecture_number_inc = Lecture.objects.filter(course=self.course).aggregate(Max('lecture_number'))['lecture_number__max']
        if lecture_number_inc:
            instance.lecture_number = lecture_number_inc + 1
        else:
            instance.lecture_number = 1
        instance.course = self.course                               # link a parent course to the lecture
        instance.save()

        return instance

    def __init__(self, course=None, *args, **kwargs):
        super(AddLectureForm, self).__init__(*args, **kwargs)
        self.course = course

    class Meta:
        # Provide an assoication between the ModelForm and a model
        model = Lecture
        fields = ('lecture_name',)
        
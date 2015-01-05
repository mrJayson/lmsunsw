"""
Definition of forms.
"""

import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

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
    course_name = forms.CharField(max_length=30)
    course_code = forms.CharField(max_length=8, min_length=4)
    course_description = forms.CharField(widget=forms.TextInput())

    #automatically gets called when validating
    def clean_course_code(self):
        data = self.cleaned_data['course_code']
        if not re.match("[A-Z]{4}[0-9]{4}",data):
            raise forms.ValidationError("Course Code is invalid")
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
    lecture_week = forms.IntegerField()

    class Meta:
        # Provide an assoication between the ModelForm and a model
        model = Lecture
        fields = ('lecture_name', 'lecture_week')
        
"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from app.models import *

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class CreateUserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        # Provide an assoication between the ModelForm and a model
        model = User
        fields = ("username", "password1", "password2", "first_name", "last_name", "email")


'''
    def save(self, commit=True):
        new_user=User.objects.create_user(self.cleaned_data['username'].lower(), self.cleaned_data['email'], self.cleaned_data['password1'])
        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']

        if commit:
            new_user.save()
        return new_user'''

class QuizSelectionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(QuizSelectionForm, self).__init__(*args, **kwargs)
        self.user = kwargs.get('user')
        self.quiz_id = kwargs.get('quiz_id')



        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = QuizChoiceSelected
        

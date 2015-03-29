"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from app.models import *

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, Button

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


class QuizSelectionForm(forms.Form):

    def __init__(self, user, quiz_id, *args, **kwargs):
        super(QuizSelectionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        #get the question title
        quiz_question = Quiz.objects.get(pk=quiz_id).question
        queryset = QuizChoice.objects.filter(Quiz=quiz_id)
        #iterate through list  to create field for each choice
        quiz_choice_list = []
        for quiz_choice in queryset:
            #place in tuples for radio buttons to display
            quiz_choice_list.append((quiz_choice.id, quiz_choice.choice))

        try:
            #if quiz has been answered already, display result of answer
            quiz_choice_selected = QuizChoiceSelected.objects.get(user=user,quiz_choice__Quiz=quiz_id) #get is faster than filter so must use this exception
            initial_value = quiz_choice_selected.quiz_choice.id
            self.fields['choices'] = forms.ChoiceField(choices = quiz_choice_list, required=True, initial=initial_value, widget=forms.RadioSelect)
            self.helper.layout.append(Fieldset(quiz_question, Field('choices', disabled="true")))
            # display a 'correct' or wrong 'button' depending on answer
            if quiz_choice_selected.quiz_choice.correct:
                self.helper.add_input(Button(name = "", value="CORRECT", css_class='btn-success'))
            else:
                self.helper.add_input(Button(name = "", value="WRONG", css_class='btn-danger'))

        except QuizChoiceSelected.DoesNotExist: #if quiz has not been answered yet, display proper format for submission 
            self.fields['choices'] = forms.ChoiceField(choices = quiz_choice_list, required=True, widget=forms.RadioSelect)

            #add hidden values into form
            self.fields['user'] = forms.CharField(widget=forms.HiddenInput())
            self.fields['quiz_id'] = forms.CharField(widget=forms.HiddenInput())

            self.helper.layout.append(Fieldset(quiz_question, Field('choices'), Field('user', value=user, type="hidden"), Field('quiz_id', value=quiz_id, type="hidden")))
            # submit button only needed if quiz has not been previously answered
            self.helper.add_input(Submit('submit', 'Submit'))

        # to prevent default form messages from being displayed, answer selection can never be wrong
        self.helper.form_show_errors = False
        self.helper.form_show_labels = False

    def is_valid(self):
        # this func is needed because is_valid would not run without defining it for some reason
        return super(QuizSelectionForm, self).is_valid()

    def clean_choices(self):
        choices = self.cleaned_data["choices"]
        return choices

    def save(self, *args, **kwargs):
        data = self.cleaned_data
        # need user and choices to create object
        if data.get('user') and data.get('choices'):
            user_object = User.objects.get(username=data.get('user'))
            quiz_choice_object = QuizChoice.objects.get(id=data.get('choices'))
        new_quiz_choice_selected = QuizChoiceSelected.objects.create(user=user_object, quiz_choice=quiz_choice_object)
        return new_quiz_choice_selected

    class Meta:
        fields = ()
        

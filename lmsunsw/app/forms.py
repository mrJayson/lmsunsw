"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from app.models import *

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field

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

    def __init__(self, user, quiz_id, quiz_choice_selected=None, *args, **kwargs):
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

        #create form fields and append to helper for crispy to display
        readonly = False
        if quiz_choice_selected is not None:
            readonly = True
        self.fields['choices'] = forms.ChoiceField(choices = quiz_choice_list, required=True, widget=forms.RadioSelect, initial=QuizChoiceSelected.objects.get(id=quiz_choice_selected).quiz_choice.id, attrs={'readonly':'readonly'})

        #add hidden values into form
        self.fields['user'] = forms.CharField(widget=forms.HiddenInput())
        self.fields['quiz_id'] = forms.CharField(widget=forms.HiddenInput())

        #attr value is used because form.initial in the hidden fields do not work
        self.helper.layout.append(Fieldset(quiz_question, Field('choices'), Field('user', value=user, type="hidden"), Field('quiz_id', value=quiz_id, type="hidden")))

        self.helper.form_show_labels = False

        self.helper.add_input(Submit('submit', 'Submit'))

    def is_valid(self):

        print "is_valid"
        print self.data
        print super(QuizSelectionForm, self).is_valid()
        print self.errors
        return super(QuizSelectionForm, self).is_valid()

    def clean_choices(self):
        choices = self.cleaned_data["choices"]
        return choices


    def save(self, *args, **kwargs):
        data = self.cleaned_data
        if data.get('user') and data.get('choices'):
            print "user save"
            print data.get('user')
            print "user save"
            print data.get('choices')
            user_object = User.objects.get(username=data.get('user'))
            quiz_choice_object = QuizChoice.objects.get(id=data.get('choices'))
        to_be_saved = QuizChoiceSelected.objects.create(user=user_object, quiz_choice=quiz_choice_object)
        return to_be_saved


    class Meta:
        fields = ()
        

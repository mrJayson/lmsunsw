"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from app.models import *

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, Button
#from app.widgets import AdminTextInputWidget, AdminURLFieldWidget
from django.contrib.admin import widgets
from django.contrib.auth.models import Permission

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
        self.fields['username'].widget = forms.TextInput(attrs={'placeholder': 'User name', 'id': 'admin-form-control', 'class': 'form-control'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Password', 'id': 'admin-form-control', 'class': 'form-control'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Type in your password again', 'id': 'admin-form-control', 'class': 'form-control'})
        self.fields['first_name'].widget = forms.TextInput(attrs={'placeholder': 'First Name', 'id': 'admin-form-control', 'class': 'form-control'})
        self.fields['last_name'].widget = forms.TextInput(attrs={'placeholder': 'Last Name', 'id': 'admin-form-control', 'class': 'form-control'})
        self.fields['email'].widget = forms.TextInput(attrs={'placeholder': 'Email Address', 'id': 'admin-form-control', 'class': 'form-control'})
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        # Provide an assoication between the ModelForm and a model
        model = User
        fields = ("username", "password1", "password2", "first_name", "last_name", "email")

    def save(self, *args, **kwargs):
        new_user = super(CreateUserForm, self).save(*args, **kwargs)
        # add permissions user upon creation
        new_user.user_permissions.add(
            Permission.objects.get(name='Can change user'),
            Permission.objects.get(name='Can change user profile'),
            Permission.objects.get(name='Can add thread'),
            Permission.objects.get(name='Can change thread'),
            Permission.objects.get(name='Can add post'),
            Permission.objects.get(name='Can change post'),
        )
        return new_user


class QuizSelectionForm(forms.Form):

    def __init__(self, user, quiz, *args, **kwargs):

        ################ data initialise ###################

        super(QuizSelectionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout()

        queryset = QuizChoice.objects.filter(Quiz=quiz.id)
        #iterate through list  to create field for each choice
        quiz_choice_list = []
        for quiz_choice in queryset:
            #place in tuples for radio buttons to display
            quiz_choice_list.append((quiz_choice.id, quiz_choice.choice))

        # switch on quiz_type
        

        ################### SINGLEMCQ ###################
        # forms are radio buttons, have only one correct answer
        # response is either correct or wrong

        if quiz.quiz_type == QuizType.SINGLEMCQ:

            # if quiz not answered yet, filter will return an empty list
            quiz_choice_selected = QuizChoiceSelected.objects.filter(User=user, QuizChoice__Quiz=quiz.id)
            if len(quiz_choice_selected) == 0:
                # Quiz not answered yet, prepare form to collect
                self.fields['choices'] = forms.ChoiceField(
                    choices = quiz_choice_list,
                    required=True,
                    widget=forms.RadioSelect
                    )
                # add hidden values into form
                self.fields['user'] = forms.CharField(widget=forms.HiddenInput())
                self.fields['quiz_id'] = forms.CharField(widget=forms.HiddenInput())
                self.helper.layout.append(
                    Fieldset(
                        quiz.question,
                        Field('choices'),
                        Field('user', value=user, type="hidden"),
                        Field('quiz_id', value=quiz.id, type="hidden")
                        )
                    )
                # form is to have a submit button since it needs to collect data
                self.helper.add_input(Submit('submit', 'Submit'))
            else:
                # Quiz answered, prepare form to display result
                # SINGLEMCQ only allows one choice to be selected
                initial_value = quiz_choice_selected.first().QuizChoice.id
                self.fields['choices'] = forms.ChoiceField(
                    choices = quiz_choice_list,
                    required=True,
                    initial=initial_value,
                    widget=forms.RadioSelect
                    )
                self.helper.layout.append(
                    Fieldset(
                        quiz.question,
                        Field('choices', disabled="true")
                        )
                    )
                # depending on the chosen choice, display the result in place of the submit button
                if quiz_choice_selected.first().QuizChoice.correct:
                    self.helper.add_input(Button(name = "", value="CORRECT", css_class='btn-success'))
                else:
                    self.helper.add_input(Button(name = "", value="WRONG", css_class='btn-danger'))

        ################### MULTIMCQ ###################
        # forms are checkboxes, can have multiple correct answers, but at least one correct
        # response can be correct, partially correct or wrong

        if quiz.quiz_type == QuizType.MULTIMCQ:

            # if quiz not answered yet, filter will return an empty list
            quiz_choice_selected = QuizChoiceSelected.objects.filter(User=user, QuizChoice__Quiz=quiz.id)
            if len(quiz_choice_selected) == 0:
                # Quiz not answered yet, prepare form to collect
                self.fields['choices'] = forms.MultipleChoiceField(
                    choices = quiz_choice_list,
                    required=True,
                    widget=forms.CheckboxSelectMultiple,
                    help_text="Select all that apply"
                    )
                # add hidden values into form
                self.fields['user'] = forms.CharField(widget=forms.HiddenInput())
                self.fields['quiz_id'] = forms.CharField(widget=forms.HiddenInput())
                self.helper.layout.append(
                    Fieldset(
                        quiz.question,
                        Field('choices'),
                        Field('user', value=user, type="hidden"),
                        Field('quiz_id', value=quiz.id, type="hidden")
                        )
                    )
                # form is to have a submit button since it needs to collect data
                self.helper.add_input(Submit('submit', 'Submit'))
            else:
                # Quiz answered, prepare form to display result
                # MULTIMCQ will have many choices selected
                initial_value = [qcs.QuizChoice.id for qcs in quiz_choice_selected]
                self.fields['choices'] = forms.MultipleChoiceField(
                    choices = quiz_choice_list,
                    required=True,
                    initial=initial_value,
                    widget=forms.CheckboxSelectMultiple
                    )
                self.helper.layout.append(
                    Fieldset(
                        quiz.question,
                        Field('choices', disabled="true")
                        )
                    )
                # depending on the chosen choice, display the result in place of the submit button
                list_of_corrects = QuizChoice.objects.filter(Quiz=quiz, correct=True)
                overlapping_choices = set([qcs.QuizChoice for qcs in quiz_choice_selected]) & set(list_of_corrects)

                if len(overlapping_choices) == 0:
                    # completely wrong
                    self.helper.add_input(Button(name = "", value="WRONG", css_class='btn-danger'))
                elif len(overlapping_choices) == len(list_of_corrects):
                    # all correct
                    self.helper.add_input(Button(name = "", value="CORRECT", css_class='btn-success'))
                else:
                    # somewhere in between, partially correct
                    self.helper.add_input(Button(name = "", value="PARTIALLY CORRECT", css_class='btn-warning'))


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
        # change a single choice into an array of single choice so that it will work in the query
        selected_choices = data.get('choices') if type(data.get('choices'))==type([]) else [data.get('choices')]
        # need user and choices to create object
        user_object = User.objects.get(username=data.get('user'))
        return [QuizChoiceSelected.objects.create(User=user_object, QuizChoice=selection)
        for selection in QuizChoice.objects.filter(id__in=selected_choices)]

    class Meta:
        fields = ()
class CreateThreadForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(CreateThreadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout()

        self.fields['title'] = forms.CharField(widget=forms.TextInput(attrs={'id': 'admin-form-control', 'class': 'form-control'}))
        self.fields['content'] = forms.CharField(widget=forms.Textarea(attrs={'id': 'admin-form-control', 'class': 'form-control'}))
        self.fields['Creator'] = forms.CharField(widget=forms.HiddenInput(attrs={'value':user.id}))
        self.fields['views'] = forms.IntegerField(widget=forms.HiddenInput(attrs={'value': 0}))
        self.helper.layout.append(
            Fieldset(
                "New Topic",
                Field('title'),
                Field('content'),
                Field('Creator'),
                Field('views'),
                )
            )
        self.helper.add_input(Submit('submit', 'Submit'))

    def clean_Creator(self):
        user_object = User.objects.get(id=self.cleaned_data.get('Creator'))
        return user_object

    class Meta:
        model = Thread
        #fields = ('title', 'content')

class PostReplyForm(forms.ModelForm):


    def __init__(self, user, thread, *args, **kwargs):
        super(PostReplyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.thread = thread

        self.fields['Thread'] = forms.CharField(widget=forms.HiddenInput(attrs={'value':thread.id}))
        self.fields['content'] = forms.CharField(label="Reply", widget=forms.Textarea(attrs={'id': 'admin-form-control', 'class': 'form-control'}))
        self.fields['Creator'] = forms.CharField(widget=forms.HiddenInput(attrs={'value':user.id}))
        self.fields['anonymous'] = forms.BooleanField(initial=True, required=False)
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Post
        fields = ('content',)

    def save(self, *args, **kwargs):
        data = self.cleaned_data
        thread_object = Thread.objects.get(id=data.get('Thread'))
        content = data.get('content')
        Creator = user_object = User.objects.get(id=data.get('Creator'))
        rank = thread_object.replies
        anonymous = data.get('anonymous')
        post_object = Post.objects.create(Thread=thread_object, content=content, Creator=Creator, rank=rank, anonymous=anonymous)
        return post_object


###################################################################################################
# Custom Admin forms

class DefaultUserAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DefaultUserAdminForm, self).__init__(*args, **kwargs)

class QuizAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(QuizAdminForm, self).__init__(*args, **kwargs)
        self.fields['question'].widget = widgets.AdminTextareaWidget({'id': 'admin-form-control', 'class': 'form-control'})
        #self.fields['visible'].widget = widgets.AdminTextareaWidget({'id': 'admin-form-control', 'class': 'form-control'})
        #self.fields['Lecture'].widget = widgets.AdminTextareaWidget({'id': 'admin-form-control', 'class': 'form-control'})

class LectureAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LectureAdminForm, self).__init__(*args, **kwargs)
        self.fields['lecture_name'].widget = widgets.AdminTextInputWidget({'id': 'admin-form-control', 'class': 'form-control', 'placeholder': 'Title of the Lecture'})
        self.fields['lecture_slide'].widget = widgets.AdminURLFieldWidget({'id': 'admin-form-control', 'class': 'form-control', 'placeholder': 'Lecture Slide URL'})
        self.fields['collab_doc'].widget = widgets.AdminURLFieldWidget({'id': 'admin-form-control', 'class': 'form-control', 'placeholder': 'A generic Document will be provided if left empty'})

class WordcloudAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WordcloudAdminForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget = widgets.AdminTextInputWidget({'id': 'admin-form-control', 'class': 'form-control', 'placeholder': 'Title of the wordcloud'})
        self.fields['words'].widget = widgets.AdminTextareaWidget({'id': 'admin-form-control', 'class': 'form-control', 'placeholder': 'The words to be placed into the word cloud as a String'})

class QuizChoiceInLineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WordcloudAdminForm, self).__init__(*args, **kwargs)
        self.fields['choice'].widget = widgets.AdminTextareaWidget({'id': 'admin-form-control', 'class': 'form-control', 'placeholder': 'One of the quiz choices'})
        self.fields['Quiz'].widget = widgets.AdminURLFieldWidget({'id': 'admin-form-control', 'class': 'form-control', 'placeholder': 'Lecture Slide URL'})
        self.fields['correct'].widget = widgets.AdminURLFieldWidget({'id': 'admin-form-control', 'class': 'form-control', 'placeholder': 'A generic Document will be provided if left empty'})


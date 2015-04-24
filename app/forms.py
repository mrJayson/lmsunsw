"""
Definition of forms.
"""

import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import widgets
from django.contrib.auth.models import Permission
from django.conf import settings
from django.forms.models import inlineformset_factory, BaseInlineFormSet

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, Button
from crispy_forms.bootstrap import InlineField

from app.models import *

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   _('class'): _('form-control'),
                                   _('placeholder'): _('User name')}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   _('class'): _('form-control'),
                                   _('placeholder'):_('Password')}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username.lower()

class CreateUserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['username'].widget = forms.TextInput(attrs={_('placeholder'): _('User name'), _('class'): _('form-control')})
        self.fields['password1'].widget = forms.PasswordInput(attrs={_('placeholder'): _('Password'), _('class'): _('form-control')})
        self.fields['password2'].widget = forms.PasswordInput(attrs={_('placeholder'): _('Type in your password again'), _('class'): _('form-control')})
        self.fields['first_name'].widget = forms.TextInput(attrs={_('placeholder'): _('First Name'), _('class'): _('form-control')})
        self.fields['last_name'].widget = forms.TextInput(attrs={_('placeholder'): _('Last Name'), _('class'): _('form-control')})
        self.fields['email'].widget = forms.TextInput(attrs={_('placeholder'): _('Email Address'), _('class'): _('form-control')})
        self.helper.add_input(Submit(_('submit'), _('Submit')))

    class Meta:
        # Provide an assoication between the ModelForm and a model
        model = User
        fields = ("username", "password1", "password2", "first_name", "last_name", "email")

    def save(self, *args, **kwargs):
        new_user = super(CreateUserForm, self).save(*args, **kwargs)
        # add permissions user upon creation
        new_user.user_permissions.add(
            Permission.objects.get(name=_('Can change user')),
            Permission.objects.get(name=_('Can change user profile')),
            Permission.objects.get(name=_('Can add thread')),
            Permission.objects.get(name=_('Can change thread')),
            Permission.objects.get(name=_('Can add post')),
            Permission.objects.get(name=_('Can change post')),
        )
        return new_user

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username.lower()

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
                self.fields['user'] = forms.CharField(widget=forms.HiddenInput(attrs={_('value'):user.id}))
                self.helper.layout.append(
                    Fieldset(
                        quiz.question,
                        Field('choices'),
                        Field('user')
                        )
                    )
                # form is to have a submit button since it needs to collect data
                self.helper.add_input(Submit(_('submit'), _('Submit')))
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
                        Field('choices', disabled=_('true'))
                        )
                    )
                # depending on the chosen choice, display the result in place of the submit button
                if quiz_choice_selected.first().QuizChoice.correct:
                    self.helper.add_input(Button(name = "", value="CORRECT", css_class="btn-success"))
                else:
                    self.helper.add_input(Button(name = "", value="WRONG", css_class="btn-danger"))

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
                    help_text=_("Select all that apply")
                    )
                # add hidden values into form
                self.fields['user'] = forms.CharField(widget=forms.HiddenInput(attrs={_('value'):user.id}))
                self.helper.layout.append(
                    Fieldset(
                        quiz.question,
                        Field('choices'),
                        Field('user')
                        )
                    )
                # form is to have a submit button since it needs to collect data
                self.helper.add_input(Submit(_('submit'), _('Submit')))
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
                        Field('choices', disabled=_('true'))
                        )
                    )
                # depending on the chosen choice, display the result in place of the submit button
                list_of_corrects = QuizChoice.objects.filter(Quiz=quiz, correct=True)
                overlapping_choices = set([qcs.QuizChoice for qcs in quiz_choice_selected]) & set(list_of_corrects)

                if len(overlapping_choices) == 0:
                    # completely wrong
                    self.helper.add_input(Button(name = _(""), value="WRONG", css_class='btn-danger'))
                elif len(overlapping_choices) == len(list_of_corrects):
                    # all correct
                    self.helper.add_input(Button(name = _(""), value="CORRECT", css_class='btn-success'))
                else:
                    # somewhere in between, partially correct
                    self.helper.add_input(Button(name = _(""), value="PARTIALLY CORRECT", css_class='btn-warning'))


        # to prevent default form messages from being displayed, answer selection can never be wrong
        self.helper.form_show_errors = False
        self.helper.form_show_labels = False

    def is_valid(self):
        return super(QuizSelectionForm, self).is_valid()

    def clean_user(self):
        user = self.cleaned_data.get('user')
        return User.objects.get(id=user)

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

        self.fields['title'] = forms.CharField(widget=forms.TextInput(attrs={_('class'): _('form-control')}))
        self.fields['content'] = forms.CharField(widget=forms.Textarea(attrs={_('class'): _('form-control')}))
        self.fields['Creator'] = forms.CharField(widget=forms.HiddenInput(attrs={_('value'):user.id}))
        self.fields['views'] = forms.IntegerField(widget=forms.HiddenInput(attrs={_('value'): 0}))
        self.helper.layout.append(
            Fieldset(
                "New Topic",
                Field('title'),
                Field('content'),
                Field('Creator'),
                Field('views'),
                )
            )
        self.helper.add_input(Submit(_('submit'), _('Submit')))

    def clean_Creator(self):
        user_object = User.objects.get(id=self.cleaned_data.get('Creator'))
        return user_object

    class Meta:
        model = Thread
        fields = ('title', 'content')

class PostReplyForm(forms.ModelForm):

    def __init__(self, user, thread, *args, **kwargs):
        super(PostReplyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.thread = thread

        self.fields['Thread'] = forms.CharField(widget=forms.HiddenInput(attrs={_('value'):thread.id}))
        self.fields['content'] = forms.CharField(label=_("Reply"), widget=forms.Textarea(attrs={_('class'): _('form-control')}))
        self.fields['Creator'] = forms.CharField(widget=forms.HiddenInput(attrs={_('value'):user.id}))
        self.fields['anonymous'] = forms.BooleanField(initial=True, required=False)
        self.helper.add_input(Submit(_('submit'), _('Submit')))

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

class WordcloudSubmissionForm(forms.ModelForm):

    class Meta:
        model = WordcloudSubmission
        fields = ('User', 'Wordcloud', 'word')

    def __init__(self, user, wordcloud, *args, **kwargs):
        super(WordcloudSubmissionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        
        previous_entries = WordcloudSubmission.objects.filter(User=user, Wordcloud=wordcloud)
        if previous_entries.exists():
            # if submission has already been made
            self.fields['word'] = forms.CharField(label=_("You have submitted the word:"), initial=previous_entries.first().word, widget=forms.TextInput(attrs={_('class'): _('form-control'), _('placeholder'):_('Enter one word only')}))
            self.fields['User'] = forms.CharField(widget=forms.HiddenInput())
            self.fields['Wordcloud'] = forms.CharField(widget=forms.HiddenInput())
            self.helper.layout.append(
            Fieldset(
                    wordcloud.title,
                    Field('word', disabled=True),
                    Field('User'),
                    Field('Wordcloud'),
                )
            )
            self.helper.add_input(Button(name = _(""), value=_("Submitted"), css_class=_('btn-primary')))

        else:
            self.fields['word'] = forms.CharField(label=_("Enter your word into the wordcloud!"), widget=forms.TextInput(attrs={_('class'): _('form-control'), _('placeholder'):_('Enter one word only')}))
            self.fields['User'] = forms.CharField(widget=forms.HiddenInput(attrs={_('value'):user.id}))
            self.fields['Wordcloud'] = forms.CharField(widget=forms.HiddenInput(attrs={_('value'):wordcloud.id}))
            self.helper.layout.append(
            Fieldset(
                    wordcloud.title,
                    Field('word'),
                    Field('User'),
                    Field('Wordcloud'),
                )
            )
            self.helper.add_input(Submit(_('submit'), _('Submit')))
            
    def is_valid(self):
        valid = super(WordcloudSubmissionForm, self).is_valid()
        if not valid:
            # no need to check if already invalid
            return valid
        if re.search('[^a-zA-Z]', self.cleaned_data.get('word')):
            self._errors['word'] = [_('Input must be only one word')]
            return False
            
        # passed all tests
        return True

    def clean_User(self):
        return User.objects.get(id=self.cleaned_data.get('User'))

    def clean_Wordcloud(self):
        return Wordcloud.objects.get(id=self.cleaned_data.get('Wordcloud'))

    def clean_word(self):
        return self.cleaned_data.get('word').lstrip().rstrip()

###################################################################################################
# Admin Dashboard forms

class QuickSettingsForm(forms.Form):

    def __init__(self, session=None, *args, **kwargs):
        super(QuickSettingsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'quick_settings_form'
        self.helper.layout = Layout()
        # assign current lecture from session
        if session!=None and session.has_key('quick_lecture'):
            quick_lecture = session.get('quick_lecture')
        else:
            quick_lecture = Lecture.objects.last().id

        visible_quizzes = [(i.id, i.question) for i in Quiz.objects.filter(visible=True)]
        visible_wordclouds = [(i.id, i.title) for i in Wordcloud.objects.filter(visible=True)]
        self.fields['Lecture'] = forms.ChoiceField(
            label = _("Current Lecture"),
            initial = quick_lecture,
            choices = [(i.id,i.lecture_name) for i in Lecture.objects.all()],
            widget = forms.Select(attrs={_('id'):('quick_lecture_select'), _('class'): _('form-control')}),
            )
        if visible_quizzes:
            self.fields['visible_quizzes'] = forms.ChoiceField(
                label = _("Currently visible Quizzes, click to finish"),
                choices = visible_quizzes,
                widget=forms.SelectMultiple(attrs={_('id'):('quick_quiz_select'), _('class'): _('form-control')}),
                )
        if visible_wordclouds:
            self.fields['visible_wordclouds'] = forms.ChoiceField(
                label = _("Currently visible Wordclouds, click to finish"),
                choices = visible_wordclouds,
                widget=forms.SelectMultiple(attrs={_('id'):('quick_wordcloud_select'), _('class'): _('form-control')}),
                )

class QuickQuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('question', 'Lecture', 'visible')

    def __init__(self, session=None, *args, **kwargs):
        super(QuickQuizForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout()

        self.fields['question'] = forms.CharField(label=_("Question"), widget=forms.TextInput(attrs={_('class'): _('form-control')}))
        self.fields['visible'] = forms.BooleanField(initial=True, required=False)
        # assign current lecture from session
        if session!=None and session.has_key('quick_lecture'):
            quick_lecture = session.get('quick_lecture')
        else:
            quick_lecture = Lecture.objects.last().id
        self.fields['Lecture'] = forms.CharField(widget=forms.HiddenInput(attrs={_('value'):quick_lecture}))
        self.helper.add_input(Submit(_('quiz'), _('Submit')))

    def clean_Lecture(self):
        lecture = Lecture.objects.get(id=self.cleaned_data.get('Lecture'))
        return lecture

class QuickQuizInlineForm(forms.ModelForm):
    # forms for inlines
    class Meta:
        model = QuizChoice
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(QuickQuizInlineForm, self).__init__(*args, **kwargs)
        self.fields['choice'] = forms.CharField(label='', widget=forms.TextInput( attrs={_('class'): _('form-control'), _('placeholder'): _('Quiz Choice')}))

# inlineForm factory to generate multiple forms
QuickQuizInlineFormSet = inlineformset_factory(
    Quiz,
    QuizChoice,
    form=QuickQuizInlineForm,
    can_delete=False,
    extra=4,
    )

class QuickWordcloudForm(forms.ModelForm):
    class Meta:
        model = Wordcloud
        fields = ('title', 'visible', 'Lecture')

    def __init__(self, session=None, *args, **kwargs):
        super(QuickWordcloudForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.fields['title'] = forms.CharField(label=_("Title"), widget=forms.TextInput(attrs={_('class'): _('form-control')}))
        self.fields['visible'] = forms.BooleanField(initial=True, required=False)
        # assign current lecture from session
        if session!=None and session.has_key('quick_lecture'):
            quick_lecture = session.get('quick_lecture')
        else:
            quick_lecture = Lecture.objects.last().id
        self.fields['Lecture'] = forms.CharField(widget=forms.HiddenInput(attrs={_('value'):quick_lecture}))
        self.helper.add_input(Submit(_('wordcloud'), _('Submit')))

    def clean_Lecture(self):
        lecture = Lecture.objects.get(id=self.cleaned_data.get('Lecture'))
        return lecture


class QuickCodeSnippetForm(forms.ModelForm):
    class Meta:
        model = CodeSnippet
        fields = ('syntax', 'code', 'linenumbers', 'style', 'Lecture')

    def __init__(self, session=None, *args, **kwargs):
        super(QuickCodeSnippetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout()

        self.fields['code'] = forms.CharField(label=_("Code"), widget=forms.Textarea(attrs={_('class'): _('form-control')}))
        # assign current lecture from session
        if session!=None and session.has_key('quick_lecture'):
            quick_lecture = session.get('quick_lecture')
        else:
            quick_lecture = Lecture.objects.last().id
        self.fields['Lecture'] = forms.CharField(widget=forms.HiddenInput(attrs={_('value'):quick_lecture}))

        self.helper.add_input(Submit(_('codesnippet'), _('Submit')))

    def clean_Lecture(self):
        lecture = Lecture.objects.get(id=self.cleaned_data.get('Lecture'))
        return lecture

###################################################################################################
# Custom Admin forms

class DefaultUserAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DefaultUserAdminForm, self).__init__(*args, **kwargs)

class QuizAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(QuizAdminForm, self).__init__(*args, **kwargs)
        self.fields['question'].widget = widgets.AdminTextareaWidget({_('class'): _('form-control')})

class LectureAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LectureAdminForm, self).__init__(*args, **kwargs)
        self.fields['lecture_name'].widget = widgets.AdminTextInputWidget({_('class'): _('form-control'), _('placeholder'): _('Title of the Lecture')})
        self.fields['lecture_slide'].widget = widgets.AdminURLFieldWidget({_('class'): _('form-control'), _('placeholder'): _('Lecture Slide URL')})
        self.fields['collab_doc'].widget = widgets.AdminURLFieldWidget({_('class'): _('form-control'), _('placeholder'): _('A generic Document will be provided if left empty')})

    def clean_collab_doc(self):
        collab_doc = self.cleaned_data.get('collab_doc')
        # if field is empty, retrieve an unused gdoc
        if collab_doc == "":
            collab_doc = Lecture.get_unused_gdoc()
        return collab_doc

class WordcloudAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WordcloudAdminForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget = widgets.AdminTextInputWidget({_('class'): _('form-control'), _('placeholder'): _('Title of the wordcloud')})

class QuizChoiceInLineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WordcloudAdminForm, self).__init__(*args, **kwargs)
        self.fields['choice'].widget = widgets.AdminTextareaWidget({_('class'): _('form-control'), _('placeholder'): _('One of the quiz choices')})
        self.fields['Quiz'].widget = widgets.AdminURLFieldWidget({_('class'): _('form-control'), _('placeholder'): _('Lecture Slide URL')})
        self.fields['correct'].widget = widgets.AdminURLFieldWidget({_('class'): _('form-control'), _('placeholder'): _('A generic Document will be provided if left empty')})

class CodeSnippetAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CodeSnippetAdminForm, self).__init__(*args, **kwargs)
        self.fields['code'].widget = widgets.AdminTextareaWidget({_('class'): _('form-control')})
class ThreadAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ThreadAdminForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget = widgets.AdminTextInputWidget({_('class'): _('form-control')})
        self.fields['content'].widget = widgets.AdminTextareaWidget({_('class'): _('form-control')})
        self.fields['views'].widget = widgets.AdminTextInputWidget({_('class'): _('form-control')})
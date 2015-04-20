"""
Customizations for the Django administration interface
"""
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils import six
from django.apps import apps
from django.contrib.admin import widgets
from django.conf import settings
from django.shortcuts import render, redirect

from wordcloud import WordCloud

from app.models import *
from app.forms import LectureAdminForm, QuizAdminForm, WordcloudAdminForm, QuizChoiceInLineForm, CodeSnippetAdminForm, ThreadAdminForm

###################################################################################################

# Admin settings for staff

class CustomUserAdmin(UserAdmin):
    list_display = ('username','email', 'first_name', 'last_name')

    def get_fieldsets(self, request, obj=None):
        if not request.user.is_superuser:
            return ((None, {'fields': ('username', 'password')}),(_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),)
        else:
            return super(CustomUserAdmin, self).get_fieldsets(request, obj)

    def changelist_view(self, request, extra_context=None):
        if not request.user.is_superuser:
            return redirect(reverse('admin:%s_%s_change' % (self.model._meta.app_label, self.model._meta.model_name), args=(request.user.id,)))
        return super(CustomUserAdmin, self).changelist_view(request=request, extra_context=extra_context)

class QuizChoiceInLine(admin.StackedInline):
    model = QuizChoice
    # min number of quiz choices per quiz is two
    min_num = 2
    # display two more quiz choices forms by default, giving 4 choices as standard
    extra = 2-1
    # override admin css styling for inputs
    def formfield_for_dbfield(self, db_field, *args, **kwargs):
        if db_field.name == 'choice':
            kwargs['widget'] = widgets.AdminTextInputWidget({'id': 'admin-form-control', 'class': 'form-control', 'placeholder': 'One of the quiz choices'})
        return super(QuizChoiceInLine, self).formfield_for_dbfield(db_field, *args, **kwargs)

class QuizAdmin(admin.ModelAdmin):
    """
    the admin view for creating and editing quizzes, including quiz chocies
    """
    inlines = [QuizChoiceInLine]
    form = QuizAdminForm

class QuizProxy(Quiz):
    # need proxy model since django admin does not allow a model to be registered twice
    class Meta:
        proxy = True
        verbose_name = "Quiz Result"
        verbose_name_plural = "Quiz Results"

class QuizChoiceResultsInLine(admin.StackedInline):
    # inline models of quiz results
    model = QuizChoice
    extra = 4
    min_num = 0
    fields = ('choice', 'times_chosen')
    readonly_fields = fields

    def has_add_permission(self, request, obj=None):
        return False

    def has_edit_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class QuizResultsAdmin(admin.ModelAdmin):
    """
    the admin view for displaying quiz results
    """
    inlines = [QuizChoiceResultsInLine]

    fields = ('question',)
    readonly_fields = fields

    def has_add_permission(self, request, obj=None):
        return False

    def has_edit_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class LectureAdmin(admin.ModelAdmin):
    form = LectureAdminForm


class UserProfileAdmin(admin.ModelAdmin):

    # should not be able to create or delete any, must be done in conjunction with User model
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    # once user profile has been made, you should not be able to change the FK
    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.exclude = ('user',)
        return super(UserProfileAdmin, self).change_view(request, object_id, form_url, extra_context)

    def changelist_view(self, request, extra_context=None):
        if not request.user.is_superuser:
            return redirect(reverse('admin:%s_%s_change' % (self.model._meta.app_label, self.model._meta.model_name), args=(request.user.UserProfile.id,)))
        return super(UserProfileAdmin, self).changelist_view(request=request, extra_context=extra_context)

class WordcloudAdmin(admin.ModelAdmin):
    form = WordcloudAdminForm
    
    def add_view(self, request, form_url='', extra_context=None):
        self.exclude = ('words',)
        return super(WordcloudAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.readonly_fields = ('words',)
        fieldsets = (
            ('Attributes', {
                'fields': ('title', 'Lecture', 'visible',)
            }),
            ('Input', {
                'readonly_fields': ('words',)
            }),
        )
        return super(WordcloudAdmin, self).change_view(request, object_id, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        # change parameter is flag for new object created or changing object, not if field has changed
        # if visible is flagged as False and there are words available, a wordcloud can be generated
        # need to gather all the words and generate the image
        # need to generate a new image if title also changes

        before_save_obj = Wordcloud.objects.get(id=obj.id)
        if (before_save_obj.visible == True and obj.visible == False) and obj.words:
            # if wordcloud changes from visible to not visible
            # and if there are words to process
            text = obj.words
            wc = WordCloud(font_path="static/app/fonts/Microsoft Sans Serif.ttf", width=800, height=400).generate(text)
            filepath = "wordcloud/"+ obj.title +".png"
            img = wc.to_image()
            img.save(settings.MEDIA_ROOT + "/" + filepath, 'PNG') # create the image file on filesystem
            obj.image = filepath # add the image to the model

        return super(WordcloudAdmin, self).save_model(request, obj, form, change)

class CodeSnippetAdmin(admin.ModelAdmin):
    form = CodeSnippetAdminForm

class PostsInLine(admin.StackedInline):
    model = Post
    exclude = ('rank',)
    min_num = 0
    extra = 0
    def formfield_for_dbfield(self, db_field, *args, **kwargs):
        if db_field.name == 'content':
            kwargs['widget'] = widgets.AdminTextareaWidget({'id': 'admin-form-control', 'class': 'form-control'})
        return super(PostsInLine, self).formfield_for_dbfield(db_field, *args, **kwargs)


class ThreadAdmin(admin.ModelAdmin):
    inlines = [PostsInLine]
    form = ThreadAdminForm

class Admin_Site(AdminSite):

    def index(self, request, extra_context=None):
        if not request.user.is_superuser:
            return redirect('index')
        else:
            return super(Admin_Site, self).index(request, extra_context)

    def app_index(self, request, app_label,extra_context=None):
        if not request.user.is_superuser:
            return redirect('index')
        else:
            return super(Admin_Site, self).app_index(request, app_label, extra_context)

adminsite = Admin_Site()


adminsite.register(User, CustomUserAdmin)
adminsite.register(UserProfile, UserProfileAdmin)
adminsite.register(Quiz, QuizAdmin)
adminsite.register(QuizProxy, QuizResultsAdmin)
adminsite.register(Lecture, LectureAdmin)
adminsite.register(Wordcloud, WordcloudAdmin)
adminsite.register(CodeSnippet, CodeSnippetAdmin)
adminsite.register(Thread, ThreadAdmin)


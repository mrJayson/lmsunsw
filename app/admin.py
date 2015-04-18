"""
Customizations for the Django administration interface
"""
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from app.models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils import six
from django.apps import apps
from app.forms import LectureAdminForm, QuizAdminForm, WordcloudAdminForm, QuizChoiceInLineForm, CodeSnippetAdminForm
from app.mixins import ModelAdminMixin, LimitedModelAdminMixin
from django.contrib.admin import widgets
from wordcloud import WordCloud
from lmsunsw.settings import MEDIA_ROOT

###################################################################################################

# Admin settings for staff

class DefaultUserAdmin(ModelAdminMixin, UserAdmin):
    list_display = ('username','email', 'first_name', 'last_name')

    def add_view(self, request, form_url='', extra_context=None):
        return super(DefaultUserAdmin, self).add_view(request, form_url, extra_context, default_admin_site)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        return super(DefaultUserAdmin, self).change_view(request, object_id, form_url, extra_context, default_admin_site)

    def delete_view(self, request, object_id, extra_context=None):
        return super(DefaultUserAdmin, self).delete_view(request, object_id, extra_context, default_admin_site)

    def changelist_view(self, request, extra_context=None):
        return super(DefaultUserAdmin, self).changelist_view(request=request, extra_context=extra_context, admin_site=default_admin_site)

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

class QuizAdmin(ModelAdminMixin, admin.ModelAdmin):
    """
    the admin view for creating and editing quizzes, including quiz chocies
    """
    inlines = [QuizChoiceInLine]
    form = QuizAdminForm

    def add_view(self, request, form_url='', extra_context=None):
        return super(QuizAdmin, self).add_view(request, form_url, extra_context, default_admin_site)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        return super(QuizAdmin, self).change_view(request, object_id, form_url, extra_context, default_admin_site)

    def delete_view(self, request, object_id, extra_context=None):
        return super(QuizAdmin, self).delete_view(request, object_id, extra_context, default_admin_site)

    def changelist_view(self, request, extra_context=None):
        return super(QuizAdmin, self).changelist_view(request=request, extra_context=extra_context, admin_site=default_admin_site)

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

class QuizResultsAdmin(ModelAdminMixin, admin.ModelAdmin):
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

    def add_view(self, request, form_url='', extra_context=None):
        return super(QuizResultsAdmin, self).add_view(request, form_url, extra_context, default_admin_site)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        return super(QuizResultsAdmin, self).change_view(request, object_id, form_url, extra_context, default_admin_site)

    def delete_view(self, request, object_id, extra_context=None):
        return super(QuizResultsAdmin, self).delete_view(request, object_id, extra_context, default_admin_site)

    def changelist_view(self, request, extra_context=None):
        return super(QuizResultsAdmin, self).changelist_view(request=request, extra_context=extra_context, admin_site=default_admin_site)


class LectureAdmin(ModelAdminMixin, admin.ModelAdmin):
    form = LectureAdminForm

    def add_view(self, request, form_url='', extra_context=None):
        return super(LectureAdmin, self).add_view(request, form_url, extra_context, default_admin_site)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        return super(LectureAdmin, self).change_view(request, object_id, form_url, extra_context, default_admin_site)

    def delete_view(self, request, object_id, extra_context=None):
        return super(LectureAdmin, self).delete_view(request, object_id, extra_context, default_admin_site)

    def changelist_view(self, request, extra_context=None):
        return super(LectureAdmin, self).changelist_view(request=request, extra_context=extra_context, admin_site=default_admin_site)


class UserProfileAdmin(ModelAdminMixin, admin.ModelAdmin):

    def add_view(self, request, form_url='', extra_context=None):
        return super(UserProfileAdmin, self).add_view(request, form_url, extra_context, default_admin_site)

    # once user profile has been made, you should not be able to change the FK
    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.exclude = ('user',)
        return super(UserProfileAdmin, self).change_view(request, object_id, form_url, extra_context, default_admin_site)

    def delete_view(self, request, object_id, extra_context=None):
        return super(UserProfileAdmin, self).delete_view(request, object_id, extra_context, default_admin_site)

    def changelist_view(self, request, extra_context=None):
        return super(UserProfileAdmin, self).changelist_view(request=request, extra_context=extra_context, admin_site=default_admin_site)

class WordcloudAdmin(ModelAdminMixin, admin.ModelAdmin):
    form = WordcloudAdminForm
    

    def add_view(self, request, form_url='', extra_context=None):
        self.exclude = ('words',)
        return super(WordcloudAdmin, self).add_view(request, form_url, extra_context, default_admin_site)

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
        return super(WordcloudAdmin, self).change_view(request, object_id, form_url, extra_context, default_admin_site)

    def delete_view(self, request, object_id, extra_context=None):
        return super(WordcloudAdmin, self).delete_view(request, object_id, extra_context, default_admin_site)

    def changelist_view(self, request, extra_context=None):
        return super(WordcloudAdmin, self).changelist_view(request=request, extra_context=extra_context, admin_site=default_admin_site)

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
            img.save(MEDIA_ROOT + "/" + filepath, 'PNG') # create the image file on filesystem
            obj.image = filepath # add the image to the model

        return super(WordcloudAdmin, self).save_model(request, obj, form, change)

class CodeSnippetAdmin(ModelAdminMixin, admin.ModelAdmin):
    form = CodeSnippetAdminForm

    def add_view(self, request, form_url='', extra_context=None):
        return super(CodeSnippetAdmin, self).add_view(request, form_url, extra_context, default_admin_site)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        return super(CodeSnippetAdmin, self).change_view(request, object_id, form_url, extra_context, default_admin_site)

    def delete_view(self, request, object_id, extra_context=None):
        return super(CodeSnippetAdmin, self).delete_view(request, object_id, extra_context, default_admin_site)

    def changelist_view(self, request, extra_context=None):
        return super(CodeSnippetAdmin, self).changelist_view(request=request, extra_context=extra_context, admin_site=default_admin_site)


class DefaultAdminSite(AdminSite):

    def app_list(self, request):
        app_dict = {}
        user = request.user
        for model, model_admin in self._registry.items():
            app_label = model._meta.app_label
            has_module_perms = user.has_module_perms(app_label)
            if has_module_perms:
                perms = model_admin.get_model_perms(request)
                # Check whether user has any perm for this module.
                # If so, add the module to the model_list.
                if True in perms.values():
                    info = (app_label, model._meta.model_name)
                    model_dict = {
                        'name': capfirst(model._meta.verbose_name_plural),
                        'object_name': model._meta.object_name,
                        'perms': perms,
                    }
                    if perms.get('change', False):
                        try:
                            model_dict['admin_url'] = reverse('admin:%s_%s_changelist' % info, current_app=self.name)
                        except NoReverseMatch:
                            pass
                    if perms.get('add', False):
                        try:
                            model_dict['add_url'] = reverse('admin:%s_%s_add' % info, current_app=self.name)
                        except NoReverseMatch:
                            pass
                    if app_label in app_dict:
                        app_dict[app_label]['models'].append(model_dict)
                    else:
                        app_dict[app_label] = {
                            'name': apps.get_app_config(app_label).verbose_name,
                            'app_label': app_label,
                            'app_url': reverse('admin:app_list', kwargs={'app_label': app_label}, current_app=self.name),
                            'has_module_perms': has_module_perms,
                            'models': [model_dict],
                        }
        # Sort the apps alphabetically.
        app_list = list(six.itervalues(app_dict))
        app_list.sort(key=lambda x: x['name'].lower())
        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: x['name'])
        return app_list

default_admin_site = DefaultAdminSite()

default_admin_site.register(User, DefaultUserAdmin)
default_admin_site.register(UserProfile, UserProfileAdmin)
default_admin_site.register(Quiz, QuizAdmin)
default_admin_site.register(QuizProxy, QuizResultsAdmin)
default_admin_site.register(Lecture, LectureAdmin)
default_admin_site.register(Wordcloud, WordcloudAdmin)
default_admin_site.register(CodeSnippet, CodeSnippetAdmin)



#######################################################################

# Admin settings for students

class UserAdminSite(AdminSite):

    def has_permission(self, request):
        # Removed check for is_staff.
        return request.user.is_active

class UserAdminLimited(UserAdmin):

    fieldsets = ((None, {'fields': ('username', 'password')}),(_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),)

    list_display = ('username',)
    list_filter = ()

    def get_queryset(self, request):
        """Limit object instances shown to only those owned by the current user"""
        qs = super(UserAdminLimited, self).get_queryset(request)
        return qs.filter(id=request.user.id)

class UserProfileAdminLimited(admin.ModelAdmin):

    # once user profile has been made, you should not be able to change the FK
    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.exclude = ('user',)
        return super(UserProfileAdminLimited, self).change_view(request, object_id, form_url, extra_context)

    def get_queryset(self, request):
        """all standard users are staff, and superuser is admin, if staff user"""
        
        qs = super(UserProfileAdminLimited, self).get_queryset(request)
        """Limit object instances shown to only those owned by the current user"""
        return qs.filter(user=request.user.id)



user_admin_site = UserAdminSite(name='useradmin')

user_admin_site.register(User, UserAdminLimited)
user_admin_site.register(UserProfile, UserProfileAdminLimited)




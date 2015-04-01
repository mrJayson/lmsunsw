"""
Customizations for the Django administration interface
"""
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from app.models import *
from fluent_contents.admin import PlaceholderFieldAdmin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

#######################################################################

# Admin settings for staff

class QuizChoiceInLine(admin.TabularInline):
    model = QuizChoice
    min_num = 2
    extra = 2

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuizChoiceInLine]

class LectureAdmin(PlaceholderFieldAdmin):
    pass

class UserProfileAdmin(PlaceholderFieldAdmin):

    # once user profile has been made, you should not be able to change the FK
    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.exclude = ('user',)
        return super(UserProfileAdmin, self).change_view(request, object_id, form_url, extra_context)

    def get_queryset(self, request):
        """all standard users are staff, and superuser is admin, if staff user"""
        
        qs = super(UserProfileAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            """superuser has access to all object instances"""
            return qs
        else:
            """Limit object instances shown to only those owned by the current user"""
            return qs.filter(user=request.user.id)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Lecture, LectureAdmin)

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


user_admin_site = UserAdminSite(name='useradmin')

user_admin_site.register(User, UserAdminLimited)
user_admin_site.register(UserProfile, UserProfileAdmin)


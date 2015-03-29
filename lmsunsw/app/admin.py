"""
Customizations for the Django administration interface
"""

from django.contrib import admin
from app.models import *
from fluent_contents.admin import PlaceholderFieldAdmin

class QuizChoiceInLine(admin.TabularInline):
    model = QuizChoice
    min_num = 2
    extra = 2

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuizChoiceInLine]

class CollabDocAdmin(PlaceholderFieldAdmin):
    pass

admin.site.register(UserProfile)
#admin.site.register(Lecture)
admin.site.register(Quiz, QuizAdmin)
'''admin.site.register(QuizChoice)'''
admin.site.register(Lecture, CollabDocAdmin)


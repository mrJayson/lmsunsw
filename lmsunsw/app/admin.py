"""
Customizations for the Django administration interface
"""

from django.contrib import admin
from app.models import *

class QuizChoiceInLine(admin.TabularInline):
    model = QuizChoice
    min_num = 2
    extra = 2

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuizChoiceInLine]

admin.site.register(UserProfile)
admin.site.register(Lecture)
admin.site.register(Quiz, QuizAdmin)
'''admin.site.register(QuizChoice)'''


"""
Customizations for the Django administration interface
"""

from django.contrib import admin
from app.models import *

admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(UserProfile)

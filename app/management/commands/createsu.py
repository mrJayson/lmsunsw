from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
	# this function adds a command to python manage.py
	# call this function with python manage.py createsu
	def handle(self, *args, **options):
		if not User.objects.filter(username="admin").exists():
			User.objects.create_superuser("admin", "admin@admin.com", "password")
		if not User.objects.filter(username="jasonhuang").exists():
			User.objects.create_superuser("jasonhuang", "jason@huang.com", "password")
		if not User.objects.filter(username="sherylshi").exists():
			User.objects.create_superuser("sherylshi", "sheryl@shi.com", "password")
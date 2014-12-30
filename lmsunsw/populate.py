import os
os.environ.setdefault('DJANGO_SETTING_MODULE', 'lmsunsw.setting')

import django
django.setup()

from app.models import *


VERBOSE = True

def clear():
    print "Clearing database"
    User.objects.all().delete()
    UserProfile.objects.all().delete()
    Class.objects.all().delete()
    django.contrib.sessions.models.Session.objects.all().delete()

def populate():
    print "Populating database"
    add_class("COMP1917", "Higher Computing 1")
    add_user("JasonHuang", "Jason", "Huang", "jh@jh.com", "password1", True)
    add_user("student", "stu", "dent", "stu@dent.com", "password1", False)

def add_user(username, first_name, last_name, email, password, is_staff):
    user=User.objects.create_user(username=username, email=email,  password=password)
    user.first_name = first_name
    user.last_name = last_name
    user.is_staff = is_staff

    user.save()
    return user

def add_class(class_name, class_description):
    c = Class.objects.get_or_create(class_name=class_name, class_description=class_description)[0]
    return c

def run():
    clear()
    populate()

if __name__ == '__main__':
    run()
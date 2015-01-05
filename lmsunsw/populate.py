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
    Course.objects.all().delete()
    Lecture.objects.all().delete()

    # remove all user sessions
    django.contrib.sessions.models.Session.objects.all().delete()


def populate():
    print "Populating database"
    
    add_user("admin", "", "", "", "password", True, True)
    u = add_user("Lecturer", "Mr", "Lecturer", "lecturer@lecture.com", "password", True, False)
    add_user("student", "stu", "dent", "stu@dent.com", "password", False, False)
    add_course("COMP1917", "Higher Computing 1", "Beginning Computing For advanced students", u)

def add_user(username, first_name, last_name, email, password, is_staff, is_superuser):
    new_user = User.objects.create_user(username=username, email=email,  password=password)
    new_user.first_name = first_name
    new_user.last_name = last_name
    new_user.is_staff = is_staff
    new_user.is_superuser = is_superuser
    new_user.save()
    # create accompanying entry for additional user data
    new_user_profile, created = UserProfile.objects.get_or_create(user=new_user)
    assert created

    return new_user

def add_course(course_code, course_name, course_description, course_head_lecturer):
    course, created = Course.objects.get_or_create(course_code=course_code, course_name=course_name, course_description=course_description, course_head_lecturer=course_head_lecturer)
    assert created
    return course

def run():
    clear()
    populate()

if __name__ == '__main__':
    run()
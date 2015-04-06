import sys
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lmsunsw.settings")

from app.models import *
from docsURL import glist
from random import choice
from string import ascii_lowercase

class Rand():

    @staticmethod
    def randomString(n):
        return ''.join(choice(list(ascii_lowercase)) for _ in xrange(n))

    @staticmethod
    def randomBool():
        return choice([True,False])

    @staticmethod
    def randomInt(n):
        return choice(xrange(n))


    @staticmethod
    def lecture(lecture_name=None, lecture_slide=None, collab_doc=None):
        lecture_name = Rand.randomString(10) if lecture_name==None else lecture_name
        lecture_slide = Rand.randomString(10) if lecture_slide==None else lecture_slide
        collab_doc = Rand.randomString(10) if collab_doc==None else collab_doc
        return Lecture.objects.create(lecture_name=lecture_name, lecture_slide=lecture_slide, collab_doc=collab_doc)

    @staticmethod
    def quiz(question=None, visible=None, lecture=None):
        question = Rand.randomString(10) if question==None else question
        visible = Rand.randomBool() if visible==None else visible
        lecture = (Rand.lecture() if (len(Lecture.objects.all())==0) else choice(Lecture.objects.all())) if lecture==None else lecture
        return Quiz.objects.create(question=question, visible=visible, Lecture=lecture) 

    @staticmethod
    def quizchoice(quiz_choice=None, quiz=None, correct=None):
        quiz_choice = Rand.randomString(10) if quiz_choice==None else quiz_choice
        quiz = (Rand.quiz() if (len(Quiz.objects.all())==0) else choice(Quiz.objects.all())) if quiz==None else quiz
        correct = Rand.randomBool() if correct==None else correct
        return QuizChoice.objects.create(choice=quiz_choice, Quiz=quiz, correct=correct)

    @staticmethod
    def user(username=None, first_name=None, last_name=None, email=None, password=None):
        username = Rand.randomString(10) if username==None else username
        first_name = Rand.randomString(10) if first_name==None else first_name
        last_name = Rand.randomString(10) if last_name==None else last_name
        email = Rand.randomString(10)+"@"+Rand.randomString(5)+"."+Rand.randomString(3) if email==None else email
        password = Rand.randomString(10) if password==None else password
        return User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email, password=password)

    @staticmethod
    def quizchoiceselected(user=None, quizchoice=None):
        user = (Rand.user() if (len(User.objects.all())==0) else choice(User.objects.all())) if user==None else user
        quizchoice = (Rand.quizchoice() if (len(QuizChoice.objects.all())==0) else choice(QuizChoice.objects.all())) if quizchoice==None else quizchoice
        return QuizChoiceSelected.objects.create(User=user, QuizChoice=quizchoice)

    @staticmethod
    def confidence(user=None, confidence=None):
        user = (Rand.user() if (len(User.objects.all())==0) else choice(User.objects.all())) if user==None else user
        confidence = choice([1,0,-1])
        obj, created = ConfidenceMeter.objects.get_or_create(User=user)
        if not created:
            obj.user = user
            obj.confidence = confidence
            obj.save()
        return obj


VERBOSE = True

def clear():
    print "Clearing database"
    User.objects.all().delete()
    UserProfile.objects.all().delete()
    Lecture.objects.all().delete()
    Quiz.objects.all().delete()
    QuizChoice.objects.all().delete()
    QuizChoiceSelected.objects.all().delete()
    ConfidenceMeter.objects.all().delete()


    # remove all user sessions
    # django.contrib.sessions.models.Session.objects.all().delete()

def revote():
    Rand.confidence(user=User.objects.all()[0])
    Rand.confidence(user=User.objects.all()[1])
    Rand.confidence(user=User.objects.all()[2])
    Rand.confidence(user=User.objects.all()[3])
    Rand.confidence(user=User.objects.all()[4])
    Rand.confidence(user=User.objects.all()[5])
    Rand.confidence(user=User.objects.all()[6])
    Rand.confidence(user=User.objects.all()[7])
    Rand.confidence(user=User.objects.all()[8])
    Rand.confidence(user=User.objects.all()[9])
    Rand.confidence(user=User.objects.all()[10])
    Rand.confidence(user=User.objects.all()[11])
    Rand.confidence(user=User.objects.all()[12])
    Rand.confidence(user=User.objects.all()[13])
    Rand.confidence(user=User.objects.all()[14])
    Rand.confidence(user=User.objects.all()[15])
    Rand.confidence(user=User.objects.all()[16])
    Rand.confidence(user=User.objects.all()[17])
    Rand.confidence(user=User.objects.all()[18])
    Rand.confidence(user=User.objects.all()[19])


def populate():
    print "Populating database"

    create_superuser("admin", "administration", "account", "admin@admin.com", "admin")
    create_student("Jack", "Jack", "James", "Jack@James.com", "password")
    Rand.user()
    Rand.user()
    Rand.user()
    Rand.user()
    Rand.user()
    Rand.user()
    Rand.user()
    Rand.user()
    Rand.user()
    Rand.user()

    Rand.user()
    Rand.user()
    Rand.user()
    Rand.user()
    Rand.user()
    Rand.user()
    Rand.user()
    Rand.user()
    Rand.user()
    Rand.user()
    revote()
    
    lecture1 = create_lecture("Lecture 1")
    lecture2 = create_lecture("Lecture 2")
    lecture3 = create_lecture("Lecture 3")

    quiz1 = create_quiz("What colour is the sky?", True, lecture1)
    create_quiz_choice("Red", quiz1, False)
    create_quiz_choice("Blue", quiz1, True)
    create_quiz_choice("Green", quiz1, False)
    create_quiz_choice("Purple", quiz1, False)

    quiz2 = create_quiz("What is the Capital of Australia?", True, lecture2)
    create_quiz_choice("London", quiz2, False)
    create_quiz_choice("Beijing", quiz2, False)
    create_quiz_choice("Sydney", quiz2, False)
    create_quiz_choice("New York", quiz2, False)
    create_quiz_choice("Canberra", quiz2, True)

    quiz3 = create_quiz("Which side of the road do Australians drive on?", True, lecture2)
    create_quiz_choice("Left", quiz3, True)
    create_quiz_choice("Right", quiz3, False)

    quiz4 = create_quiz("Which one of these translates a high level language to machine code?", True, lecture3)
    create_quiz_choice("Assembler", quiz4, False)
    create_quiz_choice("Modem", quiz4, False)
    create_quiz_choice("Compiler", quiz4, True)
    create_quiz_choice("Computer", quiz4, False)

    quiz5 = create_quiz("What is the fourth layer of the OSI model?", True, lecture3)
    create_quiz_choice("Network", quiz5, False)
    create_quiz_choice("Transport", quiz5, True)
    create_quiz_choice("Data Link", quiz5, False)
    create_quiz_choice("Physical", quiz5, False)

    quiz6 = create_quiz("Where is America Located?", True, lecture2)
    create_quiz_choice("Northern Hemisphere", quiz6, True)
    create_quiz_choice("Southern Hemisphere", quiz6, False)
    create_quiz_choice("Western Hemisphere", quiz6, True)
    create_quiz_choice("Eastern Hemisphere", quiz6, False)

    quiz6 = create_quiz("What is your favourite colour?", True, lecture3)
    create_quiz_choice("Orange", quiz6, False)
    create_quiz_choice("Red", quiz6, False)
    create_quiz_choice("Green", quiz6, False)
    create_quiz_choice("None of the above", quiz6, False)



def create_user(username, first_name, last_name, email, password, is_superuser):
    """
    Set all users' is_staff to True to be able to access all of the django admin features
    """

    sys.stdout.write("creating user... ")
    new_user = User.objects.create_user(username=username, email=email,  password=password)
    new_user.first_name = first_name
    new_user.last_name = last_name
    new_user.is_staff = True
    new_user.is_superuser = is_superuser
    if is_superuser == False:
        new_user.user_permissions.add(Permission.objects.get(name='Can change user'), Permission.objects.get(name='Can change user profile')) 
    new_user.save()
    # create accompanying entry for additional user data
    new_user_profile, created = UserProfile.objects.get_or_create(user=new_user)
    print "success" if created else "failed"
    assert created

    return new_user

def create_student(username, first_name, last_name, email, password):
    return create_user(username, first_name, last_name, email, password, False)

def create_superuser(username, first_name, last_name, email, password):
    return create_user(username, first_name, last_name, email, password, True)

def create_lecture(lecture_name):
    sys.stdout.write("creating lecture... ")
    new_lecture, created = Lecture.objects.get_or_create(lecture_name=lecture_name)
    #new_lecture.save()
    print "success" if created else "failed"
    assert created
    return new_lecture

def create_quiz(question, visible, Lecture):
    sys.stdout.write("creating quiz... ")
    new_quiz, created = Quiz.objects.get_or_create(question=question, visible=visible, Lecture=Lecture)
    print "success" if created else "failed"
    assert created
    return new_quiz

def create_quiz_choice(choice, Quiz, correct):
    sys.stdout.write("creating quiz_choice... ")
    new_quiz_choice, created = QuizChoice.objects.get_or_create(choice=choice, Quiz=Quiz, correct=correct)
    print "success" if created else "failed"
    assert created
    return new_quiz_choice

def run():
    clear()
    populate()

if __name__ == '__main__':
    print "Starting population script"
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lmsunsw.settings')
    import django
    django.setup()
    from django.contrib.auth.models import Permission
    from app.models import *
    run()
import sys
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lmsunsw.settings')
import django
django.setup()
from app.models import *

from app.models import *
from app.docsURL import glist
from random import choice
from string import ascii_lowercase

verbose_populate = True
# print for each object creation if verbose is True


first_names = ['Annie', 'Adam', 'Becky', 'Bert', 'Chris', 'Christina', 'David', 'Danielle', 'Edison', 'Ellie', 
    'Frank', 'Faye', 'Graham', 'Gwen', 'Harvey', 'Haley', 'Isaac', 'Isabella', 'Jason', 'Jessica', 
    'Keith', 'Katelyn', 'Luke', 'Lynette', 'Morgan', 'Mandy', 'Neil', 'Natalie', 'Oliver', 'Olivia', 
    'Peter', 'Penny', 'Quentin', 'Quinzel', 'Robert', 'Rachel', 'Simon', 'Sheryl', 'Todd', 'Tanya', 
    'Ulysses', 'Una', 'Victor', 'Vivian', 'Wilson', 'Wendy', 'Xaiver', 'Xana', 'Young', 'Yvonne', 'Zach', 'Zoe']

last_names = ['Anderson', 'Baker', 'Caffrey', 'Denistone', 'Ervine', 'Freeman', 'Gray', 'Haynes', 'Irwin', 
    'Jefferson', 'Kendrick', 'Lance', 'Macklin', 'Noble', 'Owen', 'Palmer', 'Queen', 'Reynolds', 'Smith', 
    'Tanner', 'Underwood', 'Valentine', 'West', 'Xander', 'York', 'Zimmer']

class Rand():

    @staticmethod
    def randomString(n):
        return ''.join(choice(list(ascii_lowercase+" ")) for _ in xrange(n))

    @staticmethod
    def randomBool():
        return choice([True,False])

    @staticmethod
    def randomInt(n):
        return choice(xrange(n))


    @staticmethod
    def lecture(title=None, collab_doc=None):
        title = Rand.randomString(10) if title==None else title
        collab_doc = Lecture.get_unused_gdoc() if collab_doc==None else collab_doc
        return Lecture.objects.create(title=title, collab_doc=collab_doc)

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
    def user(username=None, first_name=None, last_name=None, email=None, password=None, is_superuser=False):
        while True:
            first_name = choice(first_names) if first_name==None else first_name
            last_name = choice(last_names) if last_name==None else last_name
            username = (first_name+last_name).lower() if username==None else username.lower()
            if User.objects.filter(username=username).exists():
                first_name = None
                last_name = None
                username = None
            else:
                break
        
        email = first_name+"@"+last_name+".com" if email==None else email
        password = "password" if password==None else password
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        user.is_staff = True
        user.is_superuser = is_superuser
        user.save()
        return user

    @staticmethod
    def quizchoiceselected(user=None, quizchoice=None):
        while True:
            user = (Rand.user() if (len(User.objects.all())==0) else choice(User.objects.all())) if user==None else user
            quizchoice = (Rand.quizchoice() if (len(QuizChoice.objects.all())==0) else choice(QuizChoice.objects.all())) if quizchoice==None else quizchoice
            if QuizChoiceSelected.objects.filter(User=user, QuizChoice=quizchoice).exists():
                user = None
                quizchoice = None
            else:
                break
        return QuizChoiceSelected.objects.create(User=user, QuizChoice=quizchoice)

    @staticmethod
    def confidence(user=None, confidence=None):
        user = (Rand.user() if (len(User.objects.all())==0) else choice(User.objects.all())) if user==None else user
        confidence = choice([1,0,-1])
        obj, created = ConfidenceMeter.objects.get_or_create(User=user)
        obj.confidence = confidence
        obj.save()
        return obj

    @staticmethod
    def thread(title=None, content=None, Creator=None, views=None, anonymous=None):
        title = Rand.randomString(20) if title==None else title
        content = Rand.randomString(100) if content==None else content
        Creator = (Rand.user() if (len(User.objects.all())==0) else choice(User.objects.all())) if Creator==None else Creator
        views = Rand.randomInt(100) if views==None else views
        anonymous = Rand.randomBool() if anonymous==None else anonymous
        return Thread.objects.create(title=title, content=content, Creator=Creator, views=views, anonymous=anonymous)

    @staticmethod
    def post(thread=None, content=None, Creator=None, anonymous=None):
        thread = (Rand.thread() if (len(Thread.objects.all())==0) else choice(Thread.objects.all())) if thread==None else thread
        content = Rand.randomString(200) if content==None else content
        Creator = (Rand.user() if (len(User.objects.all())==0) else choice(User.objects.all())) if Creator==None else Creator
        rank = thread.replies
        anonymous = Rand.randomBool() if anonymous==None else anonymous
        return Post.objects.create(Thread=thread, content=content, Creator=Creator, rank=rank, anonymous=anonymous)

def create_user(username=None, first_name=None, last_name=None, email=None, password=None, is_superuser=None):
    """
    Set all users' is_staff to True to be able to access all of the django admin features
    """
    new_user = Rand.user(username=username, first_name=first_name, last_name=last_name, email=email,  password=password, is_superuser=is_superuser)

    if 'verbose_populate' in globals() and verbose_populate == True:
        print "created user: " + new_user.username
    return new_user

def create_student(username=None, first_name=None, last_name=None, email=None, password=None):
    return create_user(username, first_name, last_name, email, password, False)

def create_superuser(username=None, first_name=None, last_name=None, email=None, password=None):
    return create_user(username, first_name, last_name, email, password, True)

def create_lecture(title=None):
    
    new_lecture = Rand.lecture(title=title)
    if 'verbose_populate' in globals() and verbose_populate == True:
        print "created lecture: " + new_lecture.title
    return new_lecture

def create_quiz(question=None, visible=None, Lecture=None):
    
    new_quiz = Rand.quiz(question, visible, Lecture)
    if 'verbose_populate' in globals() and verbose_populate == True:
        print "created quiz: " + new_quiz.question
    return new_quiz

def create_quiz_choice(choice=None, Quiz=None, correct=None):
    
    new_quiz_choice = Rand.quizchoice(quiz_choice=choice, quiz=Quiz, correct=correct)
    if 'verbose_populate' in globals() and verbose_populate == True:
        print "created quiz_choice: " + new_quiz_choice.choice
    return new_quiz_choice

def create_quiz_choice_selection(User=None, Quiz_Choice=None, Quiz=None):
    if Quiz_Choice == None and Quiz != None:
        Quiz_Choice = choice(QuizChoice.objects.filter(Quiz=Quiz))
    new_quiz_choice_selection = Rand.quizchoiceselected(user=User, quizchoice=Quiz_Choice)
    if 'verbose_populate' in globals() and verbose_populate == True:
        print "create quiz_choice_selection: User '"+ new_quiz_choice_selection.User.username + "' voted '" + new_quiz_choice_selection.QuizChoice.choice + "' for " + new_quiz_choice_selection.QuizChoice.Quiz.question
    return new_quiz_choice_selection

def create_thread(title=None, content=None, Creator=None, views=None, anonymous=None):
    
    new_thread = Rand.thread(title, content, Creator, views)
    if 'verbose_populate' in globals() and verbose_populate == True:
        print "created thread: " + new_thread.title
    return new_thread

def create_post(Thread=None, content=None, Creator=None, anonymous=None):
    
    new_post = Rand.post(Thread, content, Creator)
    if 'verbose_populate' in globals() and verbose_populate == True:
        print "created post: " + new_post.content
    return new_post


def clear():
    print "Clearing database"
    User.objects.all().delete()
    UserProfile.objects.all().delete()
    Lecture.objects.all().delete()
    Quiz.objects.all().delete()
    QuizChoice.objects.all().delete()
    QuizChoiceSelected.objects.all().delete()
    ConfidenceMeter.objects.all().delete()
    Thread.objects.all().delete()
    Post.objects.all().delete()
    CodeSnippet.objects.all().delete()
    # remove all user sessions
    django.contrib.sessions.models.Session.objects.all().delete()

def vote():
    for user in User.objects.all():
        Rand.confidence(user=user)
        

def populate():


    print "Populating database"

    create_superuser(username="admin", first_name="administration", last_name="account", email="admin@admin.com", password="admin")
    create_student(username="Jack", first_name="Jack", last_name="James", email="Jack@James.com", password="password")
    num_students = 50

    for i in xrange(num_students):
        u = create_student()
        u.UserProfile.confidence_message = Rand.randomString(10)
        u.UserProfile.save()

    vote()
    
    lecture1 = create_lecture("Lecture 1")
    lecture2 = create_lecture("Lecture 2")
    lecture3 = create_lecture("Lecture 3")
    lecture4 = create_lecture("Lecture 4")
    lecture5 = create_lecture("Lecture 5")
    lecture6 = create_lecture("Lecture 6")
    lecture7 = create_lecture("Lecture 7")
    lecture7 = create_lecture("Week 11 Lecture 1")

    quiz0 = create_quiz("Rate Assignment 1 a", True, lecture7)
    qc_1 = create_quiz_choice("1", quiz0, False)
    qc_2 = create_quiz_choice("2", quiz0, False)
    qc_3 = create_quiz_choice("3", quiz0, False)
    qc_4 = create_quiz_choice("4", quiz0, False)
    qc_5 = create_quiz_choice("5", quiz0, False)
    qc_6 = create_quiz_choice("6", quiz0, False)
    qc_7 = create_quiz_choice("7", quiz0, False)
    qc_8 = create_quiz_choice("8", quiz0, False)
    qc_9 = create_quiz_choice("9", quiz0, False)
    qc_10 = create_quiz_choice("10", quiz0, False)
    qc_11 = create_quiz_choice("11", quiz0, False)
    qc_12 = create_quiz_choice("12", quiz0, False)
    qc_13 = create_quiz_choice("13", quiz0, False)
    qc_14 = create_quiz_choice("14", quiz0, False)
    qc_15 = create_quiz_choice("15", quiz0, False)
    qc_16 = create_quiz_choice("16", quiz0, False)
    qc_17 = create_quiz_choice("17", quiz0, False)
    qc_18 = create_quiz_choice("18", quiz0, False)
    qc_19 = create_quiz_choice("19", quiz0, False)
    qc_20 = create_quiz_choice("20", quiz0, False)

    ans = [qc_17,qc_18,qc_17,qc_16,qc_15,qc_15,qc_16,qc_19,qc_20,
    qc_20,qc_17,qc_18,qc_15,qc_15,qc_17,qc_17,qc_16,qc_18,qc_17,
    qc_19,qc_20,qc_18,qc_16,qc_16,qc_18,qc_19,qc_16,qc_13,qc_16,
    qc_17,qc_17,qc_17,qc_18,qc_16,qc_14,qc_14,qc_17,qc_17,qc_17,
    qc_18,qc_19,qc_16,qc_17,qc_17,qc_18,qc_17,qc_17,qc_18,qc_16,
    qc_16,qc_16,qc_16]
    
    i = 0
    for user in User.objects.all():
        print i
        create_quiz_choice_selection(Quiz=quiz0, User=user, Quiz_Choice=ans[i])
        i = i + 1

    quiz1 = create_quiz("What colour is the sky?", False, lecture1)
    create_quiz_choice("Red", quiz1, False)
    create_quiz_choice("Blue", quiz1, True)
    create_quiz_choice("Green", quiz1, False)
    create_quiz_choice("Purple", quiz1, False)

    quiz2 = create_quiz("What is the Capital of Australia?", False, lecture7)
    create_quiz_choice("London", quiz2, False)
    create_quiz_choice("Beijing", quiz2, False)
    create_quiz_choice("Sydney", quiz2, False)
    create_quiz_choice("New York", quiz2, False)
    create_quiz_choice("Canberra", quiz2, True)

    quiz3 = create_quiz("Which side of the road do Australians drive on?", False, lecture7)
    create_quiz_choice("Left", quiz3, True)
    create_quiz_choice("Right", quiz3, False)

    quiz4 = create_quiz("Which one of these translates a high level language to machine code?", False, lecture6)
    create_quiz_choice("Assembler", quiz4, False)
    create_quiz_choice("Modem", quiz4, False)
    create_quiz_choice("Compiler", quiz4, True)
    create_quiz_choice("Computer", quiz4, False)

    quiz5 = create_quiz("What is the fourth layer of the OSI model?", False, lecture6)
    create_quiz_choice("Network", quiz5, False)
    create_quiz_choice("Transport", quiz5, True)
    create_quiz_choice("Data Link", quiz5, False)
    create_quiz_choice("Physical", quiz5, False)

    quiz6 = create_quiz("Where is America Located?", False, lecture7)
    create_quiz_choice("Northern Hemisphere", quiz6, True)
    create_quiz_choice("Southern Hemisphere", quiz6, False)
    create_quiz_choice("Western Hemisphere", quiz6, True)
    create_quiz_choice("Eastern Hemisphere", quiz6, False)

    quiz7 = create_quiz("What is your favourite colour?", False, lecture6)
    create_quiz_choice("Orange", quiz7, False)
    create_quiz_choice("Red", quiz7, False)
    create_quiz_choice("Green", quiz7, False)
    create_quiz_choice("None of the above", quiz7, False)

    quiz8 = create_quiz("Which was created first?", False, lecture6)
    create_quiz_choice("Google", quiz8, False)
    create_quiz_choice("TV", quiz8, False)
    create_quiz_choice("Iphone", quiz8, False)
    create_quiz_choice("Radio", quiz8, True)

    quiz9 = create_quiz("Where in memory is the heap located?", True, lecture7)
    create_quiz_choice("In lower memory addresses", quiz9, True)
    create_quiz_choice("In middle memory addresses", quiz9, False)
    create_quiz_choice("In bottom memory addresses", quiz9, False)
    create_quiz_choice("In random memory addresses", quiz9, False)


    for user in User.objects.all():
        create_quiz_choice_selection(Quiz=quiz1, User=user)
        create_quiz_choice_selection(Quiz=quiz2, User=user)
        create_quiz_choice_selection(Quiz=quiz3, User=user)
        create_quiz_choice_selection(Quiz=quiz4, User=user)
        create_quiz_choice_selection(Quiz=quiz6, User=user)
        create_quiz_choice_selection(Quiz=quiz8, User=user)

    for i in xrange(num_students * 3):
        create_quiz_choice_selection()

    for i in xrange(10):
        create_thread(anonymous=False)
    for i in xrange(100):
        create_post(anonymous=False)
    

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
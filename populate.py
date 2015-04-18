import sys
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lmsunsw.settings')
import django
django.setup()
from django.contrib.auth.models import Permission
from app.models import *

from app.models import *
from app.docsURL import glist
from random import choice
from string import ascii_lowercase

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
    def lecture(lecture_name=None, lecture_slide=None, collab_doc=None):
        lecture_name = Rand.randomString(10) if lecture_name==None else lecture_name
        collab_doc = Lecture.get_unused_gdoc() if collab_doc==None else collab_doc
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
    def user(username=None, first_name=None, last_name=None, email=None, password=None, is_superuser=False):
        username = Rand.randomString(10) if username==None else username
        first_name = Rand.randomString(10) if first_name==None else first_name
        last_name = Rand.randomString(10) if last_name==None else last_name
        email = Rand.randomString(10)+"@"+Rand.randomString(5)+"."+Rand.randomString(3) if email==None else email
        password = Rand.randomString(10) if password==None else password
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        user.is_staff = True
        user.is_superuser = is_superuser
        user.save()
        return user

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

    @staticmethod
    def thread(title=None, Creator=None, views=None):
        title = Rand.randomString(40) if title==None else title
        Creator = (Rand.user() if (len(User.objects.all())==0) else choice(User.objects.all())) if Creator==None else Creator
        views = Rand.randomInt(100) if views==None else views
        return Thread.objects.create(title=title, Creator=Creator, views=views)

    @staticmethod
    def post(thread=None, content=None, Creator=None):
        thread = (Rand.thread() if (len(Thread.objects.all())==0) else choice(Thread.objects.all())) if thread==None else thread
        content = Rand.randomString(40) if content==None else content
        Creator = (Rand.user() if (len(User.objects.all())==0) else choice(User.objects.all())) if Creator==None else Creator
        rank = thread.replies
        return Post.objects.create(Thread=thread, content=content, Creator=Creator, rank=rank)

    @staticmethod
    def wordcloud(title=None, image=None, lecture=None, visible=None):
        title = Rand.randomString(5) if title==None else title
        # cannot generate rand image
        image = None if image==None else image
        lecture = (Rand.lecture() if (len(Lecture.objects.all())==0) else choice(Lecture.objects.all())) if lecture==None else lecture
        visible = Rand.randomBool() if visible==None else visible
        return Wordcloud.objects.create(title=title, image=image, Lecture=lecture, visible=visible)

    @staticmethod
    def wordcloudsubmission(user=None, wordcloud=None, word=None):

        user = (Rand.user() if (len(User.objects.all())==0) else choice(User.objects.all())) if user==None else user
        wordcloud = (Rand.wordcloud() if (len(Wordcloud.objects.all())==0) else choice(Wordcloud.objects.all())) if wordcloud==None else wordcloud
        while WordcloudSubmission.objects.filter(User=user, Wordcloud=wordcloud).exists():
            # reset both vars so forced to choose another random combination
            user=None
            wordcloud=None

            user = (Rand.user() if (len(User.objects.all())==0) else choice(User.objects.all())) if user==None else user
            wordcloud = (Rand.wordcloud() if (len(Wordcloud.objects.all())==0) else choice(Wordcloud.objects.all())) if wordcloud==None else wordcloud

        word = Rand.randomString(1) if word==None else word

        return WordcloudSubmission.objects.create(User=user, Wordcloud=wordcloud, word=word)

def create_user(username=None, first_name=None, last_name=None, email=None, password=None, is_superuser=None):
    """
    Set all users' is_staff to True to be able to access all of the django admin features
    """
    print "creating user... "
    new_user = Rand.user(username=username, first_name=first_name, last_name=last_name, email=email,  password=password, is_superuser=is_superuser)
    if is_superuser == False:
        new_user.user_permissions.add(
            Permission.objects.get(name='Can change user'),
            Permission.objects.get(name='Can change user profile'),
            Permission.objects.get(name='Can add thread'),
            Permission.objects.get(name='Can change thread'),
            Permission.objects.get(name='Can add post'),
            Permission.objects.get(name='Can change post'),
        ) 
    new_user.save()
    # create accompanying entry for additional user data
    new_user_profile, created = UserProfile.objects.get_or_create(user=new_user)
    return new_user

def create_student(username=None, first_name=None, last_name=None, email=None, password=None):
    return create_user(username, first_name, last_name, email, password, False)

def create_superuser(username=None, first_name=None, last_name=None, email=None, password=None):
    return create_user(username, first_name, last_name, email, password, True)

def create_lecture(lecture_name=None):
    print "creating lecture... "
    return Rand.lecture(lecture_name=lecture_name)

def create_quiz(question=None, visible=None, Lecture=None):
    print "creating quiz... "
    return Rand.quiz(question, visible, Lecture)

def create_quiz_choice(choice=None, Quiz=None, correct=None):
    print "creating quiz_choice... "
    return Rand.quizchoice(quiz_choice=choice, quiz=Quiz, correct=correct)

def create_thread(title=None, Creator=None, views=None):
    print "creating thread... "
    return Rand.thread(title, Creator, views)

def create_post(Thread=None, content=None, Creator=None):
    print "creating post... "
    return Rand.post(Thread, content, Creator)

def create_wordcloud(title=None, image=None, Lecture=None, visible=None):
    print "creating wordcloud..."
    return Rand.wordcloud(title, image, Lecture, visible)

def create_wordcloudsubmission(User=None, Wordcloud=None, word=None):
    print "creating wordcloud submission..."
    return Rand.wordcloudsubmission(user=User, wordcloud=Wordcloud, word=word)

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
    Wordcloud.objects.all().delete()
    WordcloudSubmission.objects.all().delete()
    # remove all user sessions
    django.contrib.sessions.models.Session.objects.all().delete()

def vote(n):
    for i in xrange(n):
        Rand.confidence(user=User.objects.all()[i])

def populate():
    print "Populating database"

    create_superuser(username="admin", first_name="administration", last_name="account", email="admin@admin.com", password="admin")
    create_student(username="Jack", first_name="Jack", last_name="James", email="Jack@James.com", password="password")
    num_students = 50
    for i in xrange(num_students):
        create_student()

    vote(num_students)
    
    lecture1 = create_lecture("Lecture 1")
    lecture2 = create_lecture("Lecture 2")
    lecture3 = create_lecture("Lecture 3")

    quiz1 = create_quiz("What colour is the sky?", False, lecture1)
    create_quiz_choice("Red", quiz1, False)
    create_quiz_choice("Blue", quiz1, True)
    create_quiz_choice("Green", quiz1, False)
    create_quiz_choice("Purple", quiz1, False)

    quiz2 = create_quiz("What is the Capital of Australia?", False, lecture2)
    create_quiz_choice("London", quiz2, False)
    create_quiz_choice("Beijing", quiz2, False)
    create_quiz_choice("Sydney", quiz2, False)
    create_quiz_choice("New York", quiz2, False)
    create_quiz_choice("Canberra", quiz2, True)

    quiz3 = create_quiz("Which side of the road do Australians drive on?", False, lecture2)
    create_quiz_choice("Left", quiz3, True)
    create_quiz_choice("Right", quiz3, False)

    quiz4 = create_quiz("Which one of these translates a high level language to machine code?", False, lecture3)
    create_quiz_choice("Assembler", quiz4, False)
    create_quiz_choice("Modem", quiz4, False)
    create_quiz_choice("Compiler", quiz4, True)
    create_quiz_choice("Computer", quiz4, False)

    quiz5 = create_quiz("What is the fourth layer of the OSI model?", False, lecture3)
    create_quiz_choice("Network", quiz5, False)
    create_quiz_choice("Transport", quiz5, True)
    create_quiz_choice("Data Link", quiz5, False)
    create_quiz_choice("Physical", quiz5, False)

    quiz6 = create_quiz("Where is America Located?", False, lecture2)
    create_quiz_choice("Northern Hemisphere", quiz6, True)
    create_quiz_choice("Southern Hemisphere", quiz6, False)
    create_quiz_choice("Western Hemisphere", quiz6, True)
    create_quiz_choice("Eastern Hemisphere", quiz6, False)

    quiz6 = create_quiz("What is your favourite colour?", False, lecture3)
    create_quiz_choice("Orange", quiz6, False)
    create_quiz_choice("Red", quiz6, False)
    create_quiz_choice("Green", quiz6, False)
    create_quiz_choice("None of the above", quiz6, False)

    quiz7 = create_quiz("Which was created first?", False, lecture3)
    create_quiz_choice("Google", quiz7, False)
    create_quiz_choice("TV", quiz7, False)
    create_quiz_choice("Iphone", quiz7, False)
    create_quiz_choice("Radio", quiz7, True)

    thread1 = create_thread()
    thread2 = create_thread()
    thread3 = create_thread()
    for i in xrange(5):
        create_thread()
    for i in xrange(num_students):
        create_post()
    
    wc = create_wordcloud(title="What is your favourite Colour?", visible=True)

    words = ['Red', 'Blue', 'Green', 'Orange', 'Yellow', 'Purple', 'Cyan', 'Magenta', 'Crimson']
    for i in xrange(num_students):
        create_wordcloudsubmission(Wordcloud=wc, word=choice(words))

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
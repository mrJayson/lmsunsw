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

verbose = True
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

        while True:
            user = (Rand.user() if (len(User.objects.all())==0) else choice(User.objects.all())) if user==None else user
            wordcloud = (Rand.wordcloud() if (len(Wordcloud.objects.all())==0) else choice(Wordcloud.objects.all())) if wordcloud==None else wordcloud
            if WordcloudSubmission.objects.filter(User=user, Wordcloud=wordcloud).exists():
                user=None
                wordcloud=None
            else:
                break

        word = Rand.randomString(1) if word==None else word

        return WordcloudSubmission.objects.create(User=user, Wordcloud=wordcloud, word=word)

def create_user(username=None, first_name=None, last_name=None, email=None, password=None, is_superuser=None):
    """
    Set all users' is_staff to True to be able to access all of the django admin features
    """
    
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
    if 'verbose' in locals() and verbose == True:
        print "created user: " + new_user.username
    return new_user

def create_student(username=None, first_name=None, last_name=None, email=None, password=None):
    return create_user(username, first_name, last_name, email, password, False)

def create_superuser(username=None, first_name=None, last_name=None, email=None, password=None):
    return create_user(username, first_name, last_name, email, password, True)

def create_lecture(lecture_name=None):
    
    new_lecture = Rand.lecture(lecture_name=lecture_name)
    if 'verbose' in locals() and verbose == True:
        print "created lecture: " + new_lecture.lecture_name
    return new_lecture

def create_quiz(question=None, visible=None, Lecture=None):
    
    new_quiz = Rand.quiz(question, visible, Lecture)
    if 'verbose' in locals() and verbose == True:
        print "created quiz: " + new_quiz.question
    return new_quiz

def create_quiz_choice(choice=None, Quiz=None, correct=None):
    
    new_quiz_choice = Rand.quizchoice(quiz_choice=choice, quiz=Quiz, correct=correct)
    if 'verbose' in locals() and verbose == True:
        print "created quiz_choice: " + new_quiz_choice.choice
    return new_quiz_choice

def create_quiz_choice_selection(User=None, Quiz_Choice=None, Quiz=None):
    if Quiz_Choice == None and Quiz != None:
        Quiz_Choice = choice(QuizChoice.objects.filter(Quiz=Quiz))
    new_quiz_choice_selection = Rand.quizchoiceselected(user=User, quizchoice=Quiz_Choice)
    if 'verbose' in locals() and verbose == True:
        print "create quiz_choice_selection: User '"+ new_quiz_choice_selection.User.username + "' voted '" + new_quiz_choice_selection.QuizChoice.choice + "' for " + new_quiz_choice_selection.QuizChoice.Quiz.question
    return new_quiz_choice_selection

def create_thread(title=None, content=None, Creator=None, views=None, anonymous=None):
    
    new_thread = Rand.thread(title, content, Creator, views)
    if 'verbose' in locals() and verbose == True:
        print "created thread: " + new_thread.title
    return new_thread

def create_post(Thread=None, content=None, Creator=None, anonymous=None):
    
    new_post = Rand.post(Thread, content, Creator)
    if 'verbose' in locals() and verbose == True:
        print "created post: " + new_post.content
    return new_post

def create_wordcloud(title=None, image=None, Lecture=None, visible=None):
    
    new_wordcloud = Rand.wordcloud(title, image, Lecture, visible)
    if 'verbose' in locals() and verbose == True:
        print "created wordcloud: " + new_wordcloud.title
    return new_wordcloud

def create_wordcloud_submission(User=None, Wordcloud=None, word=None):
    
    new_wordcloud_submission = Rand.wordcloudsubmission(user=User, wordcloud=Wordcloud, word=word)
    if 'verbose' in locals() and verbose == True:
        print "created wordcloud submission: " + new_wordcloud_submission.word
    return new_wordcloud_submission

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
    num_students = 100

    for i in xrange(num_students):
        create_student()

    vote()
    
    lecture1 = create_lecture("Lecture 1")
    lecture2 = create_lecture("Lecture 2")
    lecture3 = create_lecture("Lecture 3")

    quiz1 = create_quiz("What colour is the sky?", False, lecture1)
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

    quiz7 = create_quiz("Which was created first?", True, lecture3)
    create_quiz_choice("Google", quiz7, False)
    create_quiz_choice("TV", quiz7, False)
    create_quiz_choice("Iphone", quiz7, False)
    create_quiz_choice("Radio", quiz7, True)

    for i in xrange(10):
        create_quiz_choice_selection(Quiz=quiz1)
        create_quiz_choice_selection(Quiz=quiz2)

    #for i in xrange(num_students * 3):
    #    create_quiz_choice_selection()

    for i in xrange(5):
        create_thread(anonymous=False)
    for i in xrange(num_students):
        create_post(anonymous=False)
    
    wc = create_wordcloud(title="What is your favourite Colour?", visible=True)
    words = ['Red', 'Blue', 'Green', 'Orange', 'Yellow', 'Purple', 'Cyan', 'Magenta', 'Crimson']
    for i in xrange(num_students):
        create_wordcloud_submission(User=User.objects.all()[i], Wordcloud=wc, word=choice(words))

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
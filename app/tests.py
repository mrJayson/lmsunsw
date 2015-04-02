from django.test import TestCase
from app.models import *
from docsURL import glist
from random import choice
from string import ascii_lowercase

# Create your tests here.

class Rand():


	@staticmethod
	def lecture(lecture_name=None, lecture_slide=None, collab_doc=None):
		lecture_name = Rand.randomString(10) if lecture_name==None else lecture_name
		lecture_slide = Rand.randomString(10) if lecture_slide==None else lecture_slide
		collab_doc = Rand.randomString(10) if collab_doc==None else collab_doc
		return Lecture.objects.get_or_create(lecture_name=lecture_name, lecture_slide=lecture_slide, collab_doc=collab_doc)

	@staticmethod
	def quiz(question=None, visible=None, lecture=None):
		question = Rand.randomString(10) if question==None else question
		visible = Rand.randomBool() if visible==None else visible
		lecture = (Rand.lecture() if (len(Lecture.objects.all())==0) else choice(Lecture.objects.all())) if lecture==None else lecture
		return Quiz.objects.create(question=question, visible=visible, Lecture=lecture)	

	@staticmethod
	def quizchoice(choice=None, quiz=None, correct=None):
		choice = Rand.randomString(10) if choice==None else choice
		quiz = (Rand.quiz() if (len(Quiz.objects.all())==0) else choice(Quiz.objects.all())) if quiz==None else quiz
		correct = Rand.randomBool() if correct==None else correct
		return QuizChoice.objects.create(choice=choice, Quiz=quiz, correct=correct)

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
		return QuizChoice.objects.create(User=user, QuizChoice=quizchoice)

	@staticmethod
	def randomString(n):
		return ''.join(choice(list(ascii_lowercase)) for _ in xrange(n))

	@staticmethod
	def randomBool():
		return choice([True,False])

	@staticmethod
	def randomInt(n):
		return choice(xrange(n))


class Lecture_Model(TestCase):
	
	def setUp(self):
		Lecture.objects.create(lecture_name="Lecture 1")
		Lecture.objects.create(lecture_name="Lecture 2")
		Lecture.objects.create(lecture_name="Lecture 3", lecture_slide="A")
		Lecture.objects.create(lecture_name="Lecture 4")
		Lecture.objects.create(lecture_name="Lecture 5")
		Lecture.objects.create(lecture_name="Lecture 6")
		Lecture.objects.create(lecture_name="Lecture 7")
		Lecture.objects.create(lecture_name="Lecture 8")
		Lecture.objects.create(lecture_name="Lecture 9")
		Lecture.objects.create(lecture_name="Lecture 10")

	def test_correct_attr(self):
		#check name is inserted correctly
		self.assertEquals(Lecture.objects.get(id=1).lecture_name, "Lecture 1")
		self.assertEquals(Lecture.objects.get(id=2).lecture_name, "Lecture 2")
		self.assertEquals(Lecture.objects.get(id=3).lecture_name, "Lecture 3")
		self.assertEquals(Lecture.objects.get(id=4).lecture_name, "Lecture 4")
		self.assertEquals(Lecture.objects.get(id=5).lecture_name, "Lecture 5")
		self.assertEquals(Lecture.objects.get(id=6).lecture_name, "Lecture 6")
		self.assertEquals(Lecture.objects.get(id=7).lecture_name, "Lecture 7")
		self.assertEquals(Lecture.objects.get(id=8).lecture_name, "Lecture 8")
		self.assertEquals(Lecture.objects.get(id=9).lecture_name, "Lecture 9")
		self.assertEquals(Lecture.objects.get(id=10).lecture_name, "Lecture 10")
		#check for 
		self.assertEquals(Lecture.objects.get(id=1).lecture_slide, None)
		self.assertEquals(Lecture.objects.get(id=2).lecture_slide, None)
		self.assertEquals(Lecture.objects.get(id=3).lecture_slide, "A")
		self.assertEquals(Lecture.objects.get(id=4).lecture_slide, None)
		self.assertEquals(Lecture.objects.get(id=5).lecture_slide, None)
		self.assertEquals(Lecture.objects.get(id=6).lecture_slide, None)
		self.assertEquals(Lecture.objects.get(id=7).lecture_slide, None)
		self.assertEquals(Lecture.objects.get(id=8).lecture_slide, None)
		self.assertEquals(Lecture.objects.get(id=9).lecture_slide, None)
		self.assertEquals(Lecture.objects.get(id=10).lecture_slide, None)

		for i, item in enumerate(min(glist, Lecture.objects.all())):
			self.assertEquals(glist[i], Lecture.objects.get(id=i+1).collab_doc)

class Quiz_Model(TestCase):
	def setUp(self):
		l1 = Lecture.objects.create(lecture_name="Lecture 1")
		q1 = Quiz.objects.create(question="question", visible=True, Lecture=l1)
		QuizChoice.objects.create(choice="choice", Quiz=q1, correct=True)
		QuizChoice.objects.create(choice="choice", Quiz=q1, correct=True)

		l2 = Lecture.objects.create(lecture_name="Lecture 2")
		q2 = Quiz.objects.create(question="question", visible=False, Lecture=l2)
		QuizChoice.objects.create(choice="choice", Quiz=q2, correct=True)
		QuizChoice.objects.create(choice="choice", Quiz=q2, correct=True)
		QuizChoice.objects.create(choice="choice", Quiz=q2, correct=True)

		l3 = Lecture.objects.create(lecture_name="Lecture 3")
		q3 = Quiz.objects.create(question="question", visible=True, Lecture=l3)
		QuizChoice.objects.create(choice="choice", Quiz=q3, correct=True)
		QuizChoice.objects.create(choice="choice", Quiz=q3, correct=True)
		QuizChoice.objects.create(choice="choice", Quiz=q3, correct=True)
		QuizChoice.objects.create(choice="choice", Quiz=q3, correct=True)

		l4 = Lecture.objects.create(lecture_name="Lecture 4")
		q4 = Quiz.objects.create(question="question", visible=False, Lecture=l4)
		QuizChoice.objects.create(choice="choice", Quiz=q4, correct=True)
		QuizChoice.objects.create(choice="choice", Quiz=q4, correct=True)
		QuizChoice.objects.create(choice="choice", Quiz=q4, correct=True)
		QuizChoice.objects.create(choice="choice", Quiz=q4, correct=True)
		QuizChoice.objects.create(choice="choice", Quiz=q4, correct=True)


	def test_correct_attr(self):
		self.assertEquals(Quiz.objects.get(id=1).question, "question")
		self.assertEquals(Quiz.objects.get(id=2).question, "question")
		self.assertEquals(Quiz.objects.get(id=3).question, "question")
		self.assertEquals(Quiz.objects.get(id=4).question, "question")

		self.assertEquals(Quiz.objects.get(id=1).visible, True)
		self.assertEquals(Quiz.objects.get(id=2).visible, False)
		self.assertEquals(Quiz.objects.get(id=3).visible, True)
		self.assertEquals(Quiz.objects.get(id=4).visible, False)

		self.assertEquals(len(QuizChoice.objects.filter(Quiz=1)), 2)
		self.assertEquals(len(QuizChoice.objects.filter(Quiz=2)), 3)
		self.assertEquals(len(QuizChoice.objects.filter(Quiz=3)), 4)
		self.assertEquals(len(QuizChoice.objects.filter(Quiz=4)), 5)

class Quiz_Usage(TestCase):
	def setUp(self):
		l1 = Rand.lecture()
		q1 = Rand.quiz()
		for i in xrange(4):
			Rand.quizchoice(quiz=q1)
		for i in xrange(10):
			Rand.user()

		answers = [1,1,2,3,4,3,4,3,4,4]

		for i in xrange(10):
			QuizChoiceSelected.objects.create(User=User.objects.get(id=i+1), QuizChoice=QuizChoice.objects.get(id=answers[i]))

	def test_usage(self):
		self.assertEquals(QuizChoice.objects.get(id=1).times_chosen, 2)
		self.assertEquals(QuizChoice.objects.get(id=2).times_chosen, 1)
		self.assertEquals(QuizChoice.objects.get(id=3).times_chosen, 3)
		self.assertEquals(QuizChoice.objects.get(id=4).times_chosen, 4)



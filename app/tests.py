from django.test import TestCase
from app.models import *
from django.db import IntegrityError
from populate import Rand

# Create your tests here.

class User_Case(TestCase):

	def setUp(self):
		User.objects.create(username="AAA", first_name="A", last_name="A", email="A@test.com", password="A", is_superuser=True)
		User.objects.create(username="BBB", first_name="B", last_name="B", email="B@test.com", password="B", is_superuser=True)
		User.objects.create(username="CCC", first_name="C", last_name="C", email="C@test.com", password="C", is_superuser=False)
		User.objects.create(username="DDD", first_name="D", last_name="D", email="D@test.com", password="D", is_superuser=False)
		User.objects.create(username="EEE", first_name="E", last_name="E", email="E@test.com", password="E", is_superuser=True)
		User.objects.create(username="FFF", first_name="F", last_name="F", email="F@test.com", password="F", is_superuser=False)
		User.objects.create(username="GGG", first_name="G", last_name="G", email="G@test.com", password="G", is_superuser=False)
		User.objects.create(username="HHH", first_name="H", last_name="H", email="H@test.com", password="H", is_superuser=True)
		User.objects.create(username="III", first_name="I", last_name="I", email="I@test.com", password="I", is_superuser=False)
		User.objects.create(username="JJJ", first_name="J", last_name="J", email="J@test.com", password="J", is_superuser=False)
		User.objects.create(username="KKK", first_name="K", last_name="K", email="K@test.com", password="K", is_superuser=False)

	def test_correct_attr(self):
		self.assertEquals(User.objects.get(id=1).username, "A")
		self.assertEquals(User.objects.get(id=2).username, "B")
		self.assertEquals(User.objects.get(id=3).username, "C")
		self.assertEquals(User.objects.get(id=4).username, "D")
		self.assertEquals(User.objects.get(id=5).username, "E")
		self.assertEquals(User.objects.get(id=6).username, "F")
		self.assertEquals(User.objects.get(id=7).username, "G")
		self.assertEquals(User.objects.get(id=8).username, "H")
		self.assertEquals(User.objects.get(id=9).username, "I")
		self.assertEquals(User.objects.get(id=10).username, "J")
		self.assertEquals(User.objects.get(id=11).username, "K")

		self.assertEquals(User.objects.get(id=1).first_name, "A")
		self.assertEquals(User.objects.get(id=2).first_name, "B")
		self.assertEquals(User.objects.get(id=3).first_name, "C")
		self.assertEquals(User.objects.get(id=4).first_name, "D")
		self.assertEquals(User.objects.get(id=5).first_name, "E")
		self.assertEquals(User.objects.get(id=6).first_name, "F")
		self.assertEquals(User.objects.get(id=7).first_name, "G")
		self.assertEquals(User.objects.get(id=8).first_name, "H")
		self.assertEquals(User.objects.get(id=9).first_name, "I")
		self.assertEquals(User.objects.get(id=10).first_name, "J")
		self.assertEquals(User.objects.get(id=11).first_name, "K")

		self.assertEquals(User.objects.get(id=1).last_name, "A")
		self.assertEquals(User.objects.get(id=2).last_name, "B")
		self.assertEquals(User.objects.get(id=3).last_name, "C")
		self.assertEquals(User.objects.get(id=4).last_name, "D")
		self.assertEquals(User.objects.get(id=5).last_name, "E")
		self.assertEquals(User.objects.get(id=6).last_name, "F")
		self.assertEquals(User.objects.get(id=7).last_name, "G")
		self.assertEquals(User.objects.get(id=8).last_name, "H")
		self.assertEquals(User.objects.get(id=9).last_name, "I")
		self.assertEquals(User.objects.get(id=10).last_name, "J")
		self.assertEquals(User.objects.get(id=11).last_name, "K")

		self.assertEquals(User.objects.get(id=1).email, "A@test.com")
		self.assertEquals(User.objects.get(id=2).email, "B@test.com")
		self.assertEquals(User.objects.get(id=3).email, "C@test.com")
		self.assertEquals(User.objects.get(id=4).email, "D@test.com")
		self.assertEquals(User.objects.get(id=5).email, "E@test.com")
		self.assertEquals(User.objects.get(id=6).email, "F@test.com")
		self.assertEquals(User.objects.get(id=7).email, "G@test.com")
		self.assertEquals(User.objects.get(id=8).email, "H@test.com")
		self.assertEquals(User.objects.get(id=9).email, "I@test.com")
		self.assertEquals(User.objects.get(id=10).email, "J@test.com")
		self.assertEquals(User.objects.get(id=11).email, "K@test.com")

		self.assertEquals(User.objects.get(id=1).password, "A")
		self.assertEquals(User.objects.get(id=2).password, "B")
		self.assertEquals(User.objects.get(id=3).password, "C")
		self.assertEquals(User.objects.get(id=4).password, "D")
		self.assertEquals(User.objects.get(id=5).password, "E")
		self.assertEquals(User.objects.get(id=6).password, "F")
		self.assertEquals(User.objects.get(id=7).password, "G")
		self.assertEquals(User.objects.get(id=8).password, "H")
		self.assertEquals(User.objects.get(id=9).password, "I")
		self.assertEquals(User.objects.get(id=10).password, "J")
		self.assertEquals(User.objects.get(id=11).password, "K")

		self.assertEquals(User.objects.get(id=1).is_superuser, True)
		self.assertEquals(User.objects.get(id=2).is_superuser, True)
		self.assertEquals(User.objects.get(id=3).is_superuser, False)
		self.assertEquals(User.objects.get(id=4).is_superuser, False)
		self.assertEquals(User.objects.get(id=5).is_superuser, True)
		self.assertEquals(User.objects.get(id=6).is_superuser, False)
		self.assertEquals(User.objects.get(id=7).is_superuser, False)
		self.assertEquals(User.objects.get(id=8).is_superuser, True)
		self.assertEquals(User.objects.get(id=9).is_superuser, False)
		self.assertEquals(User.objects.get(id=10).is_superuser, False)
		self.assertEquals(User.objects.get(id=11).is_superuser, False)



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

	def test_correct_attr(self):
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

	def test_multimcq_integrity(self):
		choices = ['a','b','c','d']
		for i in xrange(len(choices)):
			Rand.quizchoice(quiz_choice=choices[i])

		u = Rand.user()
		for i in xrange(len(choices)):
			
			error_occured = False
			try:
				Rand.quizchoiceselected(quizchoice=QuizChoice.objects.get(id=i+1))
				Rand.quizchoiceselected(quizchoice=QuizChoice.objects.get(id=i+1))
			except Exception:
				error_occured = True
			self.assertTrue(error_occured)


class Quiz_Usage(TestCase):

	def test_usage(self):

		for i in xrange(4):
			Rand.quizchoice()

		answers = [1,1,2,3,4,3,4,3,4,4]
		for i in xrange(len(answers)):
			Rand.user()
		

		for i in xrange(len(answers)):
			Rand.quizchoiceselected(user=User.objects.get(id=i+1), quizchoice=QuizChoice.objects.get(id=answers[i]))

		self.assertEquals(QuizChoice.objects.get(id=1).times_chosen, 2)
		self.assertEquals(QuizChoice.objects.get(id=2).times_chosen, 1)
		self.assertEquals(QuizChoice.objects.get(id=3).times_chosen, 3)
		self.assertEquals(QuizChoice.objects.get(id=4).times_chosen, 4)

	def test_quiz_type1(self):
		correct = [False, False, False, False]
		for i in xrange(4):
			Rand.quizchoice(correct=correct[i])
		self.assertEquals(Quiz.objects.first().quiz_type, QuizType.ZEROMCQ)

	def test_quiz_type2(self):
		correct = [True, False, False, False]
		for i in xrange(4):
			Rand.quizchoice(correct=correct[i])
		self.assertEquals(Quiz.objects.first().quiz_type, QuizType.SINGLEMCQ)

	def test_quiz_type3(self):
		correct = [True, True, False, False]
		for i in xrange(4):
			Rand.quizchoice(correct=correct[i])
		self.assertEquals(Quiz.objects.first().quiz_type, QuizType.MULTIMCQ)

	def test_quiz_type4(self):
		correct = [True, True, True, False]
		for i in xrange(4):
			Rand.quizchoice(correct=correct[i])
		self.assertEquals(Quiz.objects.first().quiz_type, QuizType.MULTIMCQ)

	def test_quiz_type5(self):
		correct = [True, True, True, True]
		for i in xrange(4):
			Rand.quizchoice(correct=correct[i])
		self.assertEquals(Quiz.objects.first().quiz_type, QuizType.MULTIMCQ)



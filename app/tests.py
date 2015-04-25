from django.test import TestCase, RequestFactory, Client
from django.core.urlresolvers import reverse
from app.models import *
from django.db import IntegrityError
from populate import *
from app.docsURL import glist
from app.views import *
from app.class_based_views import *

# Create your tests here.

class User_Case(TestCase):

	def setUp(self):
		User.objects.create(username="AAA", first_name="A", last_name="A", email="A@test.com", password="A", is_superuser=True)
		User.objects.create(username="BBB", first_name="B", last_name="B", email="B@test.com", password="B", is_superuser=True)
		User.objects.create(username="CCC", first_name="C", last_name="C", email="C@test.com", password="C", is_superuser=True)
		User.objects.create(username="DDD", first_name="D", last_name="D", email="D@test.com", password="D", is_superuser=True)
		User.objects.create(username="EEE", first_name="E", last_name="E", email="E@test.com", password="E", is_superuser=True)
		User.objects.create(username="FFF", first_name="F", last_name="F", email="F@test.com", password="F", is_superuser=False)
		User.objects.create(username="GGG", first_name="G", last_name="G", email="G@test.com", password="G", is_superuser=False)
		User.objects.create(username="HHH", first_name="H", last_name="H", email="H@test.com", password="H", is_superuser=False)
		User.objects.create(username="III", first_name="I", last_name="I", email="I@test.com", password="I", is_superuser=False)
		User.objects.create(username="JJJ", first_name="J", last_name="J", email="J@test.com", password="J", is_superuser=False)
		User.objects.create(username="KKK", first_name="K", last_name="K", email="K@test.com", password="K", is_superuser=False)

	def test_correct_attr(self):
		self.assertEquals(User.objects.get(id=1).username, "AAA")
		self.assertEquals(User.objects.get(id=2).username, "BBB")
		self.assertEquals(User.objects.get(id=3).username, "CCC")
		self.assertEquals(User.objects.get(id=4).username, "DDD")
		self.assertEquals(User.objects.get(id=5).username, "EEE")
		self.assertEquals(User.objects.get(id=6).username, "FFF")
		self.assertEquals(User.objects.get(id=7).username, "GGG")
		self.assertEquals(User.objects.get(id=8).username, "HHH")
		self.assertEquals(User.objects.get(id=9).username, "III")
		self.assertEquals(User.objects.get(id=10).username, "JJJ")
		self.assertEquals(User.objects.get(id=11).username, "KKK")

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

		for i in xrange(1,5):
			self.assertEquals(User.objects.get(id=i).is_superuser, True)
		for n in xrange(6,11):
			self.assertEquals(User.objects.get(id=n).is_superuser, False)

class Forum_Post_New(TestCase):

	def setUp(self):
		u1 = User.objects.create(username="AAA", first_name="A", last_name="A", email="A@test.com", password="A", is_superuser=False)
		Thread.objects.create(title="Apple", content="Types of Fruit", Creator=u1, views=0, anonymous=False)

		u2 = User.objects.create(username="BBB", first_name="B", last_name="B", email="B@test.com", password="B", is_superuser=False)
		Thread.objects.create(title="Cars", content="Types of Cars", Creator=u2, views=0, anonymous=True)

		u3 = User.objects.create(username="CCC", first_name="C", last_name="C", email="C@test.com", password="C", is_superuser=False)
		Thread.objects.create(title="Class", content="Types of Class", Creator=u3, views=0, anonymous=False)

		u4 = User.objects.create(username="DDD", first_name="D", last_name="D", email="D@test.com", password="D", is_superuser=False)
		Thread.objects.create(title="Colour", content="Types of Colour", Creator=u4, views=0, anonymous=True)

		u5 = User.objects.create(username="EEE", first_name="E", last_name="E", email="E@test.com", password="E", is_superuser=True)
		Thread.objects.create(title="Books", content="Types of Books", Creator=u5, views=0, anonymous=False)


	def test_correct_attr(self):
		self.assertEquals(Thread.objects.get(id=1).title, "Apple")		
		self.assertEquals(Thread.objects.get(id=2).title, "Cars")		
		self.assertEquals(Thread.objects.get(id=3).title, "Class")		
		self.assertEquals(Thread.objects.get(id=4).title, "Colour")		
		self.assertEquals(Thread.objects.get(id=5).title, "Books")

		self.assertEquals(Thread.objects.get(id=1).content, "Types of Fruit")
		self.assertEquals(Thread.objects.get(id=2).content, "Types of Cars")		
		self.assertEquals(Thread.objects.get(id=3).content, "Types of Class")
		self.assertEquals(Thread.objects.get(id=4).content, "Types of Colour")
		self.assertEquals(Thread.objects.get(id=5).content, "Types of Books")

		for i in xrange(1,5):
			self.assertEquals(Thread.objects.get(id=i).Creator, User.objects.get(id=i))
		
		for x in xrange(1,5):
			self.assertEquals(Thread.objects.get(id=x).views, 0)

		self.assertEquals(Thread.objects.get(id=1).anonymous, False)		
		self.assertEquals(Thread.objects.get(id=2).anonymous, True)
		self.assertEquals(Thread.objects.get(id=3).anonymous, False)
		self.assertEquals(Thread.objects.get(id=4).anonymous, True)
		self.assertEquals(Thread.objects.get(id=5).anonymous, False)

		def test_correct_views(self):
		
			for i in xrange(1,5):
				Thread.objects.increment(Thread.objects.get(id=i).views)
				Thread.objects.increment(Thread.objects.get(id=i).views)
				Thread.objects.increment(Thread.objects.get(id=i).views)
				Thread.objects.increment(Thread.objects.get(id=i).views)

			for x in xrange(1,5):
				self.assertEquals(Thread.objects.get(id=x).views, 4)

class Forum_Thread_New(TestCase):

	def test_correct_attr(self):

		u1 = User.objects.create(username="AAA", first_name="A", last_name="A", email="A@test.com", password="A", is_superuser=True)
		u2 = User.objects.create(username="BBB", first_name="B", last_name="B", email="B@test.com", password="B", is_superuser=False)
		u3 = User.objects.create(username="CCC", first_name="C", last_name="C", email="C@test.com", password="C", is_superuser=False)
		u4 = User.objects.create(username="DDD", first_name="D", last_name="D", email="D@test.com", password="D", is_superuser=False)

		t1 = Thread.objects.create(title="Apple", content="Types of Fruit", Creator=u1, views=0, anonymous=False)
		Post.objects.create(Thread=t1, content="Apple", Creator=u2, rank=1, anonymous=False)
		Post.objects.create(Thread=t1, content="banana", Creator=u3, rank=1, anonymous=False)
		Post.objects.create(Thread=t1, content="orange", Creator=u4, rank=3, anonymous=False)

		t2 = Thread.objects.create(title="Chocolate", content="chocolate", Creator=u1, views=0, anonymous=False)
		Post.objects.create(Thread=t2, content="Volvo is a car brand", Creator=u2, rank=1, anonymous=True)
		Post.objects.create(Thread=t2, content="The question was types of Cars", Creator=u3, rank=2, anonymous=True)

		t3 = Thread.objects.create(title="Fruit", content="Banana", Creator=u2, views=0, anonymous=False)
		Post.objects.create(Thread=t3, content="Blue", Creator=u1, rank=1, anonymous=True)
		Post.objects.create(Thread=t3, content="Harry Potter", Creator=u2, rank=2, anonymous=True)
		Post.objects.create(Thread=t3, content="Oceans", Creator=u3, rank=3, anonymous=True)
		Post.objects.create(Thread=t3, content="Owls", Creator=u4, rank=4, anonymous=True)
		
		self.assertEquals(Thread.objects.get(id=1).title, "Apple")
		self.assertEquals(Thread.objects.get(id=2).title, "Chocolate")
		self.assertEquals(Thread.objects.get(id=3).title, "Fruit")

		for i in xrange(1,3):
			self.assertEquals(Post.objects.get(id=i).Thread, Thread.objects.get(id=1))

		self.assertEquals(Post.objects.get(id=4).Thread, Thread.objects.get(id=2))
		self.assertEquals(Post.objects.get(id=5).Thread, Thread.objects.get(id=2))

		for x in xrange(6,9):
			self.assertEquals(Post.objects.get(id=x).Thread, Thread.objects.get(id=3))

		self.assertEquals(Post.objects.get(id=1).content, "Apple")
		self.assertEquals(Post.objects.get(id=2).content, "banana")
		self.assertEquals(Post.objects.get(id=3).content, "orange")
		self.assertEquals(Post.objects.get(id=4).content, "Volvo is a car brand")
		self.assertEquals(Post.objects.get(id=5).content, "The question was types of Cars")
		self.assertEquals(Post.objects.get(id=6).content, "Blue")
		self.assertEquals(Post.objects.get(id=7).content, "Harry Potter")
		self.assertEquals(Post.objects.get(id=8).content, "Oceans")
		self.assertEquals(Post.objects.get(id=9).content, "Owls")

		self.assertEquals(Post.objects.get(id=1).Creator, User.objects.get(id=2))
		self.assertEquals(Post.objects.get(id=2).Creator, User.objects.get(id=3))
		self.assertEquals(Post.objects.get(id=3).Creator, User.objects.get(id=4))
		self.assertEquals(Post.objects.get(id=4).Creator, User.objects.get(id=2))
		self.assertEquals(Post.objects.get(id=5).Creator, User.objects.get(id=3))
		self.assertEquals(Post.objects.get(id=6).Creator, User.objects.get(id=1))
		self.assertEquals(Post.objects.get(id=7).Creator, User.objects.get(id=2))
		self.assertEquals(Post.objects.get(id=8).Creator, User.objects.get(id=3))
		self.assertEquals(Post.objects.get(id=9).Creator, User.objects.get(id=4))

		for n in xrange(1,3):
			self.assertEquals(Post.objects.get(id=n).anonymous, False)

		for m in xrange(4,9):
			self.assertEquals(Post.objects.get(id=m).anonymous, True)

class Lecture_Model(TestCase):
		

	def test_correct_attr(self):
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

	def test_glist(self):
		for g in glist:
			l = Rand.lecture()
			self.assertEquals(l.collab_doc, g)

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


class Get_Request(TestCase):

	def setUp(self):
		
		self.factory = RequestFactory()
		self.client = Client()
		self.user = User.objects.create(username="AAA", first_name="A", last_name="A", email="A@test.com", password="A", is_superuser=True)

	def test_index_view(self):
		# the request URL is what you type into the web browser.
		# look at urls.py for what the mappings are
		request = self.factory.get('/index')
		
		request.user = self.user
		view = IndexView.as_view()
		response = view(request)
		self.assertEquals(response.status_code, 200)

	def test_createuser_view(self):

		request = self.factory.get('/createuser')
		request.user = self.user
		view = CreateUser.as_view()
		response = view(request)
		self.assertEquals(response.status_code, 200)

	def test_alert_view(self):

		request = self.client.get('/alert/create_user_success')
		self.assertEquals(request.status_code, 200)
		'''
		self.kwargs['tag'] = "create_user_success"
		request = self.factory.get('/alert/', self)

		request.user = self.user
		view = AlertView.as_view()
		response = view(request)
		self.assertEquals(response.status_code, 200)
		'''

	def test_lecture_view(self):

		Lecture.objects.create(lecture_name="Lecture 1", lecture_slide="A")
		self.assertEquals(Lecture.objects.get(id=01).lecture_name, 'Lecture 1')

		request = self.client.get('/course/01/lecture-1')
		self.assertEquals(request.status_code, 302)
	

	def test_quiz_view(self):

		l1 = Lecture.objects.create(lecture_name="Lecture 1")
		q1 = Quiz.objects.create(question="question", visible=True, Lecture=l1)
		QuizChoice.objects.create(choice="choice", Quiz=q1, correct=True)
		
		request = self.client.get('/course/01/lecture-1/quiz/01/question')
		self.assertEquals(request.status_code, 302)


	def test_lecture_slide_view(self):

		Lecture.objects.create(lecture_name="Lecture 1", lecture_slide="A")
		
		request = self.client.get('/course/01/Lecture-1')
		self.assertEquals(request.status_code, 302)

	def test_thread_view_page(self):
		
		request = self.factory.get('/course')
		request.user = self.user
		view = ThreadView.as_view()
		response = view(request)
		self.assertEquals(response.status_code, 200)

	def test_create_thread_view(self):
		
		request = self.factory.get('/course')
		request.user = self.user
		view = CreateThreadView.as_view()
		response = view(request)
		self.assertEquals(response.status_code, 200)

	def test_post_view(self):
		
		t2 = Thread.objects.create(title="Chocolate", content="chocolate", Creator=self.user, views=0, anonymous=False)
		Post.objects.create(Thread=t2, content="Volvo is a car brand", Creator=self.user, rank=1, anonymous=True)

		request = self.client.get('/course/threads/01/chocolate')
		self.assertEquals(request.status_code, 302)

	def test_wordcloud(self):

		l1 = Lecture.objects.create(lecture_name="Lecture 1", lecture_slide="A")
		Wordcloud.objects.create(title="test", Lecture=l1, visible=True)

		request = self.client.get('/course/01/lecture-1/wordcloud/01/test')
		self.assertEquals(request.status_code, 302)

class Post_Request_Tests(TestCase):

	def setUp(self):
		self.client = Client()
		self.su = create_superuser(username="admin", first_name="administration", last_name="account", email="admin@admin.com", password="admin")
		#User.objects.create_user(username="AAA", first_name="A", last_name="A", email="A@test.com", password="A", is_superuser=True)
		self.u1 = create_user(username="BBB", first_name="B", last_name="b", email="b@test.com", password="b", is_superuser=False)	
		self.u2 = create_user(username="ccc", first_name="c", last_name="b", email="c@test.com", password="c", is_superuser=False)	
		self.l1 = Lecture.objects.create(lecture_name="Lecture 1", lecture_slide="A")
	

	def test_superuser_login(self):

		response = self.client.post('/login', {'username': 'admin', 'password': 'admin'})
		self.assertEquals(response.status_code, 302)
		self.assertRedirects(response, '/', status_code=302, target_status_code=302)

	def test_student_login(self):

		response = self.client.post('/login', {'username': 'bbb', 'password': 'b'})	
		self.assertEquals(response.status_code, 302)
		self.assertRedirects(response, '/', status_code=302, target_status_code=302)


		#self.assertEquals(request.status_code, 302)
		#self.assertRedirects(request, '/login')

	def test_login_fails(self):

		response = self.client.post('/login', {'username': 'AAA', 'password': 'aaa'})
		self.assertEquals(response.status_code, 200)
		#self.assertContains(response, 'Please enter the correct username and password for a staff account. Note that both fields may be case-sensitive.')

	
	def test_page_rerouting(self):


		request = self.client.get('/course/01/Lecture-1')
		self.assertEquals(request.status_code,302)
		self.assertRedirects(request, '/login?next=/course/01/Lecture-1')
		response = self.client.post('/login', {'username': 'bbb', 'password': 'B'})
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.context['current_url'], '/login')
	
	def test_create_user(self):

		response = self.client.post('/createuser', {'username': 'aaa', 'password1': 'a', 'password2': 'a', 'first_name': 'A', 'last_name': 'Dude', 'email': 'A@test.com'})
		
		self.assertEquals(response.status_code, 302)
		self.assertRedirects(response, '/alert/create_user_success')
		#print User.objects.get(id=04).username
		self.assertEquals(User.objects.get(id=04).username, 'aaa')

	def test_create_thread(self):

		u2 = User.objects.create(username="RRR", first_name="A", last_name="R", email="@test.com", password="A", is_superuser=False)
		Thread.objects.create(title="Apple", content="Types of Fruit", Creator=u2, views=0, anonymous=False)
		self.assertEquals(Thread.objects.get(id=01).title, 'Apple')
		#print Thread.objects.get(id=01).title

		self.user = self.u1 
		response = self.client.post('/course/threads/new', {'title':'testing', 'content':'new thread', 'Creator':self.user, 'views':0})
		self.assertEquals(response.status_code, 302)
		self.assertRedirects(response, '/login?next=/course/threads')
		
	def test_post_reply(self):

		self.t1 = Thread.objects.create(title="Colour", content="Types of Colour", Creator=self.u1, views=0, anonymous=True)
		self.assertEquals(Thread.objects.get(id=01).title, 'Colour')
		Post.objects.create(Thread=self.t1, content="Blue", Creator=self.u1, rank=1, anonymous=True)
		self.assertEquals(Post.objects.get(id=01).content, 'Blue')

		self.user = self.u2
		response = self.client.post('/course/threads/01/colour', {'Thread':01,'content':'testing reply','Creator':self.user, 'anonymous':False})
		self.assertEquals(response.status_code, 302)
		self.assertRedirects(response, '/login?next=/course/threads/01/colour')
		self.assertEquals(Post.objects.get(id=02).content, 'testing reply')
		#print request.context['current_url']
		#response = self.client.get('/course/threads/01/colour')
		#print Post.objects.get(id=02).content
		#self.assertEquals(Post.objects.get(id=01).content, 'red')

	def test_wordcloud_submit(self):

		Wordcloud.objects.create(title="test", Lecture=self.l1, visible=True)
		self.assertEquals(Wordcloud.objects.get(id=01).title, 'test')

		'''
		self.user = u1
		response = self.client.post('/course/01/lecture-1/wordcloud/01/test', {'lecture_list':self.l1, 'wordcloud':'maybe'})
		'''

		

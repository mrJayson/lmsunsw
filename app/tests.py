from django.test import TestCase, RequestFactory, Client
from django.core.urlresolvers import reverse
from app.models import *
from django.db import IntegrityError
from populate import *

from app.docsURL import glist
from app.views import *
from app.class_based_views import *
from app.forms import CreateThreadForm

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

	def tearDown(self):
		cache.clear()

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

	def tearDown(self):
		cache.clear()

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

	def tearDown(self):
		cache.clear()

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

	def tearDown(self):
		cache.clear()
		

	def test_correct_attr(self):
		Lecture.objects.create(title="Lecture 1")
		Lecture.objects.create(title="Lecture 2")
		Lecture.objects.create(title="Lecture 3")
		Lecture.objects.create(title="Lecture 4")
		Lecture.objects.create(title="Lecture 5")
		Lecture.objects.create(title="Lecture 6")
		Lecture.objects.create(title="Lecture 7")
		Lecture.objects.create(title="Lecture 8")
		Lecture.objects.create(title="Lecture 9")
		Lecture.objects.create(title="Lecture 10")
		#check name is inserted correctly
		self.assertEquals(Lecture.objects.get(id=1).title, "Lecture 1")
		self.assertEquals(Lecture.objects.get(id=2).title, "Lecture 2")
		self.assertEquals(Lecture.objects.get(id=3).title, "Lecture 3")
		self.assertEquals(Lecture.objects.get(id=4).title, "Lecture 4")
		self.assertEquals(Lecture.objects.get(id=5).title, "Lecture 5")
		self.assertEquals(Lecture.objects.get(id=6).title, "Lecture 6")
		self.assertEquals(Lecture.objects.get(id=7).title, "Lecture 7")
		self.assertEquals(Lecture.objects.get(id=8).title, "Lecture 8")
		self.assertEquals(Lecture.objects.get(id=9).title, "Lecture 9")
		self.assertEquals(Lecture.objects.get(id=10).title, "Lecture 10")


		for i, item in enumerate(min(glist, Lecture.objects.all())):
			self.assertEquals(glist[i], Lecture.objects.get(id=i+1).collab_doc)

	def test_glist(self):
		for g in glist:
			l = Rand.lecture()
			self.assertEquals(l.collab_doc, g)

class Quiz_Model(TestCase):

	def tearDown(self):
		cache.clear()

	def test_correct_attr(self):
		l1 = Lecture.objects.create(title="Lecture 1")
		q1 = Quiz.objects.create(question="question", visible=True, Lecture=l1)
		QuizChoice.objects.create(choice="choice", Quiz=q1, correct=True)
		QuizChoice.objects.create(choice="choice", Quiz=q1, correct=True)

		l2 = Lecture.objects.create(title="Lecture 2")
		q2 = Quiz.objects.create(question="question", visible=False, Lecture=l2)
		QuizChoice.objects.create(choice="choice", Quiz=q2, correct=True)
		QuizChoice.objects.create(choice="choice", Quiz=q2, correct=True)
		QuizChoice.objects.create(choice="choice", Quiz=q2, correct=True)

		l3 = Lecture.objects.create(title="Lecture 3")
		q3 = Quiz.objects.create(question="question", visible=True, Lecture=l3)
		QuizChoice.objects.create(choice="choice", Quiz=q3, correct=True)
		QuizChoice.objects.create(choice="choice", Quiz=q3, correct=True)
		QuizChoice.objects.create(choice="choice", Quiz=q3, correct=True)
		QuizChoice.objects.create(choice="choice", Quiz=q3, correct=True)

		l4 = Lecture.objects.create(title="Lecture 4")
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

	def tearDown(self):
		cache.clear()

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

	def tearDown(self):
		cache.clear()

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

		Lecture.objects.create(title="Lecture 1")
		self.assertEquals(Lecture.objects.get(id=01).title, 'Lecture 1')

		request = self.client.get('/course/01/lecture-1')
		self.assertEquals(request.status_code, 302)
	

	def test_quiz_view(self):

		l1 = Lecture.objects.create(title="Lecture 1")
		q1 = Quiz.objects.create(question="question", visible=True, Lecture=l1)
		QuizChoice.objects.create(choice="choice", Quiz=q1, correct=True)
		
		request = self.client.get('/course/01/lecture-1/quiz/01/question')
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



class Redirect_Tests(TestCase):

	def tearDown(self):
		cache.clear()

	def test_login_redirect(self):
		create_student(username="jack", password="password")	
		c = Client()
		response = c.post(reverse('login'), data={'username': 'jack', 'password': 'password'})
		# returns the redirect response and no more
		# response['Location'] is only available for redirect responses
		# added "http://testserver" to reverse as response['Locations'] is the absolute_url
		# and need to convert reverse's relative_url to absolute
		self.assertEquals(response.status_code, 302)
		# these two tests are the same
		self.assertRedirects(response, reverse('root'))
		self.assertEquals(response['Location'], "http://testserver"+reverse('root'))

	def test_student_login(self):
		create_student(username="jack", password="password")	
		c = Client()
		response = c.post(reverse('login'), data={'username': 'jack', 'password': 'password'}, follow=True)
		# follow=True follows the redirects to the end
		# response.context['current_url'] is available for all standard responses
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.context['current_url'], reverse('root'))
		# root and index url map both /index and / to the same view

	def test_admin_login(self):
		create_superuser(username="admin", password="admin")	
		c = Client()
		response = c.post(reverse('login'), data={'username': 'admin', 'password': 'admin'}, follow=True)
		# follow=True follows the redirects to the end
		# response.context['current_url'] is available for all standard responses
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.context['current_url'], reverse('admin:index'))


class New_Form_Test(TestCase):

	def tearDown(self):
		cache.clear()

	def test_new_user(self):

		c = Client()
		response = c.post(reverse('createuser'), data={'username': 'aaa', 'password1': 'a', 'password2': 'a', 'first_name': 'A', 'last_name': 'Dude', 'email': 'A@test.com'})
		self.assertEquals(response.status_code, 302)
		self.assertRedirects(response, '/login_')
		self.assertEquals(User.objects.get(id=01).username, 'aaa')


	def test_new_thread(self):
		
		u1 = create_student(username="jack", password="password")
		Thread.objects.create(title="happy", content="first", Creator=u1, views=0, anonymous=False)
		self.assertEquals(Thread.objects.get(id=01).title, 'happy')
		c = Client()
		
		response = c.post(reverse('login'), data={'username': 'jack', 'password': 'password'}, follow = True)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.context['current_url'], reverse('root'))


		response = c.post(reverse('create_thread'), data={'Creator':u1.id, 'title': 'testing', 'content': 'testing thread', 'anonymous': False, 'views':0}, follow=True)
		self.assertEquals(response.status_code, 200)


		self.assertEquals(Thread.objects.get(id=02).title, 'testing')

	def test_reply_thread(self):

		u1 = create_student(username="jack", password="password")
		t1 = Thread.objects.create(title="Chocolate", content="chocolate", Creator=u1, views=0, anonymous=False)
		self.assertEquals(Thread.objects.get(id=01).title, 'Chocolate')

		c = Client()
		response = c.post(reverse('login'), data={'username': 'jack', 'password': 'password'}, follow = True)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.context['current_url'], reverse('root'))

		# need to supply all form data, including hidden form data
		response = c.post(reverse('post', kwargs={'thread_id':t1.id, 'thread_slug':t1.slug}), data={'Creator':u1.id, 'anonymous': False, 'Thread': t1.id, 'content': 'testing reply'}, follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(Post.objects.get(id=01).content, 'testing reply')

	def test_quiz_selection(self):
		#single choice answer
		u1=create_student(username="jack", password="password")
		u2=create_student(username="harry", password="harry")
		l1=Lecture.objects.create(title="Lecture 1")
		q1=create_quiz(question="question", visible=True, Lecture=l1)
		create_quiz_choice(choice="yes", Quiz=q1, correct=True)
		create_quiz_choice(choice="nope", Quiz=q1, correct=False)
		c=Client()

		response=c.post(reverse('login'), data={'username':'jack', 'password':'password'},follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.context['current_url'], reverse('lecture', kwargs={'lecture_id':l1.id, 'lecture_slug':l1.slug}))

		response=c.post(reverse('quiz', kwargs={'lecture_id':l1.id, 'lecture_slug':l1.slug, 'quiz_id':q1.id, 'quiz_slug':q1.slug}), data={'choices':1, 'user':u1.id}, follow=True)
		#print response.context['form']
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.context['current_url'], reverse('quiz', kwargs={'lecture_id':l1.id, 'lecture_slug':l1.slug, 'quiz_id':q1.id, 'quiz_slug':q1.slug}))		

#Message that checks that it is correct
		self.assertEquals(QuizChoice.objects.get(id=01).correct, True)
		
		#multiple choice answers (all correct)
		l2=Lecture.objects.create(title="Lecture 2")
		q2=create_quiz(question="question2", visible=True, Lecture=l2)
		create_quiz_choice(choice="yes", Quiz=q2, correct=True)
		create_quiz_choice(choice="no", Quiz=q2, correct=False)
		create_quiz_choice(choice="yes", Quiz=q2, correct=True)

		response=c.post(reverse('login'), data={'username':'jack', 'password':'password'},follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.context['current_url'], reverse('lecture', kwargs={'lecture_id':l2.id, 'lecture_slug':l2.slug}))

		response=c.post(reverse('quiz', kwargs={'lecture_id':l2.id, 'lecture_slug':l2.slug, 'quiz_id':q2.id, 'quiz_slug':q2.slug}), data={'choices':5, 'choices':3, 'user':u1.id}, follow=True)
		self.assertEquals(response.status_code, 200)
		#print response.context['form']
		self.assertEquals(response.context['current_url'], reverse('quiz', kwargs={'lecture_id':l2.id, 'lecture_slug':l2.slug, 'quiz_id':q2.id, 'quiz_slug':q2.slug}))		

	def test_quickCreateQuiz_form(self):
		u1=create_superuser(username="admin", password="password")
		l1=Lecture.objects.create(title="Lecture 3")
		c=Client()

		response=c.post(reverse('login'), data={'username': 'admin', 'password': 'password'}, follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.context['current_url'], reverse('admin:index'))

		response=c.post(reverse('admin:login'), data={'question': 'test', 'visible': False, 'Lecture': l1.id, 'User': u1.id}, follow=True)
		self.assertEquals(response.status_code, 200)
		#print response.context['form']
		#self.assertEquals(Quiz.objects.get(id=01).question, 'test')
		self.assertEquals(response.context['current_url'], reverse('admin:login'))
		



class Form_Error_Test(TestCase):

	def tearDown(self):
		cache.clear()
	
	def test_incorrect_login(self):
		
		u1=create_student(username="jack", password="password")
		c=Client()

		#one field missing
		response=c.post(reverse('login'), data={'username': 'jack'}, follow=True)
		self.assertEquals(response.status_code, 200)
		#print response.context['form']
		self.assertEquals(response.context['current_url'], reverse('login'))

		# different ways to test for form errors

		# check any part of response for error message
		self.assertContains(response, 'This field is required')

		# check the form field error list
		self.assertEquals(response.context['form']['password'].errors.as_text(), '* This field is required.')
		self.assertEquals(response.context['form']['password'].errors.__getitem__(0), 'This field is required.')

		#both fields missing
		response=c.post(reverse('login'), data={}, follow=True)
		self.assertEquals(response.status_code, 200)
		#print response.context['form']
		self.assertEquals(response.context['current_url'], reverse('login'))
		#self.assertEquals(response.context['form'].error, 'This Field is Required')

		#username and password dont match
		response=c.post(reverse('login'), data={'username':'test', 'password':'none'}, follow=True)
		self.assertEquals(response.status_code, 200)
		#print response.context['form']
		self.assertEquals(response.context['current_url'], reverse('login'))
		#self.assertEquals(response.context['form'].error, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')


#	def test_quiz_partial_correct(self):

class Check_correct_URL(TestCase):

	def tearDown(self):
		cache.clear()
	
	def test_user_path(self):

		u1=create_student(username="jack", password="password")
		u2=create_student(username="harry", password="harry")
		l1=Lecture.objects.create(title="Lecture 1")
		l2=Lecture.objects.create(title="Lecture 2")
		
		c=Client()

		response=c.post(reverse('login'), data={'username': 'jack', 'password': 'password'}, follow=True)

		request=c.get(reverse('lecture', kwargs={'lecture_id': l1.id, 'lecture_slug': l1.slug}))
		request=c.get(reverse('thread'))
		
		response = c.post(reverse('create_thread'), data={'Creator':u1.id, 'title': 'testing', 'content': 'testing thread', 'anonymous': False, 'views':0}, follow=True)
		#print response.context['form']
		#self.assertEquals(Thread.objects.get(id=01).title, 'testing')

		request=c.get(reverse('post', kwargs={'thread_id': 01, 'thread_slug':Thread.objects.get(id=01).slug}))

		response=c.post(reverse('post', kwargs={'thread_id': 01, 'thread_slug': Thread.objects.get(id=01).slug}), data={'Creator':u1.id, 'anonymous': False, 'Thread': 01, 'content': 'testing reply'}, follow=True)

		request=c.get(reverse('lecture', kwargs={'lecture_id': l2.id, 'lecture_slug': l2.slug}))
		request=c.get(reverse('thread'))

		request=c.get(reverse('post', kwargs={'thread_id': 01, 'thread_slug':Thread.objects.get(id=01).slug}))
		request=c.get(reverse('post', kwargs={'thread_id': 01, 'thread_slug':Thread.objects.get(id=01).slug}))


		response=c.post(reverse('create_thread'), data={'Creator':u1.id, 'title': 'testing2', 'content': 'testing another thread', 'anonymous':True, 'views':0}, follow=True)

		self.assertEquals(response.context['current_url'], reverse('thread'))

		self.assertEquals(Thread.objects.get(id=01).title, 'testing')
		
		self.assertEquals(Post.objects.get(id=01).content, 'testing reply')
		

		self.assertEquals(Thread.objects.get(id=02).title, 'testing2')
